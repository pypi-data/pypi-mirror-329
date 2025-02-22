# ruff: noqa
"""Database

This module contains all classes needed for data persistency, i.e. different
kinds of databases and so on.
"""
from __future__ import annotations
import dataclasses

from chemtrayzer.core.qm import EnergyResult, FreqResult, OptResult
from chemtrayzer.engine.database import (
    Database,
    DatabaseError,
    DBOpenMode,
    IntegrityError,
)


import hashlib
import itertools
import json
import logging
import pickle
import sqlite3
from abc import ABCMeta, abstractmethod
from math import inf
from typing import Any, Iterable, NewType, Type, Union

import numpy as np

from chemtrayzer.core.chemid import Reaction, Species
from chemtrayzer.core.coords import ChainOfStates, ConfDiffOptions, ConformerEnsemble, Geometry, TSGeometry
from chemtrayzer.core.lot import BasisSet, LevelOfTheory

from ._serialization import IJsonConvertible


class SpeciesMismatchError(DatabaseError):
    """raised when the species generated from a geometry does not match the
    provided species id."""

    # it does not exist


GeoId = NewType("GeoId", int)

class GeometryDatabase(Database):
    """Database to store geometry and energy information

    This database stores geometries in groups which belong together. A group
    can e.g. consist of all geometries belonging to a species or to a reaction.
    The exact interpretation of what a group is, can be made in a child class.
    """

    # append version and table defintions
    _VERSION = {"GeometryDatabase": "3.1", **Database._VERSION}

    _TABLES = {
        # table name: [
        #   (column name, column type),
        #   ...
        # ],
        "geometry_ids": [
            ("geometry_id", "integer primary key"),
            ("group_id", "text"),
            ("type", "text CHECK(type IN ('geo','cos')) " "NOT NULL DEFAULT 'geo'"),
        ],
        "geometries": [
            ("geometry_id", "integer primary key"),
            ("geometries", "blob"),
            ("level_of_theory", "integer"),
            ("rotational_symmetry_nr", "integer"),
        ],
        "chains_of_states": [
            ("geometry_id", "integer primary key"),
            ("chains_of_states", "blob"),
        ],
        "levels_of_theory": [
            ("level_of_theory", "integer primary key"),
            ("hash", "blob"),
            ("json", "blob"),
        ],
        "energies": [
            ("geometry_id", "integer"),
            ("energy", "real"),
            ("level_of_theory", "integer"),
        ],
        "gradients": [
            ("geometry_id", "integer"),
            ("gradient", "blob"),
            ("level_of_theory", "integer"),
        ],
        "hessians": [
            ("geometry_id", "integer"),
            ("hessian", "blob"),
            ("level_of_theory", "integer"),
        ],
        "frequencies": [
            ("geometry_id", "integer"),
            ("frequencies", "blob"),
            ("level_of_theory", "integer"),
        ],
        "assoc_data": [("geometry_id", "integer"), ("key", "text"), ("data", "text")],
        **Database._TABLES,
    }

    def _update_version(
        self, old_version: tuple[int, int], new_version: tuple[int, int]
    ):
        if old_version[0] == 3 and new_version[0] == 3:
            new_version_str = "3." + str(new_version[1])

            if old_version[1] == 0:
                # From version 3.0 to 3.1 the type column was added to the
                # geometry table and the not null constraint was added to the
                # geometry_id columns. Before, there was just one type of
                # geometry (geo), now there are two: geo and cos.
                # Additionally, the chain_of_states table was added
                with self._con:
                    # add new table adhering to new schema
                    sql = self._sql_table_schema()["geometry_ids"]
                    sql = sql.replace("geometry_ids", "new_geometry_ids")
                    self._con.execute(sql)

                    # copy old data to new table and drop old table
                    self._con.execute(
                        "INSERT INTO new_geometry_ids (group_id, geometry_id) "
                        "SELECT group_id, geometry_id FROM geometry_ids"
                    )
                    self._con.execute("DROP TABLE geometry_ids")

                    # rename old table
                    self._con.execute(
                        "ALTER TABLE new_geometry_ids " "RENAME TO geometry_ids"
                    )

                    # add chains_of_states_table
                    self._con.execute(self._sql_table_schema()["chains_of_states"])

                    self._con.execute(
                        "UPDATE db_info SET version=? WHERE class=?",
                        (new_version_str, "GeometryDatabase"),
                    )

                    logging.info(
                        "Updated database from version 3.0 to %s", new_version_str
                    )

    def _list_group_ids(self) -> Iterable[str]:
        """
        This database stores groups of geometries. A group canee.g. consist of
        all geometries belonging to a species or to a reaction.

        :return: list of all group ids
        """

        return [
            group_id
            for group_id, in self._con.execute(
                "SELECT DISTINCT group_id " "FROM geometry_ids"
            )
        ]

    def _check_if_geo_id_in_db(self, geo_id: GeoId):
        # give a bette error message than sqlite
        if type(geo_id) != int:
            raise DatabaseError(
                "Geometry id does not have the correct type."
                f"{type(geo_id)} != GeoId alias int"
            )

        cur = self._con.execute(
            "SELECT geometry_id FROM geometries WHERE " "geometry_id=(?)", (geo_id,)
        )

        result = cur.fetchone()
        cur.close()

        if result is None:
            raise DatabaseError(f'Unkown geometry id: "{geo_id}"')

    def list_geometries(
        self, id: str, criterion: "GeometryCriterion" = None
    ) -> Iterable[GeoId]:
        """
        :param id: identifier for species or reaction
        :param criterion: criterion on the geometries (e.g. moment of inertia)
        :return: list of geometry ids (empty if no geometry matches the
                 criteria)
        """
        cur = self._con.execute(
            "SELECT geometry_id FROM geometry_ids " 'WHERE group_id=? AND type="geo"',
            (id,),
        )

        geo_ids = [geo_id for geo_id, in cur]

        if criterion is None:
            result = geo_ids
        else:
            # some criteria return sets which may be unexpected, so we are
            # making lists out of them
            result = list(criterion.eval(self, geo_ids, id))

        return result

    def save_geometry(
        self,
        id: str,
        geo: Geometry,
        lot: LevelOfTheory = None,
        rotational_symmetry_nr: int = None,
    ) -> GeoId:
        """
        :param id: identifier for species or reaction
        :param geo: geometry to be saved
        :param lot: level of theory at which the geometry was optimized
        :param rotational_symmetry_nr: (optional) symmetry number for external
                                        rotational partition function
        :return: id assigned to this geometr
        """
        with self._con:
            lot_id = self._save_lot(lot)

            # use None as geo_id to let sqlite figure out the next id
            cur = self._con.execute(
                "INSERT INTO geometry_ids " 'VALUES (?, ?, "geo")', (None, id)
            )
            # since geometry_id is of type integer primary key, this column
            # is allso the row id
            geo_id = cur.lastrowid

            geo_bytes = pickle.dumps(geo)
            cur.execute(
                "INSERT INTO geometries VALUES (?, ?, ?, ?)",
                (geo_id, geo_bytes, lot_id, rotational_symmetry_nr),
            )

        return geo_id

    def save_cos(self, id: str, cos: ChainOfStates) -> GeoId:
        """
        :param cos: chain of states object to store
        :param id: identifier for species or reaction
        :return: id assigned to this chain of states object"""
        with self._con:
            # use None as geo_id to let sqlite figure out the next id
            cur = self._con.execute(
                "INSERT INTO geometry_ids " 'VALUES (?, ?, "cos")', (None, id)
            )
            # since geometry_id is of type integer primary key, this column
            # is also the row id
            geo_id = cur.lastrowid

            cos_bytes = pickle.dumps(cos)
            self._con.execute(
                "INSERT INTO chains_of_states VALUES (?, ?)", (geo_id, cos_bytes)
            )

        return geo_id

    def list_cos(self, id: str) -> Iterable[GeoId]:
        """
        :param id: identifier for species or reaction
        :return: list of geometry ids for all chain of states geometries
        """
        with self._con:
            cur = self._con.execute(
                "SELECT geometry_id FROM geometry_ids "
                'WHERE group_id=(?) AND type="cos"',
                (id,),
            )

            return [geo_id for geo_id, in cur]

    @classmethod
    def _hash_lot(cls, lot: LevelOfTheory) -> bytes:
        """Since Python's hash function salts strings before hashing, it cannot
        be used for database applications. This function creates a stable hash
        based on the JSON representation of lot

        :return: SHA1 hash of the JSON representation of lot (exluding default
                 values and non-hash fields)"""

        # the hash should be the same for two LevelOfTheory objects that only
        # differ in the value of a non-hash field. To improve extendability,
        # default values will also not be included. That way, it is possible to
        # add new default-initialized fields to a dataclass without changing the
        # hash
        json_str = lot.to_json(
            exclude_non_hash_fields=True, exclude_default_values=True
        )

        # not used for security
        m = hashlib.sha1()
        m.update(bytes(json_str, encoding="utf-8"))
        return m.digest()

    def _save_lot(self, lot: LevelOfTheory) -> int:
        """checks if the same lot already exsists and, if not, stores it
        :return: id (column name = level_of_theory) of lot in levels_of_theory
        """
        if lot is None:
            return None

        hash_val = self._hash_lot(lot)

        # use connectino as context manager to lock the database between
        # determining if the lot is in the database and storing it
        with self._con:
            # get lots with the same hash AND the same json representation
            cur = self._con.execute(
                "SELECT level_of_theory "
                "FROM levels_of_theory WHERE hash=(?) AND json=(?)",
                (hash_val, lot),
            )

            lot_id = cur.fetchone()
            cur.close()

            # store lot, if it does not already exist
            if lot_id is not None:
                lot_id = lot_id[0]  # fetchone returns a tuple
            else:
                cur = self._con.execute(
                    "INSERT INTO levels_of_theory " "VALUES (?, ?, ?)",
                    (None, hash_val, lot),
                )

                lot_id = cur.lastrowid
                cur.close()

        # return either the new or existing lot_id
        return lot_id

    def load_rotational_symmetry_nr(self, geo_id: GeoId) -> Union[int, None]:
        """:return: rotational symmetry number for geometry with id geo_id"""
        cur = self._con.execute(
            "SELECT rotational_symmetry_nr FROM geometries" " WHERE geometry_id=(?)",
            (geo_id,),
        )

        rot_symm_nr = cur.fetchone()

        if rot_symm_nr is None:
            return None
        else:
            # fetchone returns a tuple -> use only first index
            return rot_symm_nr[0]

    def _load_cos_or_geo(
        self, geo_id: GeoId, type: str
    ) -> Union[Geometry, ChainOfStates]:
        """loads either a geometry or a chain of states object"""
        if type == "geo":
            cls_name, table_name, col_name = "Geometry", "geometries", "geometries"
        elif type == "cos":
            cls_name, table_name, col_name = (
                "ChainOfStates",
                "chains_of_states",
                "chains_of_states",
            )

        cur = self._con.cursor()

        # first check what type of object we are loading
        cur.execute("SELECT type FROM geometry_ids WHERE geometry_id=(?)", (geo_id,))
        geo_type = cur.fetchone()

        if geo_type is None:
            return None
        elif geo_type[0] != type:
            logging.debug(
                "Object with id %d could not be loaded b/c this id" " is not a %s",
                geo_id,
                cls_name,
            )
            return None

        # now try to load the actual object
        cur.execute(
            f"SELECT {col_name} FROM {table_name} " "WHERE geometry_id=(?)", (geo_id,)
        )
        geo_binary = cur.fetchone()

        if geo_binary is None:
            return None
        else:
            # fetchone returns a tuple
            geo_binary = geo_binary[0]

        geo = pickle.loads(geo_binary)

        cur.close()

        return geo

    def load_geometry(self, geo_id: GeoId) -> Geometry:
        """
        :param geo_id: id of the geometry in this database
        :return: geometry that belongs to geo_id or None if there is no
                 geometry with that id
        """
        return self._load_cos_or_geo(geo_id, "geo")

    def load_cos(self, geo_id: GeoId) -> ChainOfStates:
        """
        :param geo_id: id of the chain of states in this database
        :return: chain of states that belongs to geo_id or None if there is no
                 chain of states with that id
        """
        return self._load_cos_or_geo(geo_id, "cos")

    def load_LOT_of_geometry(self, geo_id: GeoId) -> Union[LevelOfTheory, None]:
        """:return: level of theory at which geo_id was optimized (or None)"""

        cur = self._con.execute(
            'SELECT json AS "lot [LevelOfTheory]" FROM '
            "levels_of_theory INNER JOIN geometries "
            "ON levels_of_theory.level_of_theory = geometries.level_of_theory "
            "WHERE geometry_id=(?)",
            (geo_id,),
        )

        result = cur.fetchall()
        cur.close()

        if result:
            assert len(result) == 1

            result = result[0][0]  # fetchall returns a list of tuples
        else:
            result = None

        return result

    def _list_LOTS(self, geo_id: GeoId, table: str) -> Iterable[LevelOfTheory]:
        """usef for all list_LOT_of... methods"""
        cur = self._con.execute(
            f'SELECT json AS "lot [LevelOfTheory]" FROM '
            f"levels_of_theory INNER JOIN {table} ON levels_of_theory.level_of_"
            f"theory = {table}.level_of_theory "
            "WHERE geometry_id=(?)",
            (geo_id,),
        )

        result = cur.fetchall()
        cur.close()

        # unpack list of tuples into list
        if result is not None:
            result = [r[0] for r in result]
        else:
            result = []

        return result

    def list_LOT_of_energies(self, geo_id: GeoId) -> Iterable[LevelOfTheory]:
        """
        :param geo_id: id of the geometry in this database
        :return: a list of all levels of theory at which electronic energies
                 have been computed for the geometry with geo_id, the list
                 can be empty if no energies are stored for the geometry
        """
        return self._list_LOTS(geo_id, "energies")

    def list_LOT_of_hessians(self, geo_id: GeoId) -> Iterable[LevelOfTheory]:
        """
        :param geo_id: id of the geometry in this database
        :return: a list of all levels of theory at which Hessian matrices
                 have been computed for the geometry with geo_id
        """
        return self._list_LOTS(geo_id, "hessians")

    def list_LOT_of_frequencies(self, geo_id: GeoId) -> Iterable[LevelOfTheory]:
        """
        :param geo_id: id of the geometry in this database
        :return: a list of all levels of theory at which harmonic oscillator
                 frequencies have been computed for the geometry with geo_id
        """
        return self._list_LOTS(geo_id, "frequencies")

    def list_LOT_of_gradients(self, geo_id: GeoId) -> Iterable[LevelOfTheory]:
        """
        :param geo_id: id of the geometry in this database
        :return: a list of all levels of theory at which gradients were computed
        """
        return self._list_LOTS(geo_id, "gradients")

    def _save_E_H_grad(
        self,
        geo_id: GeoId,
        lot: LevelOfTheory,
        table: str,
        obj: Union[float, np.ndarray],
    ):
        """saving energies, Hessians and gradients requires more or less the
        same code, so this function is used for all three
        """
        self._check_if_geo_id_in_db(geo_id)

        lot_id = self._save_lot(lot)

        self._con.execute(
            f"INSERT INTO {table} VALUES (?, ?, ?)", (geo_id, obj, lot_id)
        ).close()  # we don't need the returned cursor -> close
        self._con.commit()

    def save_electronic_energy(self, geo_id: GeoId, lot: LevelOfTheory, energy: float):
        """
        :param geo_id: id of the geometry in this database
        :param lot: level of theory at which the energy was computed
        :param energy: electronic energy for this species/TS and geometry at lot
        """
        self._save_E_H_grad(geo_id, lot, "energies", energy)

    def save_hessian(
        self, geo_id: GeoId, lot: LevelOfTheory, hessian: np.ndarray
    ) -> None:
        """
        :param geo_id: id of the geometry in this database
        :param lot: level of theory at which the energy was computed
        :param hessian: Hessian matrix for geometry of species/TS at lot
        """
        hessian = np.array(hessian)
        self._save_E_H_grad(geo_id, lot, "hessians", hessian)

    def save_frequencies(self, geo_id: GeoId, lot: LevelOfTheory, freqs: np.ndarray):
        """
        :param geo_id: id of the geometry in this database
        :param lot: level of theory at which the energy was computed
        :param freqs: harmonic oscillator frequencies
        """
        freqs = np.array(freqs)
        self._save_E_H_grad(geo_id, lot, "frequencies", freqs)

    def save_gradient(self, geo_id: GeoId, lot: LevelOfTheory, grad: np.ndarray):
        """
        :param geo_id: id of the geometry in this database
        :param lot: level of theory at which the energy was computed
        :param grad: gradient
        """
        grad = np.array(grad)
        self._save_E_H_grad(geo_id, lot, "gradients", grad)

    def _assert_assoc_data_key_is_unique(self, geo_id: GeoId, key: str):
        cur = self._con.execute(
            "SELECT key FROM assoc_data WHERE geometry_id=?", (geo_id,)
        )

        for (existing_key,) in cur.fetchall():
            if existing_key == key:
                raise IntegrityError(
                    f"Data with key {key} already exists for "
                    f"geometry with id {geo_id}"
                )

        cur.close()

    def save_assoc_data(
        self, geo_id: GeoId, key: str, data: Union[dict, list, str, int, float, bool]
    ):
        """saves data associated with geometry with id geo_id. The data must be given a unique key and simple Python types (i.e. dict, list, str, int, float and bool) as values.
        This function will raise an IntegrityError when there is already data with the given key associated with the geometry.
        """
        self._check_if_geo_id_in_db(geo_id)

        # lock db between checking if the key is unique and writing
        with self._con:
            self._assert_assoc_data_key_is_unique(geo_id, key)

            data_json = json.dumps(data)

            self._con.execute(
                "INSERT INTO assoc_data VALUES (?,?,?)", (geo_id, key, data_json)
            ).close()

    def update_assoc_data(
        self, geo_id: GeoId, key: str, data: Union[dict, list, str, int, float, bool]
    ):
        """Updates the associated data dictionary for geometry with id geo_id"""
        self._check_if_geo_id_in_db(geo_id)

        cur = self._con.execute(
            "UPDATE assoc_data SET data=(?) WHERE key=(?) " "AND geometry_id=(?)",
            (data, key, geo_id),
        )

        if cur.rowcount != 1:
            raise DatabaseError(
                f"No existing data for geo_id={geo_id} and " f'key="{key}"'
            )

        cur.close()

    def load_assoc_data(self, geo_id: GeoId, key: str) -> Any:
        """loads the data associated to a geometry with id geo_id
        :return: the data stored for the given key or None, if there is no data for that key
        """
        self._check_if_geo_id_in_db(geo_id)

        cur = self._con.execute(
            "SELECT data FROM assoc_data WHERE key=(?) " "AND geometry_id=(?)",
            (key, geo_id),
        )

        result = cur.fetchone()

        cur.close()

        if result is None:
            return None
        else:
            return json.loads(result[0])

    def _load_E_H_grad(
        self,
        geo_id: GeoId,
        lot: LevelOfTheory,
        table: str,
        column: str,
        alias: str = None,
    ) -> Union[float, np.ndarray]:
        """loading energies, Hessians and gradients requires more or less the
        same code, so this function is used for all three
        """
        # the alias is needed to leverage the converter functionality of
        # Python's sqlite3 module
        alias = "" if alias is None else 'AS "' + alias + '" '

        cur = self._con.execute(
            f"SELECT {column} {alias} FROM {table} t INNER JOIN levels_of_theory l ON t.level_of_theory = l.level_of_theory "
            "WHERE t.geometry_id=(?) AND l.hash=(?)",
            (geo_id, self._hash_lot(lot)),
        )

        data = cur.fetchone()
        cur.close()

        if data is not None:
            return data[0]
        else:
            return None

    def load_electronic_energy(self, geo_id: GeoId, lot: LevelOfTheory) -> float:
        """
        :param geo_id: id of the geometry in this database
        :param lot: level of theory at which the energy was computed
        :return: electronic energy in atomic units or None, if no energy found
                 for the speciefied level of theory
        """
        return self._load_E_H_grad(geo_id, lot, "energies", "energy")

    def load_hessian(self, geo_id: GeoId, lot: LevelOfTheory) -> np.ndarray:
        """
        :param geo_id: id of the geometry in this database
        :param lot: level of theory at which the energy was computed
        :return: Hessian matrix for the given geometry of species/TS at lot or
                    None
        """
        return self._load_E_H_grad(
            geo_id, lot, "hessians", "hessian", alias="hessian [np.ndarray]"
        )

    def load_frequencies(self, geo_id: GeoId, lot: LevelOfTheory) -> np.ndarray:
        """
        :param geo_id: id of the geometry in this database
        :param lot: level of theory at which the energy was computed
        :return: vector of harmonic oscillator frequencies for the given
                    geometry of the species at lot or None
        """
        return self._load_E_H_grad(
            geo_id, lot, "frequencies", "frequencies", alias="frequencies [np.ndarray]"
        )

    def load_gradient(self, geo_id: GeoId, lot: LevelOfTheory) -> np.ndarray:
        """
        :param geo_id: id of the geometry in this database
        :param lot: level of theory at which the energy was computed
        :return: gradient of the energy w.r.t. geometry
        """
        return self._load_E_H_grad(
            geo_id, lot, "gradients", "gradient", alias="gradient [np.ndarray]"
        )

    def save_opt_result(self, id: str, opt_result: OptResult,
                        lot: LevelOfTheory|None = None) -> GeoId:
        """store result of a geometry optimization

        :param id: identifier for species or reaction
        :param opt_result: result of a geometry optimization
        :return: id assigned to this geometry
        """
        rot_sym = (opt_result.final.rotational_symmetry_nr
                   if opt_result.final is not None
                   else None)
        geo_id = self.save_geometry(id, opt_result.geometries[-1], lot=lot,
                                    rotational_symmetry_nr=rot_sym)

        self.save_electronic_energy(geo_id, lot, opt_result.energies[-1])

        if opt_result.final is not None:
            self.save_freq_result(geo_id, freq_result=opt_result.final,
                                  lot=lot)

        return geo_id

    def save_freq_result(self, geo_id: GeoId, freq_result: FreqResult,
                         lot: LevelOfTheory|None = None):
        """store result of a frequency calculation

        :param geo_id: id of the geometry in this database
        :param freq_result: result of a frequency calculation
        """
        self.save_frequencies(geo_id, lot=lot, freqs=freq_result.frequencies)
        self.save_hessian(geo_id, lot=lot, hessian=freq_result.hessian)

        if freq_result.gradient is not None:
            self.save_gradient(geo_id, lot=lot, grad=freq_result.gradient)

    def save_energy_result(self, geo_id: GeoId, energy_result: EnergyResult,
                           lot: LevelOfTheory|None = None):
        """store result of an energy calculation

        :param geo_id: id of the geometry in this database
        :param energy_result: result of an energy calculation
        """
        self.save_electronic_energy(geo_id, lot, energy_result.energy)

        if energy_result.gradient is not None:
            self.save_gradient(geo_id, lot, grad=energy_result.gradient)
        if energy_result.hessian is not None:
            self.save_hessian(geo_id, lot, hessian=energy_result.hessian)


class SpeciesDB(GeometryDatabase):
    # add a table to the database
    _TABLES = {
        # table name: [
        #   (column name, column type),
        #   ...
        # ],
        "species": [
            ("species_id", "text primary key"),  # species_id = group_id
            ("inchi", "text"),
            ("smiles", "text"),
        ],
        **GeometryDatabase._TABLES,
    }

    _VERSION = {"SpeciesDB": "3.0", **GeometryDatabase._VERSION}

    def __init__(self, path, mode=DBOpenMode.WRITE) -> None:
        super().__init__(path, mode)

    def save_geometry(
        self,
        species_id: str,
        geo: Geometry,
        lot: LevelOfTheory = None,
        rotational_symmetry_nr: int = None,
    ) -> GeoId:
        """
        Saves a geometry. If there is no species object for the species in the
        database, one will be created. When a species id is provided, it will be
        checked against the id of the species object created from the geometry
        and an error will be raised in case of mismatch.

        :param species_id: id of species that the geometry belongs to. If None,
                           the species id is determined from the geometry.
        :param geo: geometry to be saved
        :param lot: level of theory at which the geometry was optimized
        :return: species id, id assigned to this geometry
                    or None if the insertion failed
        """
        species = Species.from_geometry(geo)

        if species_id is None:
            species_id = species.id

        elif species_id != species.id:
            raise SpeciesMismatchError(
                "The species id that was provided"
                " does not match the species object that was generated from the"
                " given geometry."
            )

        with self._con:
            cur = self._con.execute(
                "SELECT EXISTS(SELECT 1 FROM species " "WHERE species_id=(?))",
                (species_id,),
            )

            is_species_in_db = cur.fetchone()[0]
            cur.close()

            if not is_species_in_db:
                self.save_species(species)

            return super().save_geometry(
                species_id,
                geo,
                lot=lot,
                rotational_symmetry_nr=rotational_symmetry_nr,
            )

    def list_species(self) -> Iterable[str]:
        """:return: a list of all ids of all species stored in the db"""

        cur = self._con.execute("SELECT species_id FROM species")
        species = [id for id, in cur]
        cur.close()

        return species

    def list_geometries(
        self, id: str, criterion: "GeometryCriterion" = None
    ) -> Iterable[GeoId]:
        # if a species object is passed instead of an id, handle it gracefully
        if isinstance(id, Species):
            id = id.id

        return super().list_geometries(id, criterion)

    def save_species(self, species: Species):
        """inserts species into database

        :param species: species to save in database"""

        with self._con:
            self._con.execute(
                "INSERT INTO species VALUES(?, ?, ?)",
                (species.id, species.inchi, species.smiles),
            ).close()

    def load_species(self, species_id: str) -> Species:
        """:param species_id: id of species to load
        :return: species or None"""

        cur = self._con.execute(
            "SELECT species_id, inchi, smiles " "FROM species WHERE species_id=(?)",
            (species_id,),
        )
        species_entry = cur.fetchone()

        if species_entry is None:
            return None
        else:
            return Species(
                id=species_entry[0], inchi=species_entry[1], smiles=species_entry[2]
            )


class ReactionRateDB(Database):
    """This database can be used to store the reaction rates obtained from
    reactive molecular dynamics simulations at different temperatures"""

    _TABLES = {
        "rates": [
            ("reaction_id", "text"),
            ("temperature", "real unique"),
            ("rate", "real"),
        ]
    }

    _VERSION = {"ReactionRateDB": "1.0"}

    def save_reaction_rate(self, reaction_id: str, temperature: float, rate: float):
        """
        :param: temperature [K]
        :param: rate in cm³, mol, and seconds
        """
        try:
            with self._con:
                self._con.execute(
                    "INSERT INTO rates VALUES (?, ?, ?)",
                    (reaction_id, temperature, rate),
                ).close()
        except sqlite3.IntegrityError:
            raise IntegrityError(
                f'A reaction rate for reaction "{reaction_id}" '
                f"and T = {temperature} K already exists in the database."
            )

    def load_reaction_rates(self, reaction_id: str) -> dict[float, float]:
        """:return: map from temperature to reaction rate"""
        cur = self._con.execute(
            "SELECT temperature, rate FROM rates" " WHERE reaction_id=(?)",
            (reaction_id,),
        )

        data = cur.fetchall()
        cur.close()

        return {T: k for T, k in data}


class ReactionDB(GeometryDatabase, ReactionRateDB):
    _TABLES = {
        # table name: [
        #   (column name, column type),
        #   ...
        # ],
        "reactions": [
            ("reaction_id", "text primary key"),  # group id = reaction id
            ("reaction", "blob"),
        ],
        "transition_states": [("reaction_id", "text"), ("geometry_id", "integer")],
        "IRC_endpoints": [
            ("reaction_id", "text"),
            ("start", "integer"),  # contains geometry id
            ("end", "integer"),  # contains geometry id
        ],
        **GeometryDatabase._TABLES,
        **ReactionRateDB._TABLES,
    }

    _VERSION = {
        "ReactionDB": "2.0",
        **GeometryDatabase._VERSION,
        **ReactionRateDB._VERSION,
    }

    def __init__(self, path, mode=DBOpenMode.WRITE) -> None:
        super().__init__(path, mode)

    def _assert_that_reaction_in_db(self, id: str):
        cur = self._con.execute(
            "SELECT EXISTS(SELECT 1 FROM reactions " "WHERE reaction_id=(?))", (id,)
        )

        is_reaction_in_db = cur.fetchone()[0]
        cur.close()

        if not is_reaction_in_db:
            raise IntegrityError(f'Reaction "{id}" not in database.')

    def save_geometry(
        self,
        reaction: str,
        geo: Geometry,
        lot: LevelOfTheory = None,
        rotational_symmetry_nr: int = None,
    ) -> GeoId:
        with self._con:
            self._assert_that_reaction_in_db(reaction)

            return super().save_geometry(reaction, geo, lot, rotational_symmetry_nr)

    def list_reactions(self) -> Iterable[str]:
        """lists the ids of all reactions stored in this database"""

        cur = self._con.execute("SELECT reaction_id FROM reactions")
        reactions = [id for id, in cur]
        cur.close()

        return reactions

    def save_reaction(self, rxn: Reaction):
        """:param rxn: reaction to store in this database"""
        with self._con:
            self._con.execute(
                "INSERT OR REPLACE INTO reactions VALUES(?,?)", (rxn.id, rxn)
            ).close()

    def load_reaction(self, rxn: str) -> Reaction:
        """:param rxn: id of reaction to load
        :return: reaction with id rxn or None, if there is no reaction with
                 that id
        """
        cur = self._con.execute(
            'SELECT reaction AS "reaction [Reaction]" '
            "FROM reactions WHERE reaction_id=(?)",
            (rxn,),
        )
        reaction = cur.fetchone()

        if reaction is None:
            return None
        else:
            # if not None, then species is a one-tuple
            return reaction[0]

    def list_TS_geometries(self, rxn: Reaction|str) -> Iterable[GeoId]:
        """
        .. note: If you need to apply criteria, use ``list_geometries`` and combine the IsTransitionState criterium with the other criteria needed.

        :param rxn: (id of) reaction for which to load the transition states
                    If reaction object is provided instead of id, TS stored as
                    belonging only to the reverse reaction are also listed
        :return: a list of transition state geometries. The list is empty, if no
                 IRC endpoint at that level of theory were stored.
        """
        if isinstance(rxn, str):
            cur = self._con.execute(
                "SELECT geometry_id FROM transition_states "
                "WHERE reaction_id = (?)",
                (rxn, ),
            )
        else:
            cur = self._con.execute(
                "SELECT geometry_id FROM transition_states "
                "WHERE reaction_id = (?) OR reaction_id = (?)",
                (rxn.id, rxn.reverse().id),
            )
        ids = [geo_id for geo_id, in cur]
        cur.close()

        return ids

    def save_TS_geometry(self, rxn: str, geo: TSGeometry, lot: LevelOfTheory) -> GeoId:
        """
        :param rxn: id of reaction to which the transition state geometry
                    belongs
        :param geo: geometry to store
        :param lot: level of theory at which geo was optimized
        """
        with self._con:
            geo_id = self.save_geometry(rxn, geo, lot)

            self._con.execute(
                "INSERT INTO transition_states VALUES(?,?)", (rxn, geo_id)
            )

        return geo_id

    def save_ts_opt_result(self, rxn: str, opt_result: OptResult,
                        lot: LevelOfTheory|None = None) -> GeoId:
        """store result of a geometry optimization

        :param rxn: identifier for species
        :param opt_result: result of a geometry optimization
        :return: id assigned to this geometry
        """
        geo_id = self.save_opt_result(rxn, opt_result=opt_result, lot=lot)

        with self._con:
            self._con.execute(
                "INSERT INTO transition_states VALUES(?,?)", (rxn, geo_id)
            )

        return geo_id


    def list_IRC_endpoints(self, rxn: str) -> Iterable[tuple[GeoId, GeoId]]:
        """
        :param rxn: id of reaction for which to load IRC endpoints
        :param lot: level of theory at which the IRC was computed
        :return: a list of the IRC endpoints. The list is empty, if no
                 IRC endpoint at that level of theory were stored.
        """
        cur = self._con.execute(
            "SELECT start, end FROM IRC_endpoints " "WHERE reaction_id=(?)", (rxn,)
        )
        irc_pts = cur.fetchall()
        cur.close()

        if irc_pts is None:
            return []
        else:
            return irc_pts

    def save_IRC_endpoints(
        self, rxn: str, start: Geometry, end: Geometry, lot: LevelOfTheory
    ) -> tuple[GeoId, GeoId]:
        """
        :param rxn: id of reaction for which to load IRC endpoints
        :param lot: level of theory at which the IRC was computed
        :param start: starting point of IRC
        :param end: end point of IRC
        """
        with self._con:
            start_id = self.save_geometry(rxn, start, lot)
            end_id = self.save_geometry(rxn, end, lot)

            self._con.execute(
                "INSERT INTO IRC_endpoints VALUES(?,?,?)", (rxn, start_id, end_id)
            ).close()

        return start_id, end_id

    def save_reaction_rate(self, reaction_id: str, temperature: float, rate: float):
        with self._con:
            self._assert_that_reaction_in_db(reaction_id)
            return super().save_reaction_rate(reaction_id, temperature, rate)


class GeometryCriterion(metaclass=ABCMeta):
    """Specifies which geometries should considered. Criteria can be chained
    using the operators ``&`` (and), ``|`` (or), ``~`` (not) and ``>>``. The
    latter operator ensures that the criterion on the left is evaluated before
    the criterion on the right."""

    def __and__(self, other):
        return _AndCriterion(self, other)

    def __or__(self, other):
        return _OrCriterion(self, other)

    def __invert__(self):
        return _NotCrtierion(self)

    def __rshift__(self, other):
        return _OrderedExecutionCriterion(self, other)

    @abstractmethod
    def eval(
        self, db: GeometryDatabase, geo_ids: Iterable[GeoId], id: str
    ) -> Iterable[GeoId]:
        """
        :param db: database containing this geometry
        :param geo_id: ids of geometries to evaluate the criterion against
        :param id: id of the reaction, species or group of geometries that the
                   geo_ids belong to
        :return: ids of geometries for which the criterion is fulfilled. This
                 must be a (potentially empty or complete) subset of geo_ids
        """


class _AndCriterion(GeometryCriterion):
    """combines two criteria with a logical and"""

    def __init__(self, left: GeometryCriterion, right: GeometryCriterion) -> None:
        super().__init__()

        self._left = left
        self._right = right

    def eval(
        self, db: GeometryDatabase, geo_ids: Iterable[GeoId], id: str
    ) -> Iterable[GeoId]:
        return set(self._left.eval(db, geo_ids, id)) & set(
            self._right.eval(db, geo_ids, id)
        )


class _OrCriterion(GeometryCriterion):
    """combines two criteria with a logical or"""

    def __init__(self, left: GeometryCriterion, right: GeometryCriterion) -> None:
        super().__init__()

        self._left = left
        self._right = right

    def eval(
        self, db: GeometryDatabase, geo_ids: Iterable[GeoId], id: str
    ) -> Iterable[GeoId]:
        return set(self._left.eval(db, geo_ids, id)) | set(
            self._right.eval(db, geo_ids, id)
        )


class _NotCrtierion(GeometryCriterion):
    """inverts a criterion logically"""

    def __init__(self, crit: GeometryCriterion) -> None:
        super().__init__()
        self._crit = crit

    def eval(
        self, db: GeometryDatabase, geo_ids: Iterable[GeoId], id: str
    ) -> Iterable[GeoId]:
        return set(geo_ids) - set(self._crit.eval(db, geo_ids, id))


class _OrderedExecutionCriterion(GeometryCriterion):
    """ensures that one criterion is executed before the other"""

    def __init__(self, first: GeometryCriterion, last: GeometryCriterion) -> None:
        super().__init__()
        self.first = first
        self.last = last

    def eval(
        self, db: GeometryDatabase, geo_ids: Iterable[GeoId], id: str
    ) -> Iterable[GeoId]:
        geo_ids = self.first.eval(db, geo_ids, id)
        geo_ids = self.last.eval(db, geo_ids, id)

        return geo_ids


class MOICriterion(GeometryCriterion):
    """checks if moments of intertia are close to defined values w.r.t. an
    absolute tolerance

    :param principals: principal moments of inertia in ascending order
    :param atol: absolute tolerance for MOIs
    """

    def __init__(self, principals: np.ndarray, atol: float) -> None:
        super().__init__()
        self._principals = principals
        self._atol = atol

    def eval(
        self, db: GeometryDatabase, geo_ids: Iterable[GeoId], id: str
    ) -> Iterable[GeoId]:
        keep_ids = []

        for geo_id in geo_ids:
            geo = db.load_geometry(geo_id)

            if np.all(
                np.abs(geo.moment_of_inertia()[0] - self._principals) <= self._atol
            ):
                keep_ids.append(geo_id)

        return keep_ids


class GeometricConformerCriterion(GeometryCriterion):
    """Check if the given conformer is the reference conformer based on purely
    geometric criteria

    :param ref_geo: reference geometry
    :param rmsd_threshold: RMSD threshold for distinguing conformers [Angstrom]
    :param rot_threshold: threshold for distinguishing conformers based on
                          the rotational constant [percent]
    """

    def __init__(
            self,
            ref_geo: Geometry,
            rmsd_threshold: float,
            rot_threshold: float,
    ) -> None:
        super().__init__()

        self.ref_geo = ref_geo
        self._options = ConfDiffOptions(
            rmsd_threshold=rmsd_threshold,
            rot_threshold=rot_threshold,
            energy_threshold=inf,
            mass_weighted=True,
            rigid_rotation=True,
            permute=True,
        )

    def eval(self, db, geo_ids, id):
        keep = []

        for geo_id in geo_ids:
            geo = db.load_geometry(geo_id)

            if not ConformerEnsemble.is_different_conformer(
                self.ref_geo,
                0.0,
                geo,
                0.0,
                self._options,
            ):
                keep.append(geo_id)

        return keep

class RMSDCriterion(GeometryCriterion):
    """checks if the RMSD of two geometries are close within a certain
    tolerance

    see :class:`chemtrayzer.core.coords.Geometry`.rmsd() for more

    :param tol: absolute tolerance fro MOIs
    """

    def __init__(
        self,
        ref_geo: Geometry,
        tol: float,
        check_permutations=False,
        mass_weighted=False,
        rigid_rotations=False,
        center_of_mass=False,
    ) -> None:
        super().__init__()
        self._tol = tol
        self._ref_geo = ref_geo
        self._check_permutations = check_permutations
        self._mass_weighted = mass_weighted
        self._rigid_rot = rigid_rotations
        self._COM = center_of_mass

    def eval(
        self, db: GeometryDatabase, geo_ids: Iterable[GeoId], id: str
    ) -> Iterable[GeoId]:
        keep = []

        for geo_id in geo_ids:
            try:
                if (
                    db.load_geometry(geo_id).rmsd(
                        self._ref_geo,
                        mass_weighted=self._mass_weighted,
                        permute=self._check_permutations,
                        rigid_rotation=self._rigid_rot,
                        center_of_mass=self._COM,
                    )
                    < self._tol
                ):
                    keep.append(geo_id)
            # rmsd may throw a value error, if the order of the elements does
            # not match. We'll just ignore it here
            except ValueError:
                continue

        return keep


class OptimizedAt(GeometryCriterion):
    """checks if a geometry was optimized at a certain level of theory"""

    def __init__(self, lot: LevelOfTheory) -> None:
        super().__init__()
        self._lot = lot

    def eval(
        self, db: GeometryDatabase, geo_ids: Iterable[GeoId], id: str
    ) -> Iterable[GeoId]:
        selected_ids = []

        for geo_id in geo_ids:
            cur = db._con.execute(
                'SELECT json AS "lot [LevelOfTheory]" FROM '
                "levels_of_theory INNER JOIN geometries ON "
                "levels_of_theory.level_of_theory = geometries.level_of_theory "
                "WHERE geometry_id=(?)",
                (geo_id,),
            )
            lots = cur.fetchall()
            cur.close()

            # fetchall returns a list of tuples, whith only one element in each
            # tuple
            if (self._lot,) in lots:
                selected_ids.append(geo_id)

        return selected_ids


class IsTransitionState(GeometryCriterion):
    """checks if a geometry belongs to a transition sate"""

    def eval(
        self, db: GeometryDatabase, geo_ids: Iterable[GeoId], id: str
    ) -> Iterable[GeoId]:
        # check if database has a transition state table
        if isinstance(db, ReactionDB):
            TS_ids = db.list_TS_geometries(id)
            return set(geo_ids) & set(TS_ids)
        else:
            return []


class IsIRCEndpoint(GeometryCriterion):
    """cheks if the geometry is an IRC endpoint"""

    def eval(
        self, db: GeometryDatabase, geo_ids: Iterable[GeoId], id: str
    ) -> Iterable[GeoId]:
        # check if database has a transition state table
        if isinstance(db, ReactionDB):
            IRC_endpoints = db.list_IRC_endpoints(id)
            # transform list of tuples into flat list
            IRC_endpoints = itertools.chain(*IRC_endpoints)

            return set(geo_ids) & set(IRC_endpoints)
        else:
            return []


class OnlyLowestEnergy(GeometryCriterion):
    """only the geometry with the lowest electronic energy is returned. If there
    is no electronic energy stored for one of the geometries at the specified
    level of theory, it is ignored.

    .. note:: It is important that this criterion is evaluated last. If you want to chain multiple criteria use the ``>>`` operator. For example ``(OptimizedAt(lot)  & IsTransitionState()) >> OnlyLowestEnergy()`` returns the transition state geometry with the lowest energy, that was optimized at level of theory ``lot``.

    :param lot: level of theory at which electronic energy is computed"""

    def __init__(self, lot: LevelOfTheory) -> None:
        super().__init__()

        self.lot = lot

    def eval(
        self, db: GeometryDatabase, geo_ids: Iterable[GeoId], id: str
    ) -> Iterable[GeoId]:
        lowest_energy = inf
        geo_id_lowest = None

        for geo_id in geo_ids:
            energy = db.load_electronic_energy(geo_id, self.lot)

            if energy is not None:
                if energy < lowest_energy:
                    lowest_energy = energy
                    geo_id_lowest = geo_id

        if geo_id_lowest is not None:
            return [geo_id_lowest]
        else:
            return []


# enable the sqlite module to store pickable python objects by using Python's
# built-in converter/adapter functionality:
def _adapt_pyobj(obj):
    return pickle.dumps(obj)


def _convert_pyobj(binary_data):
    return pickle.loads(binary_data)


def _adapt_json_convertible(obj: IJsonConvertible):
    """generates a binary string with a json representation of obj"""
    # wrap everythign in try-except block and log errors, because the sqlite3
    # module does not pass along the errors which makes it harder to debug
    try:
        return bytes(obj.to_json(), encoding="utf-8")
    except Exception as e:
        logging.error(f"Exception occured in _adapt_json_convertible(): {e}")
        # reraise exception
        raise


def _convert_json_convertible(cls: Type[IJsonConvertible], json_str: bytes):
    """creates an object of type cls from json_str"""
    # wrap everythign in try-except block and log errors, because the sqlite3
    # module does not pass along the errors which makes it harder to debug
    try:
        # set this to false to suppress warning that is otherwise triggered
        BasisSet._warn_on_creation = False
        json_str = str(json_str, encoding="utf-8")

        return cls.from_json(json_str)
    except Exception as e:
        logging.error(f"Exception occured in _convert_lot(): {e}")
        # reraise exception
        raise
    finally:
        BasisSet._warn_on_creation = True


def _convert_lot(lot_str: bytes) -> LevelOfTheory:
    return _convert_json_convertible(LevelOfTheory, lot_str)


# Register the adapter and converter
sqlite3.register_adapter(np.ndarray, _adapt_pyobj)
sqlite3.register_adapter(Geometry, _adapt_pyobj)
sqlite3.register_adapter(LevelOfTheory, _adapt_json_convertible)
sqlite3.register_adapter(Species, _adapt_pyobj)
sqlite3.register_adapter(Reaction, _adapt_pyobj)

# the converters are chosen based on the column name
sqlite3.register_converter("geometries", _convert_pyobj)
sqlite3.register_converter("np.ndarray", _convert_pyobj)
sqlite3.register_converter("LevelOfTheory", _convert_lot)
sqlite3.register_converter("Species", _convert_pyobj)
sqlite3.register_converter("Reaction", _convert_pyobj)
