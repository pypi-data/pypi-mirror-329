"""
This module contains helper classes/functions to deal with file formats
commonly used in computational chemistry or employed by this software packages.
"""

import logging
import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import TextIO, Union, Optional

from chemtrayzer.core.graph import MolGraph
from chemtrayzer.core.coords import Geometry


class SDFileReadingError(Exception):
    """raised when an error occurs during reading SD files"""


class SDFileReader:
    """reader for BIOVIA SDfiles"""

    @dataclass
    class Compound:
        """represents one item (usually one molecule) of the SDfile"""

        geometry: Optional[Geometry] = None
        graph: Optional[MolGraph] = None
        description: Optional[str] = None
        comment: Optional[str] = None
        associated_data: dict[str, str] = field(default_factory=dict)

    def __init__(
        self, path: Union[os.PathLike, str], create_graph: bool = False
    ) -> None:
        self.path = Path(path)
        self.create_graph = create_graph

    def read(self) -> list[Compound]:
        """
        :return: list of compounds in the SDF file or empty list,
                 if no compound in file
        :raises: SDFileReadingError
        """
        content = []
        with open(self.path, "r", encoding="utf-8") as fp:
            try:
                compound = self._read_compound(fp)

                while compound is not None:
                    content.append(compound)
                    compound = self._read_compound(fp)

            except SDFileReadingError as err:
                raise SDFileReadingError(
                    f"Error reading {self.path}:\n" f"{str(err)}"
                )
            except Exception as err:
                raise SDFileReadingError(f"Error reading {self.path}") from err

        return content

    def _read_compound(self, fp: TextIO):
        """:return: compound data for next compound or None if no more compound
        """
        cmpd = SDFileReader.Compound(
            geometry=None,
            graph=MolGraph() if self.create_graph else None,
            description=None,
            comment=None,
            associated_data={},
        )

        first_line = fp.readline()

        if first_line == "":
            # EOF reached, otherwise we would at least have "\n"
            return None

        # [:-1] to remove newline "\n" at end
        cmpd.description = first_line[:-1]
        program_timestamp = fp.readline()[:-1] # noqa
        cmpd.comment = fp.readline()[:-1]

        counts_line = fp.readline()[:-1].split()

        version = counts_line[-1]

        if version != "V2000":
            raise SDFileReadingError("Only V2000 SDF version compatible.")

        n_atoms = int(counts_line[0])
        n_bonds = int(counts_line[1])

        elems = []
        coords = []
        for i in range(n_atoms):
            line = fp.readline()[:-1].split()

            elems.append(line[3])
            coords.append([float(coord) for coord in line[:3]])

        cmpd.geometry = Geometry(atom_types=elems, coords=coords)

        for i in range(n_bonds):
            line = fp.readline().strip().split()
            if cmpd.graph is not None:
                for i, atom_type in enumerate(cmpd.geometry.atom_types):
                    cmpd.graph.add_atom(i, atom_type)
                cmpd.graph.add_bond(int(line[0]) - 1, int(line[1]) - 1)
            # ToDo: deal with bond type

        # skip to end of molfile section
        for line in fp:
            if line.strip().startswith("M RAD"):
                pass
                # ToDo: deal with Radical
            elif line.strip() == "M  END":
                break

        # read associated data section
        for line in fp:
            # block is terminated by "$$$$"
            if line.strip() == "$$$$":
                break

            field_name = line.split("<")[1].split(">")[0]
            content = ""

            # content section is terminated by blank line
            for line in fp:
                if line == "\n":
                    break
                content += line

            # remove last linebreak of the content
            content = content[:-1]

            cmpd.associated_data[field_name] = content

        return cmpd


def backup_file(f_path: Path):
    """makes a copy of file within the same directory and appends .backup to
    the filename. If a .backup file already exists, it will be overridden such
    that there is always just one backup.

    :param f_path: file to be backed up
    """
    if f_path.is_file():
        f_name = f_path.name
        dir_path = f_path.parent
        new_f_path = dir_path / (f_name + ".backup")

        shutil.copyfile(f_path, new_f_path)
    else:
        logging.debug(
            "File %s does not exist or is not a file. Skipping " "backup...",
            str(f_path),
        )
