import unittest
import numpy as np
import os
from shutil import rmtree
from ase.build import bulk
from pyiron_lammps.structure import (
    structure_to_lammps,
    write_lammps_datafile,
)


class TestLammpsStructure(unittest.TestCase):
    def setUp(self):
        self.output_folder = os.path.abspath(os.path.join(__file__, "..", "structure"))
        os.makedirs(self.output_folder, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        rmtree(os.path.abspath(os.path.join(__file__, "..", "structure")))

    def test_structure_to_lammps_with_velocity(self):
        structure = bulk("Al", a=4.05)
        structure.set_velocities([[1.0, 1.0, 1.0]])
        structure_lammps = structure_to_lammps(structure=structure)
        self.assertEqual(len(structure), len(structure_lammps))
        self.assertTrue(
            np.all(
                np.isclose(
                    np.abs(structure_lammps.cell),
                    np.array(
                        [
                            [2.8637824638055176, 0.0, 0.0],
                            [1.4318912319, 2.4801083645, 0.0],
                            [1.4318912319, 0.8267027881, 2.3382685902],
                        ]
                    ),
                )
            )
        )
        self.assertTrue(
            np.all(
                np.isclose(
                    structure_lammps.get_velocities(),
                    np.array([[1.41421356, 0.81649658, 0.57735027]]),
                )
            )
        )

    def test_structure_to_lammps_without_velocity(self):
        structure = bulk("Al", a=4.05)
        structure_lammps = structure_to_lammps(structure=structure)
        self.assertEqual(len(structure), len(structure_lammps))
        self.assertTrue(
            np.all(
                np.isclose(
                    np.abs(structure_lammps.cell),
                    np.array(
                        [
                            [2.8637824638055176, 0.0, 0.0],
                            [1.4318912319, 2.4801083645, 0.0],
                            [1.4318912319, 0.8267027881, 2.3382685902],
                        ]
                    ),
                )
            )
        )

    def test_structure_atomic_non_cubic(self):
        structure = bulk("Al", a=4.05)
        structure.set_velocities([[1.0, 1.0, 1.0]])
        write_lammps_datafile(
            structure=structure,
            el_eam_lst=["Ni", "Al", "H"],
            file_name="lammps.data",
            units="metal",
            cwd=self.output_folder,
        )
        with open(os.path.join(self.output_folder, "lammps.data"), "r") as f:
            self.assertEqual(
                [
                    l
                    for l in f.readlines()
                    if "xlo xhi" not in l
                    and "ylo yhi" not in l
                    and "zlo zhi" not in l
                    and "xy xz yz" not in l
                ],
                [
                    "Start File for LAMMPS \n",
                    "1 atoms \n",
                    "3 atom types \n",
                    "\n",
                    "\n",
                    "Masses\n",
                    "\n",
                    "  1 58.693400  # (Ni) \n",
                    "  2 26.981538  # (Al) \n",
                    "  3 1.008000  # (H) \n",
                    "\n",
                    "Atoms\n",
                    "\n",
                    "1 2 0.000000000000000 0.000000000000000 0.000000000000000\n",
                    "\n",
                    "Velocities\n",
                    "\n",
                    "1 1414.213562 816.496581 577.350269\n",
                ],
            )

    def test_structure_atomic_cubic(self):
        structure = bulk("Al", a=4.0, cubic=True)
        write_lammps_datafile(
            structure=structure,
            el_eam_lst=["Ni", "Al", "H"],
            file_name="lammps_cubic.data",
            units="metal",
            cwd=self.output_folder,
        )
        with open(os.path.join(self.output_folder, "lammps_cubic.data"), "r") as f:
            self.assertEqual(
                f.readlines(),
                [
                    "Start File for LAMMPS \n",
                    "4 atoms \n",
                    "3 atom types \n",
                    "\n",
                    "0. 4.000000000000000 xlo xhi\n",
                    "0. 4.000000000000000 ylo yhi\n",
                    "0. 4.000000000000000 zlo zhi\n",
                    "\n",
                    "Masses\n",
                    "\n",
                    "  1 58.693400  # (Ni) \n",
                    "  2 26.981538  # (Al) \n",
                    "  3 1.008000  # (H) \n",
                    "\n",
                    "Atoms\n",
                    "\n",
                    "1 2 0.000000000000000 0.000000000000000 0.000000000000000\n",
                    "2 2 0.000000000000000 2.000000000000000 2.000000000000000\n",
                    "3 2 2.000000000000000 0.000000000000000 2.000000000000000\n",
                    "4 2 2.000000000000000 2.000000000000000 0.000000000000000\n",
                    "\n",
                ],
            )
