import logging
import os
import pathlib
import shutil
from dataclasses import dataclass
from datetime import timedelta
from enum import Enum, auto
from io import TextIOBase
from os import PathLike
from pathlib import Path
from string import Template
from typing import Optional, Union
from collections.abc import Iterable

import numpy as np

from chemtrayzer.core.coords import Geometry
from chemtrayzer.core.graph import MolGraph
from chemtrayzer.core.md import (
    PSTAT_NOT_SET,
    BerendsenTStat,
    BoxType,
    MDIntegrator,
    MDJob,
    MDJobFactory,
    MDMetadata,
    NoseHooverTStat,
    Trajectory,
    TrajectoryParser,
)
from chemtrayzer.core.periodic_table import Element, PERIODIC_TABLE as PTOE
from chemtrayzer.engine.jobsystem import Job, JobTemplate, Memory, Program


class Lammps(Program):
    """LAMMPS molecular dynamics program"""

    class AtomStyle(Enum):
        """LAMMPS atom styles"""

        charge = auto()
        """adds partial charge information to each atom"""

    def __init__(self, executable: str) -> None:
        super().__init__(executable)

    @classmethod
    def geometry2input(
        self,
        geometry: Geometry,
        path: Union[str, PathLike],
        box_vectors: np.ndarray,
        box_origin: tuple[float, float, float],
        atom_style: AtomStyle = AtomStyle.charge,
    ):
        """generates a simple input file that can be read by the read_data
        command from a geometry


        .. note::

            The atom definitions are sorted by the atomic numbers of the
            atom_types of the geometry. Undefined behavior if a geometry
            contains two different atom_types with the same mass!"""

        def gen_masses_section() -> tuple[str, dict[Element, int]]:
            """:return: masses section and mapping from Element to its
            id (one-based)"""
            masses_str = "Masses\n\n"
            ids = {}

            # each type is only needed once and in ascending order
            atom_types = set(geometry.atom_types)
            atom_types = sorted(atom_types, key=lambda el: el.atomic_nr)

            for i, atype in enumerate(atom_types, start=1):
                masses_str += f"{i:2d} {atype.mass:7.4f}\n"
                ids[atype] = i

            return masses_str, ids

        def gen_atoms_section(
            id_map: dict[Element, int],
            charges: Optional[Iterable[float]] = None,
        ) -> str:
            atoms_str = "Atoms\n\n"
            if charges is None:
                charges = np.zeros(geometry.n_atoms)
            for i, (elem, q, (x, y, z)) in enumerate(
                zip(geometry.atom_types, charges, geometry.coords), start=1
            ):
                atoms_str += (
                    f"{i:3d} {id_map[elem]:2d} {q:.2f} "
                    f"{x:10.6f} {y:10.6f} {z:10.6f}\n"
                )
            return atoms_str

        def gen_header(n_types: int) -> str:
            # assumes orthogonal box
            xlo, ylo, zlo = box_origin
            xhi, yhi, zhi = box_origin + box_vectors.diagonal()
            return (
                "# generated by ChemTraYzer\n"
                "\n"
                f"{geometry.n_atoms} atoms\n"
                f"{n_types} atom types\n"
                "\n"
                f"{xlo:7.3f} {xhi:7.3f} xlo xhi\n"
                f"{ylo:7.3f} {yhi:7.3f} ylo yhi\n"
                f"{zlo:7.3f} {zhi:7.3f} zlo zhi\n"
            )

        if atom_style == Lammps.AtomStyle.charge:
            masses_str, id_map = gen_masses_section()
            n_types = len(id_map)
            header = gen_header(n_types)
            atoms_str = gen_atoms_section(id_map)

            with open(path, "w", encoding="utf-8") as file:
                file.write(header + "\n" + masses_str + "\n" + atoms_str)

        else:
            raise NotImplementedError("Not implemented for this atom style")


class LammpsParsingError(Exception):
    """raised when there was an error while parsing a LAMMPS file."""


class LammpsBondOrderParser:
    """Parser for files generated with the reaxff/bonds LAMMPS fix

    .. note:: assumes that the number of atoms remains constant

    :param path: Path to bond order file
    :param skip: number of steps to skip (number of steps that have been
                 written into the file, not the number of timesteps computed by
                 LAMMPS!)"""

    @dataclass
    class Result:
        n_steps: int
        """number of timesteps for which data was read"""
        steps: np.ndarray
        """n_steps long array containing the timestep numbers for which data is
        available in the other arrays"""
        bond_orders: list[dict[tuple[int, int], float]]
        """ bond orders for pairs of (zero-based and in ascending order) atom
        ids for each step.


        ``bond_orders[19][(0,5)]`` contains the bond order between atoms 0 and
        5 at timestep 19.
        """
        charges: np.ndarray
        """ n_steps x n_atoms array containing the partial charge for each atom
        and timestep """
        total_bond_orders: np.ndarray
        """ n_steps x n_atoms array containing containing the sum of all bond
        orders for each atom """
        n_lone_pairs: np.ndarray
        """ n_steps x n_atoms array containing the number of lone electron
        pairs for each atom and timestep"""

    def __init__(self, path: Union[str, PathLike]) -> None:
        self.path = path
        self._pos = 0

    def parse(self, n_steps) -> Result:
        """
        Parse n_steps of the contents of the bond file.

        Afterwards, self.skip will be incremented by n_steps, so that a second
        call to parse will continue where the first call has left off.
        """
        if n_steps < 0:
            raise ValueError('n_steps must be greater than 0')

        try:
            return self._parse(n_steps)
        except Exception as err:
            raise LammpsParsingError(
                f"An error occurred while parsing {self.path}"
            ) from err


    def _parse(self, n_steps) -> Result:
        """parse method without try except"""
        with open(self.path, "r", encoding="utf-8") as file:
            # skip self.skip steps
            file.seek(self._pos)

            # read first timestep to get number of atoms
            timestep, n_atoms, table = self._read_step(file)

            # reached end of file immediately
            n_steps = 0 if timestep is None else n_steps
            n_atoms = 0 if n_atoms is None else n_atoms

            # allocate memory
            result = self.Result(
                n_steps=n_steps,
                steps=np.zeros(n_steps),
                bond_orders=[{} for i in range(n_steps)],
                charges=np.zeros((n_steps, n_atoms)),
                total_bond_orders=np.zeros((n_steps, n_atoms)),
                n_lone_pairs=np.zeros((n_steps, n_atoms)),
            )

            if n_steps > 0:
                # add data of first step to result
                result.steps[0] = timestep
                self._fill_result_with_table(0, n_atoms, table, result)


            # go over all other steps
            for step in range(1, n_steps):
                timestep, n_atoms_again, table = self._read_step(file)

                # reached end of file
                if timestep is None:
                    n_steps = step
                    break

                # sanity check
                assert n_atoms == n_atoms_again

                result.steps[step] = timestep
                self._fill_result_with_table(step, n_atoms, table, result)

            # EOF reached before n_steps could be read
            if result.n_steps != n_steps:
                result.n_steps = n_steps
                # not doing refcheck might cause problems due to shared memory!
                result.steps.resize(n_steps, refcheck=False)
                result.bond_orders = result.bond_orders[:n_steps]
                result.charges.resize(n_steps, n_atoms, refcheck=False)
                result.total_bond_orders.resize(
                    (n_steps, n_atoms), refcheck=False
                )
                result.n_lone_pairs.resize((n_steps, n_atoms), refcheck=False)

            self._pos = file.tell()

        return result

    def _read_step(
        self, file: TextIOBase
    ) -> tuple[int, int, list[list[Union[int, float]]]]:
        """:return: (timestep, n_particles, connection table)"""
        step = None
        n_atoms = None
        table = []

        line = file.readline()
        while line:
            line = line.strip()
            # skip blank lines
            if line == "#" or line == "":
                line = file.readline()
                continue

            if line.startswith("# Timestep"):
                if step is not None:  # sanity check
                    raise LammpsParsingError(
                        "unexpected timestep definition " "encountered."
                    )

                step = int(line[11:])

            elif line.startswith("# Number of particles"):
                # sanity checks
                if step is None:
                    raise LammpsParsingError(
                        "Number of particles encountered " "before timesteps"
                    )
                if n_atoms is not None:
                    raise LammpsParsingError(
                        "Number of particles encountered "
                        "twice in the same timestep"
                    )

                n_atoms = int(line[22:])

            # data line
            elif not line.startswith("#"):
                # sanity checks
                if step is None:
                    raise LammpsParsingError(
                        "Non-commented line encountered "
                        "before timestep was defined"
                    )
                if n_atoms is None:
                    raise LammpsParsingError(
                        "Non-commented line encountered "
                        "before number of particles was defined"
                    )

                words = line.split()

                id = int(words[0])
                type = int(words[1])
                n_bonds = int(words[2])

                table.append(
                    [id, type, n_bonds]
                    + [int(word) for word in words[3 : 3 + n_bonds + 1]]
                    + [float(word) for word in words[4 + n_bonds :]]
                )

            # end of timestep
            if len(table) == n_atoms:
                break

            line = file.readline()


        return step, n_atoms, table

    def _fill_result_with_table(self, step, n_atoms, table, result: Result):
        for i in range(n_atoms):
            # lammps atom ids are one-based and the connection table is not
            # necessarily ordered by the ids
            atom_id = table[i][0] - 1
            result.charges[step, atom_id] = table[i][-1]
            result.n_lone_pairs[step, atom_id] = table[i][-2]
            result.total_bond_orders[step, atom_id] = table[i][-3]

            n_BOs = table[i][2]

            for j in range(n_BOs):
                # atom ids connected to atom_id start at position 3 and bond
                # order values start at position 3+n_BOs+1
                atom2_id = table[i][3 + j] - 1  # make id zero-based
                BO = table[i][4 + n_BOs + j]

                if atom_id < atom2_id:
                    result.bond_orders[step][(atom_id, atom2_id)] = BO
                else:
                    result.bond_orders[step][(atom2_id, atom_id)] = BO


class LammpsDumpCustomParser:
    """Parser for custom dump style of LAMMPS.

    .. note::

        LAMMPS uses one-based indexing for atoms. If your custom styles
        included the atom ids, they will be one-based in the result returned by
        this parser.

    .. note:: Assumes an orthogonal box and a constant number of atoms

    :param skip: number of steps to skip (number of steps that have been
                 written into the file, not the number of timesteps computed by
                 LAMMPS!)
    """

    @dataclass
    class Result:
        n_steps: int
        """number of timesteps for which data was read"""
        steps: np.ndarray
        """n_steps long array containing the timestep numbers for which data is
        available in the other arrays"""
        n_atoms: int
        """number of atoms"""
        box_origin: np.ndarray
        """n_steps x 3 array containing the coordinates of the corner of the
        box whose x,y and z coordinates are the smallest"""
        box_vectors: np.ndarray
        """n_steps x 3 x 3 containing the box vectors of the simulation box"""
        data: np.ndarray
        """n_steps x n_atoms x n_datapoints array containing the data for each
        frame"""
        data_labels: list[str]
        """n_datapoints long array containing the descriptors of data"""
        periodic_boundary_conditions: tuple[bool, bool, bool]
        """periodic boundary conditions in x, y and z respectively"""
        box_type: BoxType

    def __init__(self, path: Union[str, PathLike]) -> None:
        self.path = path
        self._pos = 0

    def parse(self, n_steps: int) -> Result:
        if n_steps < 0:
            raise ValueError('n_steps must be positive.')

        try:
            with open(self.path, "r", encoding="utf-8") as file:
                file.seek(self._pos)

                # read first step to get number of atoms
                (
                    timestep,
                    n_atoms,
                    pbe,
                    box_origin,
                    box_vectors,
                    labels,
                    data_str,
                    box_type,
                ) = self._read_step(file)

                # check if end of file
                n_steps = 0 if timestep is None else n_steps
                n_labels = 0 if labels is None else len(labels)
                n_atoms = 0 if n_atoms is None else n_atoms


                # allocate
                result = LammpsDumpCustomParser.Result(
                    n_steps=n_steps,
                    steps=np.zeros(n_steps),
                    n_atoms=n_atoms,
                    box_origin=np.zeros((n_steps, 3)),
                    box_vectors=np.zeros((n_steps, 3, 3)),
                    data_labels=labels,
                    data=np.zeros(
                        (n_steps, n_atoms, n_labels), dtype=float
                    ),
                    periodic_boundary_conditions=pbe,
                    box_type=box_type,
                )

                if n_steps > 0:
                    # copy data of first step into result
                    result.steps[0] = timestep
                    result.box_origin[0, :] = box_origin
                    result.box_vectors[0, :] = box_vectors
                    result.data[0, :, :] = data_str  # converted to float

                for step in range(1, n_steps):
                    # read next step
                    (
                        timestep,
                        n_atoms_curr,
                        pbe_curr,
                        box_origin,
                        box_vectors,
                        labels_curr,
                        data_str,
                        box_type,
                    ) = self._read_step(file)

                    # check for EOF
                    if timestep is None:
                        n_steps = step
                        result.n_steps = n_steps
                        # not doing refcheck might cause problems due to
                        # shared memory!!
                        result.steps.resize(n_steps, refcheck=False)
                        result.box_origin.resize(n_steps, 3, refcheck=False)
                        result.box_vectors.resize(
                            n_steps, 3, 3, refcheck=False
                        )
                        result.data.resize(
                            n_steps,
                            n_atoms,
                            len(result.data_labels),
                            refcheck=False,
                        )
                        break

                    # sanity checks
                    if (
                        n_atoms_curr != n_atoms
                        or pbe_curr != pbe
                        or labels_curr != labels
                    ):
                        raise LammpsParsingError(
                            "Assumption violated: "
                            f"{self.__class__.__name__} assumes that the "
                            "number of steps, the periodic boundary "
                            "conditions and the data labels do not change in "
                            "the trajectory"
                        )

                    # copy data into result
                    result.steps[step] = timestep
                    result.box_origin[step, :] = box_origin
                    result.box_vectors[step, :] = box_vectors
                    result.data[step, :, :] = data_str  # converted to float

                self._pos = file.tell()

            return result
        except Exception as err:
            raise LammpsParsingError(
                f"An error occurred while parsing {self.path}"
            ) from err


    def _read_step(
        self, file: TextIOBase
    ) -> tuple[
        int,
        int,
        tuple[bool, bool, bool],
        np.ndarray,
        np.ndarray,
        list[str],
        list[list[str]],
    ]:
        """:return: timestep, n_atoms, periodic_boundary_conditions,
        box_origin, box_vectors, labels, data"""
        # check for end fo file
        line = file.readline().strip()
        if line == "" or line is None:
            return [None] * 8

        # timesteps
        if line != "ITEM: TIMESTEP":
            raise LammpsParsingError("expected item: TIMESTEP")

        timestep = int(file.readline())

        # number of atoms
        if file.readline().strip() != "ITEM: NUMBER OF ATOMS":
            raise LammpsParsingError("expected item: NUMBER OF ATOMS")

        n_atoms = int(file.readline())

        # box bounds and periodic boundary conditions
        line = file.readline().strip()
        if not line.startswith("ITEM: BOX BOUNDS"):
            raise LammpsParsingError("expected item: BOX BOUNDS")

        pbe_x, pbe_y, pbe_z = line.split()[-3:]
        pbe = (pbe_x == "pp", pbe_y == "pp", pbe_z == "pp")

        if len(line.split()) == 6:
            # Orthogonal box
            xlo, xhi = file.readline().split()
            xlo, xhi = float(xlo), float(xhi)
            ylo, yhi = file.readline().split()
            ylo, yhi = float(ylo), float(yhi)
            zlo, zhi = file.readline().split()
            zlo, zhi = float(zlo), float(zhi)

            box_origin = np.array([xlo, ylo, zlo])
            box_vectors = np.array(
                [[xhi - xlo, 0, 0], [0, yhi - ylo, 0], [0, 0, zhi - zlo]]
            )
            box_type = BoxType.ORTHOGONAL
        elif len(line.split()) == 9:
            # Triclinic box
            xlo, xhi, xy = file.readline().split()
            xlo, xhi, xy = float(xlo), float(xhi), float(xy)
            ylo, yhi, xz = file.readline().split()
            ylo, yhi, xz = float(ylo), float(yhi), float(xz)
            zlo, zhi, yz = file.readline().split()
            zlo, zhi, yz = float(zlo), float(zhi), float(yz)

            box_origin = np.array([xlo, ylo, zlo])
            box_vectors = np.array(
                [[xhi - xlo, xy, xz], [0, yhi - ylo, yz], [0, 0, zhi - zlo]]
            )
            box_type = BoxType.TRICLINIC
        else:
            raise LammpsParsingError(
                "unexpected number of box bound params, expected 6 or 9 got "
                f"{len(line.split())}"
            )

        # atom info
        line = file.readline().strip()
        if not line.startswith("ITEM: ATOMS"):
            raise LammpsParsingError("expected item: ATOMS")

        labels = line[11:].strip().split()

        data_str = [file.readline().strip().split() for i in range(n_atoms)]

        return (
            timestep,
            n_atoms,
            pbe,
            box_origin,
            box_vectors,
            labels,
            data_str,
            box_type,
        )


class LammpsJob(Job):
    """Base class for all LAMMPS job objects"""

    def __init__(self, *, lammps: Lammps, **kwargs) -> None:
        super().__init__(**kwargs)

    _INPUT_TMPLS = Template(
        """\
"""
    )


class LammpsTrajParser(TrajectoryParser):
    """Parser for LAMMPS trajectory files
    either atom_types or atom_type_mapping must be provided. If
    atom_type_mapping is specified, the atom_types will be generated during
    __init__ based on the atom_type_mapping. It is crucial that the user
    specifies the atom_types as an ordered list of atom types, in the order of
    the atom ids in the dump file. E.g. starting with the atom type of the atom
    with id 1, 2, ...
    """

    def __init__(
        self,
        custom_dump_path: Union[str, PathLike],
        bond_path: Union[str, PathLike],
        metadata: MDMetadata,
        atom_type_mapping: dict = None,
        atom_types: tuple[str] = None,
    ) -> None:
        """constructor for the LammpsTrajParser class

        :param custom_dump_path: path to the dump file
        :param bond_path: path to the bond order file
        :param metadata: MDMetadata of the job
        :param atom_type_mapping: mappings of atom type (force field) to
                                  chemical element(element).
        :param atom_types: tuple of atom types in the order specified in the
            dump file
        """

        self.custom_dump_path = custom_dump_path
        self.bond_path = bond_path
        self.metadata = metadata
        self.atom_type_mapping = atom_type_mapping
        if atom_types is None:
            if atom_type_mapping is None:  # 0 0
                raise ValueError(
                    "Either atom_types or atom_type_mapping must be provided"
                )
            else:  # 0 1
                self.atom_types = self._get_atom_types_from_custom_dump()
        elif atom_type_mapping is not None:  # 1 1
            raise ValueError(
                "Either atom_types or atom_type_mapping must be "
                "provided, but not both"
            )
        else:  # 1 0
            self.atom_types = atom_types

        # store parser to keep their internal state (i.e. position pointer)
        self.custom_parser = LammpsDumpCustomParser(self.custom_dump_path)
        self.bond_parser = LammpsBondOrderParser(self.bond_path)

    def parse(self, n_steps: int = -1) -> Trajectory:
        """gets the trajectory and bond orders, where the latter will be
        included in the graphs member variable of the returned trajectory
        object"""
        # if no number of steps is given, use the total number of steps
        # in metadata
        if n_steps == -1:
            n_steps = self.metadata.number_of_steps

        custom_parser = self.custom_parser
        bond_parser = self.bond_parser

        custom_data = custom_parser.parse(n_steps)
        bond_data = bond_parser.parse(n_steps)

        # number_of_steps = actual number of steps in file
        n_steps = custom_data.data.shape[0]
        n_atoms = len(self.atom_types)

        # empty trajectory
        if custom_data.n_steps == 0:
            return Trajectory(
                metadata=self.metadata,
                atom_types=self.atom_types,
                coords=np.zeros((0,n_atoms, 3)),
                box_vectors=np.zeros((0, 3, 3)),
                box_origin=np.zeros((0, 3)),
                graphs=[],
            )

        assert n_atoms == custom_data.data.shape[1], (
            "Number of atoms in trajectory does not match length of atom_types"
        )
        assert custom_data.data_labels[0] == "id", (
            "The 'id' column was not found in the custom dump file or is in "
            "the wrong order. Expected format: id, type, x, y, z, vx, vy, vz, "
            "c_ape"
        )
        assert custom_data.data_labels[2] == "x", (
            "The 'x' column was not found in the custom dump file or is in the"
            " wrong order. Expected format: id, type, x, y, z, vx, vy, vz, "
            "c_ape"
        )
        assert custom_data.data_labels[3] == "y", (
            "The 'y' column was not found in the custom dump file or is in the"
            " wrong order. Expected format: id, type, x, y, z, vx, vy, vz, "
            "c_ape"
        )
        assert custom_data.data_labels[4] == "z", (
            "The 'z' column was not found in the custom dump file or is in the"
            " wrong order. Expected format: id, type, x, y, z, vx, vy, vz, "
            "c_ape"
        )

        ids = np.array(custom_data.data[:, :, 0], dtype=int)
        coords = np.zeros((n_steps, n_atoms, 3))
        # lammps ids start at 1
        ids -= 1

        # the output in the dump file is not necessarily sorted, that is why
        # it is important to also use the printed atom ids
        for i in range(coords.shape[0]):
            coords[i, ids[i], :] = custom_data.data[i, :, 2:5]

        # constant volume (only store first frame to not waste memory)
        if self.metadata.barostat == PSTAT_NOT_SET:
            # make efficient use of repeating elements by broadcasting the
            # first frame copy is used so that box_origin is independent of
            # custom_data and custom_data can be deleted
            box_origin = np.broadcast_to(
                custom_data.box_origin[0, :].copy(), (n_steps, 3)
            )
            box_vectors = np.broadcast_to(
                custom_data.box_vectors[0, :].copy(), (n_steps, 3, 3)
            )
        else:  # constant pressure
            if self.metadata.barostat is None:
                logging.warning('Barostat is None. If no barostat was used set'
                                ' it to %s for more efficient parsing.',
                                PSTAT_NOT_SET.type)
            box_origin = custom_data.box_origin.copy()
            box_vectors = custom_data.box_vectors.copy()

        traj = Trajectory(
            metadata=self.metadata,
            atom_types=self.atom_types,
            coords=coords,
            box_vectors=box_vectors,
            box_origin=box_origin,
        )

        traj.charges = bond_data.charges

        traj.graphs = []

        for BOs in bond_data.bond_orders:
            g = MolGraph()
            for atomid in range(0, n_atoms):
                g.add_atom(atomid, atom_type=self.atom_types[atomid])
            for (u, v), BO in BOs.items():
                g.add_bond(u, v, bond_order=BO)

            traj.graphs.append(g)

        return traj

    def _get_atom_types_from_custom_dump(self) -> tuple[str]:
        """read first frame from the custom.dump and get atom types based on
        the atom_type_mapping. Watch out that you read in the number of atoms
        before you read in the atom types."""
        atom_type_mapping = {k: PTOE[v].atomic_nr
                             for k, v in self.atom_type_mapping.items()}

        with open(self.custom_dump_path, "r", encoding="utf-8") as file:
            line = file.readline()
            while line:  # use this type of iteration to allow the use of tell
                if line.startswith("ITEM: NUMBER OF ATOMS"):
                    n_atoms = int(file.readline())
                    atom_types = np.zeros(n_atoms, dtype=int)
                if line.startswith("ITEM: ATOMS"):
                    for _ in range(n_atoms):
                        line = file.readline().split()
                        atom_id, atom_type_ff = line[
                            0:2
                        ]  # atom_id and atom type in the force field
                        # this approach encodes the atom id as the position
                        # in the array
                        atom_types[int(atom_id) - 1]\
                            = atom_type_mapping[int(atom_type_ff)]
                    break

                line = file.readline()
        return atom_types


class LammpsReaxFFJob(MDJob):
    r"""
    Job for the LAMMPS molecular dynamics software for simulations using a
    ReaxFF force field.

    .. note::

        Since jobs, including their result, are saved by the job system, and
        trajectory data can be very large, this job does not immediately read
        the trajectory data from disk. Instead, it creates a parser object that
        remembers the job's id. When ``parse()`` is called on this parser
        object later, the parser gets the relevant data from the job system
        using the job's id and constructs a trajectory object from the data in
        the job directory.

    :param metadata: details of the job, that should be submitted
    :param initial_geometry: simulation box of the first frame. The coordinates
                            here are absolute, i.e. **not** relative to
                            metadata.initial_box.box_origin
    :param reaxff_path: path to a ReaxFF parameter file.
    :param lammps: LAMMPS software
    :ivar result: result set by ``parse_result``. If successful, it will
                  contain a dictionary with the key "trajectory_parser" and a
                  :class:`LammpsReaxFFJob.TrajParser` object as value
    :param \*\*kwargs: keywords to specify the jobs runtime, etc.
    """

    _CMD_TMPL = "${executable} -in in.lmp"
    _INPUT_TMPLS = {
        "in.lmp": """\
log lammps.log

### init system
units           real
    # also store charge for each atom
atom_style      charge
atom_modify     map hash
read_data       ${DATA_FILE}

### force field
    # also store charge for each atom
    # use reax/c keyword for downward compatibility
pair_style      reax/c NULL
pair_coeff      * * ${REAXFF_FILE} ${atoms_in_order}
    # perform charge equilibration (QEq) and read the respective parameters
    # from the reaxff file
fix             qeq all qeq/reax 1 0.0 10.0 1e-6 reax/c

### neighbor list generation
neighbor        2 bin
neigh_modify    every 10 delay 0 check no
${thermostat_str}
### output
    # set output for printing thermodynamic information
thermo_style    custom step temp press etotal pe ke
    # print thermo data every X steps
thermo          ${dump_steps}

    # compute the energy per atom
compute         ape all pe/atom
    # write id, type, coordinates, velocities and energy per atom energy in
    # file
dump            dmp all custom ${dump_steps} ${DUMP_FILE} id type x y z &
                                                          vx vy vz c_ape
    # write ReaxFF bond orders to disk
fix             bnd all reax/c/bonds ${dump_steps} ${BOND_FILE}

### simulation
timestep        ${timestep}
    # run
run             ${n_steps}

undump dmp
unfix bnd
"""
    }

    @dataclass(kw_only=True)
    class Result(MDJob.Result):
        path: Path
        metadata: MDMetadata
        initial_geometry: Geometry
        _trajectory_parser: LammpsTrajParser = (
            None  # Define _trajectory_parser in __post_init__
        )

        def __post_init__(self):
            self.path = Path(self.path)

            bond_path = self.path / "bonds.dmp"
            custom_dump_path = self.path / "custom.dmp"
            atom_types = self.initial_geometry.atom_types
            self._trajectory_parser = LammpsTrajParser(
                bond_path=bond_path,
                custom_dump_path=custom_dump_path,
                metadata=self.metadata,
                atom_types=atom_types,
            )

        def parse(self, n_steps: int = -1) -> Trajectory:
            """parse the data from the job directory and return a trajectory.
                parsing functionality has been moved to the LammpsTrajParser
                class

            :return: Trajectory"""
            return self._trajectory_parser.parse(n_steps=n_steps)

    def __init__(
        self,
        *,
        metadata: MDMetadata,
        initial_geometry: Geometry,
        reaxff_path: Union[str, os.PathLike],
        lammps: Lammps,
        **kwargs,
    ) -> None:
        super().__init__(lammps=lammps, **kwargs)

        if metadata.initial_box.box_type != BoxType.ORTHOGONAL:
            raise NotImplementedError("Non-orthogonal boxes not supported")
        if (
            isinstance(metadata.thermostat, NoseHooverTStat)
            and metadata.integration_method != MDIntegrator.VELOCITY_VERLET
        ):
            raise ValueError(
                "Invalid integration scheme for " "Nosé-Hoover thermostat"
            )
        if (
            isinstance(metadata.thermostat, BerendsenTStat)
            and metadata.integration_method != MDIntegrator.VELOCITY_VERLET
        ):
            raise ValueError(
                "Invalid integration scheme for " "Berendsen thermostat"
            )

        self.metadata = metadata
        self.reaxff_path = reaxff_path
        self.lammps = lammps

        # needed to fill template
        self.executable = lammps.executable
        self.dump_steps = metadata.sampling_frequency
        self.timestep = metadata.timestep
        self.n_steps = metadata.number_of_steps
        self.DATA_FILE = "data.lmp"
        self.REAXFF_FILE = "reax.ff"
        self.DUMP_FILE = "custom.dmp"
        self.BOND_FILE = "bonds.dmp"

        self.initial_geometry = initial_geometry
        self._reaxff_path = reaxff_path

        self._template = JobTemplate(self, self._CMD_TMPL, self._INPUT_TMPLS)

    def parse_result(self, path):
        try:
            self.result = LammpsReaxFFJob.Result(
                path=path,
                metadata=self.metadata,
                initial_geometry=self.initial_geometry,
            )
            self.succeed()
        except Exception as e:
            self.fail(e)

    def gen_input(self, path):
        path = pathlib.Path(path)
        # force field
        shutil.copyfile(self._reaxff_path, path / self.REAXFF_FILE)

        # input box definition
        self.lammps.geometry2input(
            self.initial_geometry,
            path=path / self.DATA_FILE,
            box_vectors=self.metadata.initial_box.box_vectors,
            box_origin=self.metadata.initial_box.box_origin,
        )

        # input file
        self._template.gen_input(path)

    @property
    def thermostat_str(self) -> str:
        """used to generate part of the input file"""
        thermo_str = ""

        if self.metadata.thermostat is not None:
            thermo_str += "\n### thermostat and temperature\n"
        else:
            return ""

        if self.metadata.seed is not None:
            thermo_str += "    # generate initial velocity distribution\n"
            thermo_str += (
                "velocity        all create "
                + str(self.metadata.thermostat.temperature)
                + " "
                + str(self.metadata.seed)
                + " mom yes rot yes\n"
            )

        T = self.metadata.thermostat.temperature
        tau = self.metadata.thermostat.tau

        if isinstance(self.metadata.thermostat, NoseHooverTStat):
            # check the integration scheme
            if (
                self.metadata.integration_method
                != MDIntegrator.VELOCITY_VERLET
            ):
                raise ValueError(
                    "Invalid integration scheme for " "Nosé-Hoover thermostat"
                )

            chain_length = self.metadata.thermostat.chain_length

            thermo_str += f"""\
    # use a Nose-Hoover thermostat (incl. integration)
fix             thermostat all nvt temp {T} {T} {tau} tchain {chain_length}
"""

        elif isinstance(self.metadata.thermostat, BerendsenTStat):
            # check the integration scheme
            if (
                self.metadata.integration_method
                != MDIntegrator.VELOCITY_VERLET
            ):
                raise ValueError(
                    "Invalid integration scheme for " "Berendsen thermostat"
                )

            thermo_str += f"""\
    # Berendsen thermostat does not include time integration
fix		        integration all nve
    # use a Berendsen thermostat
fix             thermostat all temp/berendsen {T} {T} {tau}
"""
        else:
            raise NotImplementedError("Thermostat not implemented")

        return thermo_str

    @property
    def atoms_in_order(self) -> str:
        """generates part of the input file"""

        def extract_atomic_nr(elem: Element):
            return elem.atomic_nr

        sorted_elems = sorted(
            set(self.initial_geometry.atom_types), key=extract_atomic_nr
        )

        elems_str = " ".join([elem.symbol for elem in sorted_elems])

        return elems_str

    @property
    def command(self):
        return self._template.command


class LammpsReaxFFJobFactory(MDJobFactory):
    """Factory for creating LAMMPS ReaxFF jobs

    :param reaxff_path: path to a ReaxFF parameter file
    :param lammps: LAMMPS software
    :param n_cpus: number of CPUs to use
    :param n_tasks: number of tasks to use
    :param memory: maximum memory per cpu
    :param runtime: maximum runtime
    """

    def __init__(
        self,
        *,
        reaxff_path: Union[str, os.PathLike],
        lammps: Lammps,
        n_cpus: int,
        n_tasks: int,
        memory: Memory,
        runtime: timedelta,
    ) -> None:
        self.reaxff_path = reaxff_path
        self.lammps = lammps
        self.kwargs = {
            "n_cpus": n_cpus,
            "n_tasks": n_tasks,
            "memory": memory,
            "runtime": runtime,
        }

    def create(
        self,
        metadata: MDMetadata,
        initial_geometry: Geometry,
        name: str = None,
    ) -> MDJob:
        """
        create a Lammps ReaxFF.
        :param metadata: options and settings for MD
        :param initial_geometry: initial box geometry
        :param name: optional name
        """
        super().create(
            metadata=metadata, initial_geometry=initial_geometry, name=name
        )

        return LammpsReaxFFJob(
            metadata=metadata,
            initial_geometry=initial_geometry,
            reaxff_path=self.reaxff_path,
            lammps=self.lammps,
            name=name,
            **self.kwargs,
        )
