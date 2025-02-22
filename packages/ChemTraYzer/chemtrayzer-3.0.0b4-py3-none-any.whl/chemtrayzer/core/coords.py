"""Molecular coordinates

This module contains classes for representing molecular systems and their
evolution as atomic coordinates.
"""

from __future__ import annotations

import operator
import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from io import TextIOWrapper
from itertools import chain, repeat
from numbers import Number
from os import PathLike
from typing import (
    Any,
    Literal,
    Optional,
    Union,
    overload,
)

# type: ignore
import numpy as np
import rdkit  # type: ignore
import scipy  # type: ignore
from rdkit import Chem  # type: ignore
from rdkit.Chem import (
    AllChem,  # type: ignore
    rdDistGeom,  # type: ignore
)
from scipy.constants import physical_constants
from typing_extensions import Self

from chemtrayzer.core.constants import h_bar, k_B, amu, E_h
from chemtrayzer.core.periodic_table import PERIODIC_TABLE as PTOE
from chemtrayzer.core.periodic_table import Element


def wrap_coords(
    coords: np.ndarray,
    box_size: tuple[float, float, float],
    pbc: tuple[bool, bool, bool] = (True, True, True),
    copy: bool = True,
) -> np.ndarray:
    """wrap coordinates with periodic boundary conditions into the box

    Values on the upper boundary will be wrapped to the lower boundary. Values
    on the lower boundary are preserved, i.e. the box interval is [-L/2, L/2)

    :param coords: N x 3 or M1 x ... x Md x N x 3 array where N is the
                   number of atoms, 3 are the x, y, and z coordinates, and
                   M1 - Md can be an arbitrary number of dimensions with
                   arbitrary size,
    :param box_size: tuple of the box size in x, y, and z direction (entries
                     where pbc is False are ignored)
    :param pbc: tuple of the periodic boundary conditions in x, y, and z
                direction; coordinates along non-PBC directions are not changed
    :param copy: whether to copy the input array or modify it in place (if the
                 input array is not a numpy array it will always be copied)
    :return: wrapped coordinates in array of same dimensions as input
    """
    coords = np.array(coords, copy=copy)
    _box_size: np.ndarray = np.array(box_size)  # make numpy array for
    # indexing
    i = np.nonzero(pbc)  # indices with periodic boundary conditions

    # move half a box size, b/c modulo wraps at the full box size, but the box
    # is centered at zero (we want to actually wrap at +-box_size/2)
    positive_shift = coords[..., i] + _box_size[i] / 2

    # Apply wrapping and then shift back
    coords[..., i] = (positive_shift % (_box_size[i])) - _box_size[i] / 2

    return coords


def calc_distance_matrix(
    coords,
    box_size: tuple[float, float, float] = (0, 0, 0),
    periodic: str = "xyz",
) -> np.ndarray:
    """
    calculates atom pairwise atom distances for large (periodic) system
    :param coords: cartesian coordinates of atoms
    :type coords: np.ndarray
    :param box_size: size of simulation box as tuple (x,y,z)
    :type box_size: tuple(float, float, float)
    :param periodic: string with periodicity definition 'xyz','xy','xz',
                    'yz','x','y','z', optional
    :type periodic: str
    :returns: distance matrix and the metric dist(u=X[i], v=X[j])
    """

    period_dim = (
        set()
        if not periodic
        else {{"x": 0, "y": 1, "z": 2}[d] for d in periodic}
    )
    not_period_dim = {0, 1, 2} - period_dim
    n_atoms = np.shape(coords)[0]
    # to match the output of pdist
    dist_nd_sq = np.zeros(n_atoms * (n_atoms - 1) // 2)

    for d in period_dim:
        pos_1d = coords[:, d][:, np.newaxis]  # shape (N, 1)
        dist_1d = scipy.spatial.distance.pdist(pos_1d)  # shape (N *(N-1)//2, )
        dist_1d[dist_1d > box_size[d] * 0.5] -= box_size[d]
        dist_nd_sq += np.square(dist_1d)  # d^2 = dx^2 + dy^2 + dz^2
    for d in not_period_dim:
        pos_1d = coords[:, d][:, np.newaxis]  # shape (N, 1)
        dist_1d = scipy.spatial.distance.pdist(pos_1d)  # shape (N*(N-1)//2, )
        dist_nd_sq += np.square(dist_1d)  # dx^2
    condensed_distance_matrix = np.sqrt(dist_nd_sq)  # =sqrt(dx^2 + dy^2 +dz^2)
    distance_matrix = scipy.spatial.distance.squareform(
        condensed_distance_matrix
    )
    return distance_matrix


class InvalidXYZFileError(Exception):
    """Thrown when trying to read an xyz file with an unsupported format"""


class Geometry:
    """
    Represents a molecular geometry, i.e. the coordinates and type of one or
    more atoms.

    Equality for geometries is determined based on the atom types and
    coordinates.
    To check if two geometries are similar, use rmsd()

    Note: The hash function and == operator are not safe to use accross
    different maschines, because the endianess of the data is ignored.

    :param atom_types: list of strings containing symbol for each atom
    :type atom_types: Iterable[Element]
    :param coords: nAtomsx3 numpy array with cartesian coordinates
    :type coords: np.array
    """

    coords: np.ndarray
    atom_types: tuple[Element, ...]

    def __init__(
        self,
        atom_types: Iterable[str | int | Element] = None,
        coords: np.ndarray = None,
    ):
        if atom_types is not None and coords is not None:
            self.atom_types = tuple([PTOE[type] for type in atom_types])
            self._check_coords_shape(coords)
            self.coords = np.array(coords)
            if self.n_atoms != np.shape(self.coords)[0]:
                raise ValueError(
                    "Number of atoms and coordinates do not match"
                )
        else:
            self.coords = np.empty(shape=[0, 3])
            self.atom_types = tuple()

    @staticmethod
    def _check_coords_shape(coords) -> None:
        for atom_coord in coords:
            if len(atom_coord) != 3:
                raise ValueError("wrong cartesian coordinates input")
            for i in atom_coord:
                if not isinstance(i, Number):
                    raise ValueError(f"{i} wrong cartesian coordinates input")

    @property
    def n_atoms(self) -> int:
        return len(self.atom_types)

    def __len__(self) -> int:
        return self.n_atoms

    def xyz_str(self, comment: Optional[str] = None) -> str:
        """
        returns the xyz representation of this geometry as a string

        :param comment: comment for 2nd line of xyz file
        :return: xyz representation of this geometry
        """
        xyz = str(self.n_atoms) + "\n"
        if comment is not None:
            xyz += comment + "\n"
        else:
            xyz += "\n"

        for type, coords in zip(self.atom_types, self.coords):
            xyz += (
                f"{type.symbol:s} {coords[0]:.8f} {coords[1]:.8f} "
                f"{coords[2]:.8f}\n"
            )

        return xyz

    def to_xyz(
        self,
        path: PathLike,
        comment: Optional[str] = None,
        overwrite: bool = False,
    ) -> None:
        """
        Writes coordinates into an xyz file.

        :param path: path-like object that points to the xyz file
        :param comment: comment for 2nd line of xyz file
        :param overwrite: if True, replaces file contents, otherwise appends
        """
        mode = "w" if overwrite else "a"
        with open(path, mode, encoding="utf-8") as file:
            file.write(str(self.n_atoms) + "\n")
            if comment is not None:
                file.write(comment + "\n")
            else:
                file.write("\n")
            for type, coords in zip(self.atom_types, self.coords):
                file.write(
                    f"{type:s} {coords[0]:.8f} {coords[1]:.8f} "
                    f"{coords[2]:.8f}\n"
                )

    @overload
    @classmethod
    def from_xyz_file(
        cls, path: PathLike, comment: Literal[False]
    ) -> Geometry: ...

    @overload
    @classmethod
    def from_xyz_file(
        cls, path: PathLike, comment: Literal[True]
    ) -> tuple[Geometry, str]: ...

    @classmethod
    def from_xyz_file(
        cls, path: PathLike, comment: bool = False
    ) -> Geometry | tuple[Geometry, str]:
        """
        Creates a Geometry object from an xyz file

        returns: (obj : Geometry, comment : str)
        """

        with open(path, "r", encoding="utf-8") as xyz_file:
            return cls._from_opened_xyz_file(xyz_file, comment=comment)

    @overload
    @classmethod
    def _from_opened_xyz_file(
        cls, file: TextIOWrapper, comment: Literal[False]
    ) -> Geometry: ...

    @overload
    @classmethod
    def _from_opened_xyz_file(
        cls, file: TextIOWrapper, comment: Literal[True]
    ) -> tuple[Geometry, str]: ...

    @overload
    @classmethod
    def _from_opened_xyz_file(
        cls, file: TextIOWrapper, comment: bool = False
    ) -> Geometry | tuple[Geometry, str]: ...

    @classmethod
    def _from_opened_xyz_file(
        cls,
        file: TextIOWrapper,
        comment: bool = False,
        ignore_additional_lines: bool = False,
    ) -> Geometry | tuple[Geometry, str]:
        """
        reads n_atoms atoms from file and creates Geometry object

        :param file: xyz file object where the pointer sits on the first line
        of the xyz section, i.e. the line with the number of atoms
        :return: Geometry object and comment section of xyz section
        """
        try:
            n_atoms = int(file.readline())  # 1st line contains num of atoms
        except ValueError as e:
            raise InvalidXYZFileError("First line not an integer.") from e

        comment_str = file.readline().strip()  # second line is comment

        atom_types = []
        coordinates = np.zeros((n_atoms, 3))
        n_atoms_read = 0
        line_operator = operator.lt if ignore_additional_lines else operator.ne
        # use this construct instead of `for line in file` such that tell() is
        # not disabled as it is being used in `multiple_from_xyz`
        line = file.readline()
        while line:
            words = line.split()

            if words == []:  # terminate by empty line
                break

            atom_types.append(words[0])  # first word in line is atom name

            # next three words contain coordinates
            try:
                coordinates[n_atoms_read, :] = np.array(words[1:4])
            except ValueError as e:
                raise InvalidXYZFileError() from e

            # if more than 4 lines are given, the remaining are ignored.
            if line_operator(len(words), 4):
                raise InvalidXYZFileError("Unexpected number of columns.")

            # only read as many lines as specified
            n_atoms_read += 1
            if n_atoms_read >= n_atoms:
                break

            line = file.readline()

        if n_atoms_read != n_atoms:
            raise InvalidXYZFileError("Fewer atoms than specified.")
        if comment is True:
            return cls(atom_types, coordinates), comment_str
        elif comment is False:
            return cls(atom_types, coordinates)
        else:
            raise ValueError(
                f"comment is set to {type(comment)}: "
                f"{comment} and should be a bool"
            )

    @overload
    @classmethod
    def multiple_from_xyz_file(
        cls, path: PathLike, comment: Literal[False], max=np.inf
    ) -> list[Geometry]: ...

    @overload
    @classmethod
    def multiple_from_xyz_file(
        cls, path: PathLike, comment: Literal[True], max=np.inf
    ) -> tuple[list[Geometry], list[str]]: ...

    @classmethod
    def multiple_from_xyz_file(
        cls,
        path: PathLike,
        comment: bool = False,
        max=np.inf,
    ) -> list[Geometry] | tuple[list[Geometry], list[str]]:
        """
        Creates several Geometry objects from a single xyz file which contains
        several sections each formatted like an xyz file (i.e. beginning with
        the number of atoms and a comment). This can be used to quickly read in
        CREST output.

        :param path: path to xyz file
        :param max: maximum number of objects that should be read/created
        :param returns: objs : list(Geometry), comments : list(str)
        :param comment: if True, the comment section of each xyz section is
                        included, default: False
        """

        with open(path, "r", encoding="utf-8") as xyz_file:
            geos: list[Geometry] = []
            comments: list[str] = []
            while len(geos) <= max:
                geo, comment_str = cls._from_opened_xyz_file(
                    xyz_file, comment=True
                )
                comments.append(comment_str)
                geos.append(geo)

                # peek ahead to check for empty lines
                pos = xyz_file.tell()
                if xyz_file.readline().strip() == "":
                    break
                xyz_file.seek(pos)
        if comment is True:
            return geos, comments
        elif comment is False:
            return geos
        else:
            raise ValueError(
                f"comment is set to {type(comment)}: {comment}"
                " and should be a bool"
            )

    @classmethod
    def from_inchi(cls, inchi: str) -> Geometry:
        """
        generate a geometry from an InChI. Results may vary.

        :param inchi: InChI
        :return: generated geometry
        """
        from chemtrayzer.core.chemid import _rdkit_mol_from_inchi

        mol = _rdkit_mol_from_inchi(inchi)

        return cls._from_rdkit_mol(mol)

    @classmethod
    def _from_rdkit_mol(cls, mol: rdkit.Chem.Mol, seed=42) -> Geometry:
        """This method is private because the dependency on RDKit should not
        be public
        """
        ce = ConformerEnsemble.from_rdmol(mol, n_confs=1, opt="uff", seed=seed)

        return ce.geos[0]

    def to_sdf(
        self,
        path,
        name: str,
        comment: Optional[str] = None,
        append: bool = True,
        associated_data: Optional[dict[str, str]] = None,
    ) -> None:
        """
        Creates an SDF file for this geometry.

        :param path: path where the SDF file should be created
        :param name: name of this geometry in the header block of the molfile
        :param comment: comment for this geometry in the header block
        :param append: if true and an SDF file already exists at path, this
                       geometry will be added to the end of the file
        :param associated_data: data that should be added to the data part of
                                the SDF file.
        """
        from chemtrayzer.core.chemid import _rdkit_mol_from_geometry

        rdkitmol = _rdkit_mol_from_geometry(self)

        mol_block = Chem.MolToMolBlock(
            rdkitmol, includeStereo=False, kekulize=False
        )
        lines: list[str] = mol_block.splitlines()

        # check if name, comment & data are in agreement with SD file standard
        if comment is None:
            comment = ""
        else:
            if "\n" in comment:
                raise ValueError("No new lines allowed in comment")
            if "$$$$" in comment:
                raise ValueError(
                    'SD file record separator "$$$$" not allowed in comment.'
                )
            if "$$$$" in name:
                raise ValueError(
                    'SD file record separator "$$$$" not allowed in name.'
                )

        if associated_data is not None:
            for field_name, data in associated_data.items():
                if not re.match("^[A-Za-z][A-Za-z0-9_]+$", field_name):
                    raise ValueError(
                        f'Invalid field name "{field_name}":\nField '
                        "names must begin with an alphabetic character which"
                        " can be followed by alphanumeric characters and"
                        " underscores"
                    )

                for line in data.splitlines():
                    reason = None
                    if line.startswith("$$$$"):
                        reason = (
                            "Lines cannot start with SD file record "
                            'separator "$$$$".'
                        )
                    elif len(line) > 200:
                        reason = "Lines can contain only up to 200 characters."
                    elif line.strip() == "":
                        # blank lines terminate the data entry
                        reason = "Data cannot contain blank lines."
                    if reason is not None:
                        raise ValueError(
                            f'Illegal data for field "{field_name}":\n{reason}'
                        )

            for field_name, data in associated_data.items():
                lines.append(f"> <{field_name}>")
                # remove possible leading and trailing new lines
                lines.append(data.strip())
                lines.append("")  # data entries are terminated by blank lines
        # add seperator
        lines.append("$$$$")

        # first line is the title, third one is the comment
        lines[0] = name
        lines[2] = comment

        mode = "a" if append else "x"

        with open(path, mode, encoding="utf-8") as file:
            # if the file is not empty we need to add a new line before adding
            # the content
            if append and file.tell() != 0:
                file.write("\n")

            file.write("\n".join(lines))

    @property
    def molecular_weight(self) -> float:
        """molecular weight of this geometry in amu"""
        mw = 0.0

        for elem in self.atom_types:
            mw += elem.mass

        return mw

    def split_fragments(self) -> list[Geometry]:
        from chemtrayzer.core.chemid import _rdkit_mol_from_geometry

        mol = _rdkit_mol_from_geometry(self)

        fragments = []

        for fragment in Chem.GetMolFrags(mol):
            atom_ids = [atom for atom in fragment]

            atom_types = [self.atom_types[atom_id] for atom_id in atom_ids]

            coords = [self.coords[atom_id] for atom_id in atom_ids]

            fragments.append(Geometry(atom_types, coords))

        return fragments

    def __hash__(self) -> int:
        return hash(self.coords.tobytes()) ^ hash(self.atom_types)

    def __eq__(self, __o: object) -> bool:
        return hash(self) == hash(__o) and type(__o) is __class__

    def align(
        self,
        other: Geometry,
        mass_weighted=False,
        align_atoms: Optional[Iterable[int]] = None,
    ) -> Self:
        """Aligns the geometry to another geometry by translating and rotating
        it.
        Operation is done in place.
        Atoms have to be in the same order in both geometries!

        :param other: Geometry the structure should be aligned to
        :type other: Geometry
        :param mass_weighted: if True,  with mass weighting
        :param align_atoms: list of atom indices that should be aligned by
                            rotation. If None, all atoms are used.
                            Useful to align not active atoms in reactions.
                            Default: None
        :type align_atoms: Iterable[int]
        """
        self.coords -= self.center_of_mass()
        self.coords += other.center_of_mass()

        weights = np.array(
            [el.mass if mass_weighted else 1 for el in self.atom_types]
        )
        if align_atoms is not None:
            for atom in align_atoms:
                weights[atom] = 0

        rot_mat, _rmsd = scipy.spatial.transform.Rotation.align_vectors(
            other.coords, self.coords, weights=weights
        )
        self.coords = rot_mat.apply(self.coords)

        return self

    def rmsd(
        self,
        other: Geometry,
        mass_weighted: bool = False,
        rigid_rotation: bool = False,
        center_of_mass: bool = False,
        permute: bool | Iterable[dict[int, int]] = False,
    ) -> float:
        """computes the root-mean-square distance to another geometry

        :param mass_weighted: if true, each coordinate is weighted by its
                              atomic mass instead of one
        :type mass_weighted: bool
        :param rigid_rotation: uses the Kabsh algorithm to align the two
                            geometries to get the minimal RMSD w.r.t. rotation
        :type rigid_rotation: bool
        :param center_of_mass: move the centers of mass of one geometry on the
                               the other before comparing
        :type center_of_mass: bool
        :param permute: If False, nothing is done.
                        Otherwise, the minimal RMSD over all considered
                        permutations of atom ids is used.
                        If True, all isomorphic atom id mappings of the
                        molecular graph are generated.
                        If an iterable of atom-id to atom-id mappings is given,
                        those are considered as permutations. Here, the key is
                        the atom-id in the permutation and the value is the
                        current atom-id.
        :return: RMSD
        :rtype: float
        """

        if not self.n_atoms == other.n_atoms:
            raise ValueError("The number of atoms must be equal.")

        if permute is False:
            if not all(
                [
                    self_t == other_t
                    for self_t, other_t in zip(
                        self.atom_types, other.atom_types
                    )
                ]
            ):
                raise ValueError("Atoms must be of the same type.")

        elif permute and permute is True:
            from chemtrayzer.core.graph import MolGraph

            self_graph = MolGraph.from_geometry(geo=self)
            other_graph = MolGraph.from_geometry(geo=other)
            permute = tuple(self_graph.get_isomorphic_mappings(other_graph))

        if permute and all(isinstance(perm, dict) for perm in permute):
            rmsd_list = []
            for mapping in permute:
                mapped_atom_types = [
                    other.atom_types[mapping[i]] for i in range(self.n_atoms)
                ]
                mapped_coords = np.array(
                    [other.coords[mapping[i]] for i in range(self.n_atoms)]
                )
                mapped_other = Geometry(mapped_atom_types, mapped_coords)

                rmsd_list.append(
                    self.rmsd(
                        mapped_other,
                        mass_weighted=mass_weighted,
                        rigid_rotation=rigid_rotation,
                        center_of_mass=center_of_mass,
                        permute=False,
                    )
                )
            if len(rmsd_list) == 0:
                raise ValueError("No isomorphic mapping found.")
            return min(rmsd_list)

        # rotated or translated coordinates are copied into this variable,
        # if requested
        other_coords = other.coords
        self_coords = self.coords

        if center_of_mass:
            other_coords = other_coords - other.center_of_mass()
            self_coords = self_coords - self.center_of_mass()

        masses = np.array(
            [el.mass if mass_weighted else 1 for el in self.atom_types]
        )

        if rigid_rotation:
            _, rmsd = scipy.spatial.transform.Rotation.align_vectors(
                self_coords, other_coords, weights=masses
            )
        else:
            M = np.sum(masses)
            rmsd = np.sqrt(
                1
                / M
                * np.sum(
                    np.sum((self_coords - other_coords) ** 2, axis=1) * masses
                )
            )

        return rmsd

    def moment_of_inertia(self) -> tuple[np.ndarray, np.ndarray]:
        """Computes the inertia tensor w.r.t. the geometries center of mass and
        returns its eigenvalues and the principal axes

        .. note::
            This method assumes that the unit of length for this object is
            Angstrom!

        :return: eigenvalues in ascending order in atomic
                 units [a_0^2 amu] and a 3x3 matrix where each column contains
                 a principal axis
        """
        masses = np.array([el.mass for el in self.atom_types])

        centered = self.coords - self.center_of_mass()
        # convert to Bohr radii
        a_0 = 1.88972612463  # [Angstrom]
        centered *= a_0

        # move origin to center of mass and mass weight the coordinates
        mass_weighted_coords = centered * np.sqrt(masses[:, np.newaxis])

        # construct moment of inertia tensor
        # after this element x,y of this matrix contains -\sum_i^N m_i x_i y_i
        # meaning that the off-diagonal entries are correct
        I = -mass_weighted_coords.T @ mass_weighted_coords  # noqa: E741

        # extract \sum_i^N m_i x_i^2   (same with y and z)
        mx2 = -I[0, 0]
        my2 = -I[1, 1]
        mz2 = -I[2, 2]

        # fill diagonal elements
        I[0, 0] = my2 + mz2
        I[1, 1] = mx2 + mz2
        I[2, 2] = mx2 + my2

        return np.linalg.eigh(I)  # eigenvalues, principal axis

    def rotational_constants(self) -> tuple[float, float, float]:
        r"""Rotational constant

        .. note::

            There are different ways to define the rotational constant in
            literature, e.g. as wavenumber, frequency or energy. Here, we
            express it as energy.


        :return: :math:`\frac{\bar h^2}{2 \text{MOI}}` where MOI are the
                 principal moments of inertia [Hartree]
        """
        return (h_bar**2) / (2 * self.moment_of_inertia()[0] * 1e-20*amu) / E_h

    def center_of_mass(self) -> np.ndarray:
        """returns the center of mass of the cartesian coordinates"""
        masses = np.array([atom.mass for atom in self.atom_types])

        return np.average(self.coords, axis=0, weights=masses)

    def wrap(
        self,
        box_size: tuple[float, float, float],
        pbc: tuple[bool, bool, bool] = (True, True, True),
    ) -> np.ndarray:
        """Apply periodic boundary conditions

        Shift all atoms into the defined box with the center 0, 0, 0
        :param box_size: tuple of the box size in x, y, and z direction
                         (entries where pbc is False are ignored)
        :param pbc: tuple of the periodic boundary conditions in x, y, and z
                    direction; coordinates along non-PBC directions are not
                    changed
        :return: self.coords (after wrapping)
        """
        self.coords = wrap_coords(self.coords, box_size, pbc, copy=False)

        return self.coords

    def unbreak_molecule(
        self,
        box_size: tuple[float, float, float],
        periodic_boundary_conditions: tuple[bool, bool, bool] = (
            True,
            True,
            True,
        ),
        zero_com=False,
    ) -> np.ndarray:
        """
        Wrap back parts of the Geometry which have been split off due to
        periodic boundary conditions.
        This is mandatory to start a COM calculation or an optimization in
        another program.

        Set zero_com to True to center the Geometry around the center of mass.
        E.g.: [o  oO] --> oO[o    ] --> oO-o

        :param box_size: size of orthogonal simulation box as tuple (x,y,z)
        :param periodic_boundary_conditions: flags boundary condiditons as
                                             periodic or infinite
        :param zero_com: centers the atoms around their COM
        :returns: the final n_atoms x 3 displacement vector
        """
        orig = self.coords.copy()

        # do per dimension i
        for i in [0, 1, 2]:
            if not periodic_boundary_conditions[i]:
                continue

            # box length + coordinates
            bl = box_size[i]
            x = self.coords[:, i]
            # sort by value
            xs = np.sort(x)

            # find all gaps between atoms along dimension i
            dx = np.diff(xs, append=xs[0] + bl)
            # [o  oO]  atom coord left of biggest gap
            #  ^
            z = xs[np.argmax(dx)]
            # shift all atoms which are right of the gap back one box length
            # oO[o    ]
            #  <-----|
            x[x > z] -= bl

        if zero_com:
            #  [ oO-o ]  shift all atoms towards the origin
            # |--->
            self.coords -= self.center_of_mass()

        # return the displacment after-before
        return self.coords - orig

    def distance_matrix(
        self,
        box_size: tuple[float, float, float] = (0, 0, 0),
        periodic: str = "xyz",
    ) -> np.ndarray:
        """
        calculates atom pairwise atom distances for large (periodic) system

        :param box_size: size of simulation box as touple (x,y,z)
        :type box_size: tuple(float, float, float)
        :param periodic: string with periodicity definition 'xyz','xy','xz',
                         'yz','x','y','z', optional
        :type periodic: str
        :returns: distance matrix and the metric dist(u=X[i], v=X[j])
        """

        return calc_distance_matrix(self.coords, box_size, periodic)


class TSGeometry(Geometry):
    """
    Represents the geometry of a transition state and contains additional
    information like the active atoms

    :param atom_types: list of strings containing symbol for each atom
    :type atom_types: Iterable[Element]
    :param coords: nAtomsx3 numpy array with cartesian coordinates
    :type coords: np.array
    :param multiplicity: spin multiplicity
    :type multiplicity: float, optional
    :param active: list of zero-based ids of active (in the reaction) atoms
    """

    def __init__(
        self,
        atom_types: Iterable[str | int | Element],
        coords: np.ndarray,
        multiplicity: Optional[float] = None,
        active: Optional[Iterable[int]] = None,
    ):
        super().__init__(atom_types, coords)

        if active is not None:
            self.active = tuple(active)
        else:
            self.active = tuple()

    def __hash__(self) -> int:
        return (
            hash(self.coords.tobytes())
            ^ hash(self.atom_types)
            ^ hash(self.active)
        )

    def __eq__(self, __o: object) -> bool:
        return hash(self) == hash(__o) and type(__o) is __class__

    @classmethod
    def from_geometry(cls, geo: Geometry, active: Optional[list] = None):
        """
        translates a Geometry into a TSGeometry by adding active atoms

        :param geo: Geometry
        :param active: list of IDs of active atoms in the geometry (start at 1)
        :return: TSGeometry object
        """
        return cls(
            [t.atomic_nr for t in geo.atom_types], geo.coords, active=active
        )

@dataclass
class ConfDiffOptions:
    """Thresholds for determining if two conformers are different.
    """
    # distinguishing conformers
    energy_threshold: float = 0.00038
    """Energy threshold used for filtering. Default value coressponds to
    about 1 kJ/mol [Hartree]
    """
    rmsd_threshold: float = 0.125
    """RMSD threshold for distinguing conformers. [Angstrom]"""
    rot_threshold: float = 1
    """Rotational constant threshold for distinguing conformers. [percent]"""

    # rmsd parameters
    mass_weighted: bool = True
    """If True, mass weighted RMSD is used."""
    rigid_rotation: bool = True
    """If True, rigid rotation is used for RMSD calculation."""
    permute: bool | Iterable[dict[int, int]] = False
    """If True, all isomorphic mappings are considered for RMSD calculation.
    If an iterable of atom-id to atom-id mappings is given, those are
    considered as permutations. Here, the key is the atom-id in the
    permutation and the value is the current atom-id.
    """

@dataclass
class ConfFilterOptions(ConfDiffOptions):
    """
    Contains the filtering options for conformer ensembles.
    """

    # filtering unrelevant conformers
    temperature: float = 1500
    """Temperature [K] used for Boltzmann weighting. The higher the
    temperature, the more conformers are retained.
    """
    cum_boltzmann_threshold: float = 1
    """Threshold for cumulative Boltzmann weights.

    Retains the lowest energy conformers such that the sum of their
    Boltzmann weights is just greater than or equal to this threshold.
    The last conformer included is the one that causes the threshold
    to be reached/exceeded. By default, all conformers are retained.
    """
    energy_window: float = np.inf
    """Energy window [Hartree] used for filtering conformers.
    Conformers with energies >= E_min + energy_window are filtered out after
    the Boltzmann-weighted filtering.

    By default, no energy window is used.
    """



@dataclass
class ConformerEnsemble(Sequence[tuple[Geometry, float]]):
    """
    Represents Conformer ensembles. The ensemble is always sorted by energy.
    Filtering of Conformers is implemented according this paper (check
    Figure 3): https://doi.org/10.1039/C9CP06869D


    :param geos: list of conformer geometries
    :param energies: list of conformer energies [Hartree]
    """

    geos: list[Geometry] = field(default_factory=list)
    energies: list[float] = field(default_factory=list)  # in Hartree
    filter_opts: ConfFilterOptions|None = field(init=False)
    """Filter options used for filtering the conformers. Set by `filter()`
    """

    def __post_init__(self):
        if len(self.geos) != len(self.energies):
            raise ValueError("Length of geos and energies must be equal.")
        if any(geo.atom_types != self.geos[0].atom_types for geo in self.geos):
            raise ValueError("All geometries must have the same atom types.")

    def __getitem__(self, id: int) -> tuple[Geometry, float]:
        return self.geos[id], self.energies[id]

    def add_geometry(
        self,
        geo: Geometry,
        energy: float = 0,
    ) -> None:
        """Adds a new conformer to the ensemble."""
        self.geos.append(geo)
        self.energies.append(energy)

    @overload
    def get_boltzmann_weight(
        self, i: int, *, temperature: float
    ) -> float: ...

    @overload
    def get_boltzmann_weight(
        self, i: np.ndarray[np.int] | slice, *, temperature: float
    ) -> np.ndarray: ...

    def get_boltzmann_weight(self, i, *, temperature: float = 293):
        """
        Returns the Boltzmann weight of the conformer at the given temperature.
        If no temperature is given, the temperature of the ensemble is used.

        :param id: id(s) of the geometries for which to compute the
                   boltzmann_weight(s)
        :param temperature: temperature [K]
        :return: boltzman weight(s) of requested geometries
        """
        energies = np.array(self.energies, dtype=float)
        energies -= np.min(energies)  # substract lowest energy to avoid
        # division by zero (substraction of
        # constant min. energy cancels out)
        energies *= physical_constants["Hartree energy"][0]  # Hartree -> J

        boltz_factors = np.exp(-energies / (k_B * temperature))
        return boltz_factors[i] / np.sum(boltz_factors)

    def sort(self, descending: bool = True) -> None:
        """Sorts the conformers by energy 'inplace'.

        :param descending: if True, sort in descending order,
                           if False ascending
        """
        self.energies, self.geos = zip(
            *sorted(zip(self.energies, self.geos),
                    key=lambda x: x[0],
                    reverse=descending)
        )

    @staticmethod
    def is_different_conformer(
        geo: Geometry,
        energy: float,
        other_geo: Geometry,
        other_energy: float,
        opts: ConfDiffOptions,
    ) -> bool:
        """
        Determines if the two geometries are similar enough to be considered
        the same conformer.
        Determined by RMSD, energy and rotational constant threshold.
        """

        c_rot = np.array(geo.rotational_constants())
        other_c_rot = np.array(other_geo.rotational_constants())

        # use element-wise minimum to make this function symmetric, i.e.,
        # it should not matter, if geo and other_geo are switched
        rot_diff_percent = (np.abs(c_rot - other_c_rot)
                            / np.minimum(c_rot, other_c_rot)
                            * 100)

        return (
            geo.rmsd(
                other_geo,
                mass_weighted=opts.mass_weighted,
                rigid_rotation=opts.rigid_rotation,
                permute=opts.permute,
            )
            > opts.rmsd_threshold
            or all(rot_diff_percent > opts.rot_threshold)
            or abs(energy - other_energy) > opts.energy_threshold
        )

    def filter(
        self, opts: ConfFilterOptions|None = None, copy: bool = False
    ) -> ConformerEnsemble:
        """
        Removes duplicate and irrelevant conformers. See
        :class:`ConfFilterOptions` for more information. `filter_opts` is set
        to the options used for filtering.

        :param opts: filtering options. If None, default values of
                     :class:`ConfFilterOptions` are used. If `opts.permute` is
                     True, it will be set to all isomorphic mappings of the
                     molecular graph.
        :return: self, if copy = False, or a new ConformerEnsemble object,
                 if copy = True
        """
        if opts is None:
            opts = ConfFilterOptions()

        if opts.permute is True and self.geos:
            from chemtrayzer.core.graph import MolGraph

            opts.permute = tuple(
                MolGraph.from_geometry(
                    self.geos[0]
                ).get_automorphic_mappings()
            )

        new_geos: Iterable[Geometry] = []
        new_energies: Iterable[float] = []

        for geo, energy in zip(self.geos, self.energies):
            if all(
                self.is_different_conformer(
                    geo,
                    energy,
                    new_geo,
                    new_energy,
                    opts,
                )
                for j, (new_geo, new_energy) in enumerate(
                    zip(new_geos, new_energies)
                )
            ):
                new_geos.append(geo)
                new_energies.append(energy)


        if copy is True:
            filtered = self.__class__(
                geos=new_geos,
                energies=new_energies
            )

        else:
            self.geos, self.energies = new_geos, new_energies
            filtered = self

        filtered.filter_opts = opts
        # sorting needed for cumulative Boltzmann weights
        filtered.sort(descending=False)

        # Boltzmann weight filtering
        if opts.cum_boltzmann_threshold < 1:
            bws = filtered.get_boltzmann_weight(
                range(len(filtered)), temperature=opts.temperature
            )
            cum_bws = np.cumsum(bws)  # cumulative Boltzmann weights
            # get index of
            i_bw_cutoff = np.searchsorted(cum_bws,
                                          opts.cum_boltzmann_threshold,
                                          side='right') + 1
        else:
            # if threshold is 1, all conformers are retained -> avoid
            # unnecessary computation and numerical issues by setting
            # i_bw_cutoff to the last index
            i_bw_cutoff = len(filtered)

        # energy window filtering
        e_min = np.min(filtered.energies)
        i_e_cutoff = np.searchsorted(filtered.energies - e_min,
                                     opts.energy_window,
                                     side='right')

        # apply "strongest" filter
        i_cutoff = min(i_bw_cutoff, i_e_cutoff)

        filtered.geos = filtered.geos[:i_cutoff]
        filtered.energies = list(filtered.energies[:i_cutoff])

        return filtered

    @property
    def n_conformers(self) -> int:
        return len(self.geos)

    def __len__(self) -> int:
        return self.n_conformers

    def xyz_str(self, comments: Optional[Iterable[str]] = None) -> str:
        xyz_str = ""
        comments = (
            repeat("") if comments is None else chain(comments, repeat(""))
        )
        for comment, geo in zip(comments, self.geos):
            xyz_str += geo.xyz_str(comment=comment)
        return xyz_str

    @classmethod
    def from_rdmol(
        cls: type[Self],
        mol: rdkit.Chem.Mol,
        n_confs: int = 100,
        max_attempts: int = 1_000_000_000,
        permute: bool = True,
        opt: None | Literal["uff"] = "uff",
        seed: int = 42,
    ) -> Self:
        """
        Generates a ConformerEnsemble from an RDKit molecule using the ETDG3
        algorithm. Energies are calculated using the UFF force field if
        optimization is requested.

        :param mol: rdkit molecule
        :param n_confs: number of conformers to generate, defaults to 1_000
        :param max_attempts: number of generation attempts,
                             defaults to 1_000_000_000
        :param energy_threshold: , defaults to 0.0
        :param rmsd_threshold: , defaults to 0.125
        :param rot_threshold: , defaults to 0.01
        :param opt: , defaults to "uff"
        :param seed: , defaults to 42
        :return: ConformerEnsemble
        """
        mol = Chem.AddHs(mol, explicitOnly=True)
        if permute is True:
            from chemtrayzer.core.graph import MolGraph

            permute = tuple(
                MolGraph.from_rdmol(mol).get_automorphic_mappings()
            )
        elif permute is not False:
            raise ValueError("permute must be True or False")

        if opt == "uff":
            mol.UpdatePropertyCache(strict=False)
            Chem.GetSymmSSSR(mol)
            Chem.SetHybridization(mol)


        ps = rdDistGeom.EmbedParameters()
        ps.ETversion = 2
        ps.ignoreSmoothingFailures = True
        ps.randomSeed = seed
        ps.enforceChirality = True
        ps.embedFragmentsSeparately = False
        ps.useRandomCoords = False
        ps.useBasicKnowledge = True
        ps.useExpTorsionAnglePrefs = True
        ps.useMacrocycle14config = True
        ps.useMacrocycleTorsions = True
        ps.useSmallRingTorsions = True
        ps.maxAttempts = max_attempts
        rdDistGeom.EmbedMultipleConfs(mol, n_confs, ps)

        if opt == "uff":
            ff = AllChem.UFFGetMoleculeForceField(mol)
            ff.Minimize(energyTol=1e-6, maxIts=100)
            energies = [ff.CalcEnergy() for _ in range(n_confs)]

        else:
            energies = None

        atom_types = [atom.GetAtomicNum() for atom in mol.GetAtoms()]
        geos = [
            Geometry(atom_types, np.array(conf.GetPositions()))
            for conf in mol.GetConformers()
        ]

        ce = ConformerEnsemble(
            geos=geos,
            energies=([0] * len(geos) if energies is None else energies),
        )

        return ce


class ChainOfStates(Sequence[Geometry]):
    """
    Container for multiple geometries.

    :param geometries: list of geometries to create to use the coordinates and
                      atom types from
    :type geometries: list[Geometries]
    :param atom_types: elements of the atoms in the correct order, Optional
    :type atom_types: Iterable[Element]
    :param coords: n_steps x n_atoms x 3 array containing atomic coordinates.
    :type coords: np.ndarray
    """

    atom_types: list[Element]
    """elements of the atoms in the correct order"""
    coords: np.ndarray
    """n_steps x n_atoms x 3 array containing atomic coordinates."""

    def __init__(
        self,
        *,
        geometries: Iterable[Geometry] = None,
        coords_list=None,
        atom_types: Iterable[Element | int | str] = None,
    ):
        if geometries is None and coords_list is None and atom_types is None:
            self.coords = None
            self.atom_types = None

        # populate from list of coordiantes and atom types
        elif geometries is None and (
            coords_list is not None and atom_types is not None
        ):
            self.atom_types = [PTOE[i] for i in atom_types]
            self.set_coords(coords_list)

        # populate from list og geomtries
        elif geometries is not None and (
            coords_list is None and atom_types is None
        ):
            self.atom_types = geometries[0].atom_types

            if not all(
                geo.atom_types == self.atom_types for geo in geometries
            ):
                raise ValueError(
                    "All geometries have to have the same atom_types"
                )

            self.set_coords(geometries)

        # illegal combination of inputs
        else:
            raise ValueError(
                "Takes only one, either, geometries or "
                "coords_list and atom_types."
            )

    def set_coords(
        self, input: list[Union[Geometry, list[list[list[float]]]]]
    ):
        """set the coordinates using a list of Geometries,
        or a list of lists"""

        if all(isinstance(i, Geometry) for i in input) and len(input) > 0:
            self.coords = self._make_coords_from_geometries(input)
        elif len(input) == 0:
            self.coords = np.array([])
        else:
            self.coords = self._make_coords_from_coords_list(input)

    def _make_coords_from_geometries(
        self, geometries: Sequence[Geometry]
    ) -> np.ndarray:
        self._check_geometries_shape_and_types(geometries)
        if getattr(self, "atom_types", None) and len(
            geometries[0].atom_types
        ) != len(self.atom_types):
            raise ValueError(
                "geometries should have the same number of atoms as the"
                "chain_of_states"
            )
        return np.array([geom.coords for geom in geometries])

    def _make_coords_from_coords_list(self, coords_list) -> np.ndarray:
        self._check_coords_list_shape(coords_list)
        if self.atom_types is not None and len(self.atom_types) != len(
            coords_list[0]
        ):
            raise ValueError(
                "the coordinates should have the same number of atoms as in "
                "atom_types"
            )
        return np.array(coords_list)

    def set_atom_types(self, input: Union[Geometry, list[Element]]) -> None:
        """
        :param input: either a list of atom types or a geometry object
        """
        if self.n_atoms > 0 and self.n_atoms != len(input):
            raise ValueError(
                "set atom types need to have the same number of atoms as "
                "the coordinates"
            )
        if isinstance(input, Geometry):
            self.atom_types = input.atom_types
        elif all(isinstance(PTOE[i], Element) for i in input):
            self.atom_types = [PTOE[i] for i in input]
        else:
            raise ValueError("not valid atom types")

    @property
    def n_frames(self) -> int:
        """
        :returns: number of frames"""
        if getattr(self, "coords", None) is None:
            return 0
        return np.shape(self.coords)[0]

    def __len__(self) -> int:
        return self.n_frames

    @property
    def n_atoms(self) -> int:
        """
        :returns: number of atoms in the first frame
        """
        if getattr(self, "coords", None) is None:
            return 0
        return np.shape(self.coords)[1]

    def xyz_str(
        self,
        comments: Optional[list[str]] = None,
    ) -> str:
        xyz_str = ""
        comments = (
            repeat("") if comments is None else chain(comments, repeat(""))
        )
        for i, (comment, frame_coords) in enumerate(
            zip(comments, self.coords)
        ):
            xyz_str += self.get_geometry(i).xyz_str(comment=comment)
        return xyz_str

    @staticmethod
    def _check_coords_list_shape(coords_list):
        for coords in coords_list:
            Geometry._check_coords_shape(coords)
            if len(coords) != len(coords_list[0]):
                raise ValueError(
                    "every frame should have the same number of atoms"
                )

    @staticmethod
    def _check_geometries_shape_and_types(
        geometries: Iterable[Geometry],
    ) -> None:
        """
        checks if number of atoms and atom_type is the same for all geometries
        coords shape and atom_types have been checked at creation of each
        geometry
        """
        if not all(
            geometry.n_atoms == geometries[0].n_atoms
            for geometry in geometries
        ):
            raise ValueError(
                "All geometries have to have the same number of atoms of the"
                " same atom_type"
            )
        if not all(
            len({atoms_with_same_index}) == 1
            for atoms_with_same_index in zip(
                *(geometry.atom_types for geometry in geometries)
            )
        ):
            raise ValueError(
                "All geometries have to have the same number of atoms of the "
                "same atom_type"
            )

    def get_geometry(self, frame: int, atoms: list[int] = None) -> Geometry:
        """ """
        if atoms is None:
            return Geometry(
                atom_types=self.atom_types, coords=self.coords[frame]
            )
        else:
            return Geometry(
                atom_types=[self.atom_types[atomid] for atomid in atoms],
                coords=self.coords[frame][atoms],
            )

    def __getitem__(self, frame: int) -> Geometry:
        return self.get_geometry(frame=frame)

    def insert(
        self,
        position: int,
        *,
        coords: Optional[Iterable] = None,
        coords_list: Optional[Iterable] = None,
        geom: Optional[Geometry] = None,
        geometries: Optional[Iterable[Geometry]] = None,
    ) -> None:
        """
        inserts the input geometry onto the given position.
        all following images are pushed back by the number of inserted frames.
        """
        num_inputs = sum(map(bool, (coords, coords_list, geom, geometries)))
        if num_inputs != 1:
            raise ValueError(
                f"one input is expected, but {num_inputs} where given "
            )
        if coords is not None:
            coords_to_insert = self._make_coords_from_coords_list([coords])
        elif coords_list is not None:
            coords_to_insert = self._make_coords_from_coords_list(coords_list)
        elif geom is not None:
            coords_to_insert = self._make_coords_from_geometries([geom])
        elif geometries is not None:
            coords_to_insert = self._make_coords_from_geometries(geometries)
        if position > self.n_frames:
            raise IndexError(
                f"can not add an image at position {position} for an object "
                f"with {self.n_frames} frames"
            )
        elif position == self.n_frames:
            self.coords: np.ndarray = np.concatenate(
                (self.coords, coords_to_insert)
            )
        elif position == 0:
            self.coords: np.ndarray = np.concatenate(
                (coords_to_insert, self.coords)
            )
        else:
            self.coords: np.ndarray = np.concatenate(
                (
                    self.coords[0:position],
                    coords_to_insert,
                    self.coords[position : self.n_frames],
                )
            )

    def append(
        self,
        *,
        coords: Optional[Iterable] = None,
        coords_list: Optional[Iterable] = None,
        geom: Optional[Geometry] = None,
        geometries: Optional[Iterable[Geometry]] = None,
    ) -> None:
        self.insert(
            self.n_frames,
            coords_list=coords_list,
            geom=geom,
            geometries=geometries,
        )

    @classmethod
    def from_xyz_file(
        cls, filepath: PathLike, comment=False
    ) -> ChainOfStates | tuple[ChainOfStates, list[str]]:
        """
        Creates a Geometry object from an xyz file
        :returns: (obj : Chain_of_states, comment : str)
        """
        geometries, comments_str = Geometry.multiple_from_xyz_file(
            filepath, comment=True
        )
        chain_of_states = cls(geometries=geometries)
        if comment is True:
            return chain_of_states, comments_str
        return chain_of_states

    def to_xyz(
        self,
        filepath: PathLike,
        comments: Optional[Iterable[str]] = None,
        overwrite: bool = False,
    ) -> None:
        comments = comments if comments is not None else ()
        for i, (comment, frame_coords) in enumerate(
            zip(chain(comments, repeat("")), self.coords)
        ):
            self.get_geometry(i).to_xyz(
                filepath,
                comment=comment,
                overwrite=True if i == 0 and overwrite else False,
            )

    def to_allxyz(
        self,
        filepath: PathLike,
        comments: Optional[Iterable[str]] = None,
        overwrite: bool = False,
    ) -> None:
        comments = comments if comments is not None else ()
        for i, (comment, frame_coords) in enumerate(
            zip(chain(comments, repeat("")), self.coords)
        ):
            self.get_geometry(i).to_xyz(
                filepath,
                comment=comment,
                overwrite=True if i == 0 and overwrite else False,
            )
            with open(filepath, "a") as f:
                f.write(">\n")

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ChainOfStates):
            raise ValueError(
                f"can not compare ChainOfStates with {type(other)}"
            )
        return self.atom_types == other.atom_types and np.allclose(
            self.coords, other.coords
        )
