"""
This module contains classes to generate simulation boxes for MD simulations.
"""

import os
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import timedelta
from pathlib import PurePath

from chemtrayzer.core.coords import Geometry, InvalidXYZFileError
from chemtrayzer.engine.jobsystem import Job, JobTemplate, Memory


class PackmolJob(Job):
    r"""
    Create simple MD boxes using Packmol.

    :param name: string - name of job
    :param geometries: geometry of species added to the box
    :param count: number of molecules for each geometry which should be added
                  to the box
    :param box_dim: tuple of six integers (x1, y1, z1, x2, y2, z2) which define
                    the two points spanning the box
    :param executable: path to Packmol executable
    :param tol: minimum distance between atoms of different molecules in
                Angstrom
    :param result: dictionary with keys 'box' for storing the generated
                   geometry and 'reason' for holding the reason for a possible
                   failure
    :type result: dict
    :param \**kwargs: standard arguments to configure a Job (e.g. n_cpus)
    :type result: Geometry
    """

    _CMD_TMPL = "${executable} < packmol.inp"
    _INPUT_TMPLS = {
        "packmol.inp": """\
tolerance ${tol}

filetype xyz

output mixture.xyz

${_tmpl_struct_def}"""
    }

    @dataclass
    class Result(Job.Result):
        """result of a PackmolJob"""

        box: Geometry
        """packed box"""

    def __init__(
        self,
        geometries: Iterable[Geometry],
        count: Iterable[int],
        box_dim: tuple[float],
        executable: os.PathLike,
        tol: float = 2.0,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.count = count
        self.geometries = geometries
        self.box_dim = box_dim
        self.result = None

        if len(self.box_dim) != 6:
            raise ValueError("box_dim needs to contain six coordinates")

        self.tol = tol
        self.executable = executable

        self._template = JobTemplate(self, self._CMD_TMPL, self._INPUT_TMPLS)

    def gen_input(self, path):
        self._template.gen_input(path)  # for packmol.inp

        for i, geo in enumerate(self.geometries):
            geo.to_xyz(os.path.join(path, f"geo{i}.xyz"))

    @property
    def command(self):
        return self._template.command

    @property
    def _tmpl_struct_def(self) -> str:
        """assembles structure definition of input file"""

        box_def = " ".join([f"{coord:f}" for coord in self.box_dim])

        return "\n".join(
            [
                f"structure geo{i}.xyz\n  number {count}\n"
                f"  inside box {box_def}\nend structure\n"
                for i, (count, geo) in enumerate(
                    zip(self.count, self.geometries)
                )
            ]
        )

    def parse_result(self, path):
        try:
            self.result = self.Result(
                box=Geometry.from_xyz_file(os.path.join(path, "mixture.xyz"))
            )
            self.succeed()
        except (InvalidXYZFileError, FileNotFoundError) as e:
            self.fail(e)


class PackmolJobFactory:
    """Factory for jobs of type PackmolJob

    :param packmol: path to packmol executable
    :param account: SLURM account to use for MDBoxJobs (this setting overrides
                    the account specified in the job system)
    """

    def __init__(self, packmol: os.PathLike, account: str = None) -> None:
        self._packmol = PurePath(packmol)
        self._account = account

    def create(
        self,
        name,
        geometries: Iterable[Geometry],
        count: Iterable[int],
        box_dim: tuple[int],
        metadata: object = None,
    ) -> PackmolJob:
        """
        :param name: string - name of job
        :param geometries: geometry of species added to the box
        :param count: number of molecules for each geometry which should be
                      added to the box
        :param box_dim: tuple of six integers (x1, y1, z1, x2, y2, z2) which
                        define the two points spanning the box
        :param metadata: any metadata you may want to add to the job
        """
        job = PackmolJob(
            geometries,
            count,
            box_dim,
            executable=self._packmol,
            tol=2,  # default tolerance (may be changed later)
            name=name,
            account=self._account,
            n_tasks=1,  # a packmol jobs does not need a lot of resources
            n_cpus=1,
            memory=Memory(1, unit=Memory.UNIT_GB),  # enough for most box sizes
            runtime=timedelta(minutes=15),  # packmol usually only runs seconds
            metadata=metadata,
        )

        return job
