# coding: utf-8
# Copyright (c) Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department
# Distributed under the terms of "New BSD License", see the LICENSE file.

from __future__ import print_function

import decimal as dec
import posixpath
import warnings
from collections import OrderedDict

import numpy as np

from pyiron_atomistics.lammps.units import UnitConverter

try:
    from ase.calculators.lammps import Prism
except ImportError:
    try:
        from ase.calculators.lammpsrun import Prism
    except ImportError:
        from ase.calculators.lammpsrun import prism as Prism

__author__ = "Joerg Neugebauer, Sudarsan Surendralal, Yury Lysogorskiy, Jan Janssen, Markus Tautschnig"
__copyright__ = (
    "Copyright 2021, Max-Planck-Institut für Eisenforschung GmbH - "
    "Computational Materials Design (CM) Department"
)
__version__ = "1.0"
__maintainer__ = "Sudarsan Surendralal"
__email__ = "surendralal@mpie.de"
__status__ = "production"
__date__ = "Sep 1, 2017"


class UnfoldingPrism(Prism):
    """
    Create a lammps-style triclinic prism object from a cell

    The main purpose of the prism-object is to create suitable
    string representations of prism limits and atom positions
    within the prism.
    When creating the object, the digits parameter (default set to 10)
    specify the precision to use.
    lammps is picky about stuff being within semi-open intervals,
    e.g. for atom positions (when using create_atom in the in-file),
    x must be within [xlo, xhi).

    Args:
        cell:
        pbc:
        digits:
    """

    def __init__(self, cell, pbc=(True, True, True), digits=10):
        # Temporary fix. Since the arguments for the constructor have changed, try to see if it is compatible with
        # the latest ase. If not, revert to the old __init__ parameters.
        try:
            super(UnfoldingPrism, self).__init__(
                cell, pbc=pbc, tolerance=float("1e-{}".format(digits))
            )
        except TypeError:
            super(UnfoldingPrism, self).__init__(cell, pbc=pbc, digits=digits)
        a, b, c = cell
        an, bn, cn = [np.linalg.norm(v) for v in cell]

        alpha = np.arccos(np.dot(b, c) / (bn * cn))
        beta = np.arccos(np.dot(a, c) / (an * cn))
        gamma = np.arccos(np.dot(a, b) / (an * bn))

        xhi = an
        xyp = np.cos(gamma) * bn
        yhi = np.sin(gamma) * bn
        xzp = np.cos(beta) * cn
        yzp = (bn * cn * np.cos(alpha) - xyp * xzp) / yhi
        zhi = np.sqrt(cn**2 - xzp**2 - yzp**2)

        # Set precision
        self.car_prec = dec.Decimal("10.0") ** int(
            np.floor(np.log10(max((xhi, yhi, zhi)))) - digits
        )
        self.dir_prec = dec.Decimal("10.0") ** (-digits)
        self.acc = float(self.car_prec)
        self.eps = np.finfo(xhi).eps

        # For rotating positions from ase to lammps
        apre = np.array(((xhi, 0, 0), (xyp, yhi, 0), (xzp, yzp, zhi)))
        # np.linalg.inv(cell) ?= np.array([np.cross(b, c), np.cross(c, a), np.cross(a, b)]).T / np.linalg.det(cell)
        self.R = np.dot(np.linalg.inv(cell), apre)

        def fold(vec, pvec, i):
            p = pvec[i]
            x = vec[i] + 0.5 * p
            n = (np.mod(x, p) - x) / p
            return [float(self.f2qdec(vec_a)) for vec_a in (vec + n * pvec)], n

        apre[1, :], n1 = fold(apre[1, :], apre[0, :], 0)
        if np.abs(apre[1, 0] / apre[0, 0]) > 0.5:
            apre[1, 0] -= np.sign(n1) * apre[0, 0]
            n1 -= np.sign(n1)

        apre[2, :], n2 = fold(apre[2, :], apre[1, :], 1)
        if np.abs(apre[2, 1] / apre[1, 1]) > 0.5:
            apre[2, 1] -= np.sign(n2) * apre[1, 1]
            n2 -= np.sign(n2)

        apre[2, :], n3 = fold(apre[2, :], apre[0, :], 0)
        if np.abs(apre[2, 0] / apre[0, 0]) > 0.5:
            apre[2, 0] -= np.sign(n3) * apre[0, 0]
            n3 -= np.sign(n3)
        self.ns = [n1, n2, n3]

        d_a = apre[0, 0] / 2 - apre[1, 0]
        if np.abs(d_a) < self.acc:
            if d_a < 0:
                print("debug: apply shift")
                apre[1, 0] += 2 * d_a
                apre[2, 0] += 2 * d_a

        self.A = apre

        if self.is_skewed() and (not (pbc[0] and pbc[1] and pbc[2])):
            warnings.warn(
                "Skewed lammps cells should have PBC == True in all directions!"
            )

    def unfold_cell(self, cell):
        """
        Unfold LAMMPS cell to original

        Let C be the pyiron_atomistics cell and A be the Lammps cell, then define (in init) the rotation matrix between them as
            R := C^inv.A
        And recall that rotation matrices have the property
            R^T == R^inv
        Then left multiply the definition of R by C, and right multiply by R.T to get
            C.R.R^T = C.C^inv.A.R^T
        Then
            C = A.R^T

        After that, account for the folding process.

        Args:
            cell: LAMMPS cell,

        Returns:
            unfolded cell
        """
        # Rotation
        ucell = np.dot(cell, self.R.T)
        # Folding
        a = ucell[0]
        bp = ucell[1]
        cpp = ucell[2]
        (n1, n2, n3) = self.ns
        b = bp - n1 * a
        c = cpp - n2 * bp - n3 * a
        return np.array([a, b, c])

    def pos_to_lammps(self, position):
        """
        Rotate an ase-cell position to the lammps cell orientation

        Args:
            position:

        Returns:
            tuple of float.
        """
        return tuple([x for x in np.dot(position, self.R)])

    def f2qdec(self, f):
        return dec.Decimal(repr(f)).quantize(self.car_prec, dec.ROUND_DOWN)

    def f2s(self, f):
        return str(dec.Decimal(repr(f)).quantize(self.car_prec, dec.ROUND_HALF_EVEN))

    def get_lammps_prism_str(self):
        """Return a tuple of strings"""
        p = self.get_lammps_prism()
        return tuple([self.f2s(x) for x in p])


class LammpsStructure(object):
    """

    Args:
        input_file_name:
    """

    def __init__(self, bond_dict=None, job=None):
        self._string_input = ""
        self._structure = None
        self._potential = None
        self._el_eam_lst = []
        self.atom_type = None
        self.cutoff_radius = None
        self.digits = 10
        self._bond_dict = bond_dict
        self._force_skewed = False
        self._job = job
        self._molecule_ids = []

    @property
    def potential(self):
        return self._potential

    @potential.setter
    def potential(self, val):
        self._potential = val

    @property
    def structure(self):
        """

        Returns:

        """
        return self._structure

    @structure.setter
    def structure(self, structure):
        """

        Args:
            structure:

        Returns:

        """
        self._structure = structure
        if self.atom_type == "full":
            input_str = self.structure_full()
        elif self.atom_type == "bond":
            input_str = self.structure_bond()
        elif self.atom_type == "charge":
            input_str = self.structure_charge()
        else:  # self.atom_type == 'atomic'
            input_str = self.structure_atomic()

        if self._structure.velocities is not None:
            uc = UnitConverter(self._job.units)
            self._structure.velocities *= uc.pyiron_to_lammps("velocity")
            vels = self.rotate_velocities(self._structure)
            input_str += "Velocities\n\n"
            if self._structure.dimension == 3:
                format_str = "{0:d} {1:f} {2:f} {3:f}\n"
                for id_atom, (x, y, z) in enumerate(vels, start=1):
                    input_str += format_str.format(id_atom, x, y, z)
            if self._structure.dimension == 2:
                format_str = "{0:d} {1:f} {2:f}\n"
                for id_atom, (x, y) in enumerate(vels, start=1):
                    input_str += format_str.format(id_atom, x, y)
        self._string_input = input_str

    @property
    def molecule_ids(self):
        return self._molecule_ids

    @molecule_ids.setter
    def molecule_ids(self, molecule_ids=None):
        if molecule_ids is None:
            if "molecule_ids" in self.structure.get_tags():
                self._molecule_ids = self.structure.molecule_ids
            else:
                self._molecule_ids = np.ones(len(self.structure), dtype=int)
        else:
            self._molecule_ids = molecule_ids

    @property
    def el_eam_lst(self):
        """

        Returns:

        """
        return self._el_eam_lst

    @el_eam_lst.setter
    def el_eam_lst(self, el_eam_lst):
        """

        Args:
            el_eam_lst:

        Returns:

        """
        self._el_eam_lst = el_eam_lst

    @staticmethod
    def get_lammps_id_dict(el_eam_lst):
        if len(el_eam_lst) == 0:
            raise ValueError("el_eam_list is empty. Can not determine order of species")
        return {el: idx + 1 for idx, el in enumerate(el_eam_lst)}

    @staticmethod
    def lammps_header(
        structure,
        cell_dimensions,
        species_lammps_id_dict,
        nbonds=None,
        nangles=None,
        nbond_types=None,
        nangle_types=None,
    ):
        atomtypes = (
            "Start File for LAMMPS \n"
            + "{0:d} atoms".format(len(structure))
            + " \n"
            + "{0} atom types".format(len(species_lammps_id_dict.keys()))
            + " \n"
        )  # '{0} atom types'.format(structure.get_number_of_species()) + ' \n'
        if nbonds is not None:
            atomtypes += "{0:d} bonds\n".format(nbonds)
        if nangles is not None:
            atomtypes += "{0:d} angles\n".format(nangles)
        if nbond_types is not None:
            atomtypes += "{0:d} bond types\n".format(nbond_types)
        if nangle_types is not None:
            atomtypes += "{0:d} angle types\n".format(nangle_types)

        masses = "Masses\n\n"
        for el, idx in species_lammps_id_dict.items():
            mass = structure._pse[el].AtomicMass
            masses += "{0:3d} {1:f}  # ({2}) \n".format(idx, mass, el)

        return atomtypes + "\n" + cell_dimensions + "\n" + masses + "\n"

    def simulation_cell(self):
        """

        Returns:

        """

        self.prism = UnfoldingPrism(self._structure.cell, digits=15)
        xhi, yhi, zhi, xy, xz, yz = self.prism.get_lammps_prism_str()
        # Please, be carefull and not round xhi, yhi,..., otherwise you will get too skew cell from LAMMPS.
        # These values are already checked in UnfoldingPrism to fullfill LAMMPS skewness criteria
        simulation_cell = (
            "0. {} xlo xhi\n".format(xhi)
            + "0. {} ylo yhi\n".format(yhi)
            + "0. {} zlo zhi\n".format(zhi)
        )

        if self.structure.is_skewed() or self._force_skewed:
            simulation_cell += "{0} {1} {2} xy xz yz\n".format(xy, xz, yz)

        return simulation_cell

    def structure_bond(self):
        """

        Returns:

        """
        species_lammps_id_dict = self.get_lammps_id_dict(self.el_eam_lst)
        self.molecule_ids = None
        # analyze structure to get molecule_ids, bonds, angles etc
        coords = self.rotate_positions(self._structure)

        elements = self._structure.get_chemical_symbols()

        ## Standard atoms stuff
        atoms = "Atoms \n\n"
        # atom_style bond
        # format: atom-ID, molecule-ID, atom_type, x, y, z
        format_str = "{0:d} {1:d} {2:d} {3:f} {4:f} {5:f} "
        if self._structure.dimension == 3:
            for id_atom, (x, y, z) in enumerate(coords):
                id_mol = self.molecule_ids[id_atom]
                atoms += (
                    format_str.format(
                        id_atom + 1,
                        id_mol,
                        species_lammps_id_dict[elements[id_atom]],
                        x,
                        y,
                        z,
                    )
                    + "\n"
                )
        elif self._structure.dimension == 2:
            for id_atom, (x, y) in enumerate(coords):
                id_mol = self.molecule_ids[id_atom]
                atoms += (
                    format_str.format(
                        id_atom + 1,
                        id_mol,
                        species_lammps_id_dict[elements[id_atom]],
                        x,
                        y,
                        0.0,
                    )
                    + "\n"
                )
        else:
            raise ValueError("dimension 1 not yet implemented")

        ## Bond related.
        # This seems independent from the lammps atom type ids, because bonds only use atom ids
        el_list = self._structure.get_species_symbols()
        el_dict = OrderedDict()
        for object_id, el in enumerate(el_list):
            el_dict[el] = object_id

        n_s = len(el_list)
        bond_type = np.ones([n_s, n_s], dtype=int)
        count = 0
        for i in range(n_s):
            for j in range(i, n_s):
                count += 1
                bond_type[i, j] = count
                bond_type[j, i] = count

        if self.structure.bonds is None:
            if self.cutoff_radius is None:
                bonds_lst = self.structure.get_bonds(max_shells=1)
            else:
                bonds_lst = self.structure.get_bonds(radius=self.cutoff_radius)
            bonds = []

            for ia, i_bonds in enumerate(bonds_lst):
                el_i = el_dict[elements[ia]]
                for el_j, b_lst in i_bonds.items():
                    b_type = bond_type[el_i][el_dict[el_j]]
                    for i_shell, ib_shell_lst in enumerate(b_lst):
                        for ib in np.unique(ib_shell_lst):
                            if ia < ib:  # avoid double counting of bonds
                                bonds.append([ia + 1, ib + 1, b_type])

            self.structure.bonds = np.array(bonds)
        bonds = self.structure.bonds

        bonds_str = "Bonds \n\n"
        for i_bond, (i_a, i_b, b_type) in enumerate(bonds):
            bonds_str += (
                "{0:d} {1:d} {2:d} {3:d}".format(i_bond + 1, b_type, i_a, i_b) + "\n"
            )

        return (
            self.lammps_header(
                structure=self.structure,
                cell_dimensions=self.simulation_cell(),
                species_lammps_id_dict=species_lammps_id_dict,
                nbonds=len(bonds),
                nbond_types=np.max(np.array(bonds)[:, 2]),
            )
            + "\n"
            + atoms
            + "\n"
            + bonds_str
            + "\n"
        )

    def structure_full(self):
        """
        Write routine to create atom structure static file for atom_type='full' that can be loaded by LAMMPS

        Returns:

        """
        species_lammps_id_dict = self.get_lammps_id_dict(self.el_eam_lst)
        self.molecule_ids = None
        coords = self.rotate_positions(self._structure)

        # extract electric charges from potential file
        q_dict = {}
        for species in self.structure.species:
            species_name = species.Abbreviation
            q_dict[species_name] = self.potential.get_charge(species_name)

        bonds_lst, angles_lst = [], []
        bond_type_lst, angle_type_lst = [], []
        # Using a cutoff distance to draw the bonds instead of the number of neighbors
        # Only if any bonds are defined
        if len(self._bond_dict.keys()) > 0:
            cutoff_list = list()
            for val in self._bond_dict.values():
                cutoff_list.append(np.max(val["cutoff_list"]))
            max_cutoff = np.max(cutoff_list)
            # Calculate neighbors only once
            neighbors = self._structure.get_neighbors_by_distance(
                cutoff_radius=max_cutoff
            )

            # Draw bonds between atoms is defined in self._bond_dict
            # Go through all elements for which bonds are defined
            for element, val in self._bond_dict.items():
                el_1_list = self._structure.select_index(element)
                if el_1_list is not None:
                    if len(el_1_list) > 0:
                        for i, v in enumerate(val["element_list"]):
                            el_2_list = self._structure.select_index(v)
                            cutoff_dist = val["cutoff_list"][i]
                            for j, ind in enumerate(
                                np.array(neighbors.indices, dtype=object)[el_1_list]
                            ):
                                # Only chose those indices within the cutoff distance and which belong
                                # to the species defined in the element_list
                                # i is the index of each bond type, and j is the element index
                                id_el = el_1_list[j]
                                bool_1 = (
                                    np.array(neighbors.distances, dtype=object)[id_el]
                                    <= cutoff_dist
                                )
                                act_ind = ind[bool_1]
                                bool_2 = np.in1d(act_ind, el_2_list)
                                final_ind = act_ind[bool_2]
                                # Get the bond and angle type
                                bond_type = val["bond_type_list"][i]
                                angle_type = val["angle_type_list"][i]
                                # Draw only maximum allowed bonds
                                final_ind = final_ind[: val["max_bond_list"][i]]
                                for fi in final_ind:
                                    bonds_lst.append([id_el + 1, fi + 1])
                                    bond_type_lst.append(bond_type)
                                # Draw angles if at least 2 bonds are present and if an angle type is defined for this
                                # particular set of bonds
                                if (
                                    len(final_ind) >= 2
                                    and val["angle_type_list"][i] is not None
                                ):
                                    angles_lst.append(
                                        [final_ind[0] + 1, id_el + 1, final_ind[1] + 1]
                                    )
                                    angle_type_lst.append(angle_type)

        if len(bond_type_lst) == 0:
            num_bond_types = 0
        else:
            num_bond_types = int(np.max(bond_type_lst))
        if len(angle_type_lst) == 0:
            num_angle_types = 0
        else:
            num_angle_types = int(np.max(angle_type_lst))

        atoms = "Atoms \n\n"

        # format: atom-ID, molecule-ID, atom_type, q, x, y, z
        format_str = "{0:d} {1:d} {2:d} {3:f} {4:f} {5:f} {6:f}"
        el_lst = self.structure.get_chemical_symbols()
        for id_atom, (el, coord) in enumerate(zip(el_lst, coords)):
            atoms += (
                format_str.format(
                    id_atom + 1,
                    self.molecule_ids[id_atom],
                    species_lammps_id_dict[el],
                    q_dict[el],
                    coord[0],
                    coord[1],
                    coord[2],
                )
                + "\n"
            )

        if len(bonds_lst) > 0:
            bonds_str = "Bonds \n\n"
            for i_bond, id_vec in enumerate(bonds_lst):
                bonds_str += (
                    "{0:d} {1:d} {2:d} {3:d}".format(
                        i_bond + 1, bond_type_lst[i_bond], id_vec[0], id_vec[1]
                    )
                    + "\n"
                )
        else:
            bonds_str = "\n"

        if len(angles_lst) > 0:
            angles_str = "Angles \n\n"
            for i_angle, id_vec in enumerate(angles_lst):
                angles_str += (
                    "{0:d} {1:d} {2:d} {3:d} {4:d}".format(
                        i_angle + 1,
                        angle_type_lst[i_angle],
                        id_vec[0],
                        id_vec[1],
                        id_vec[2],
                    )
                    + "\n"
                )
        else:
            angles_str = "\n"
        return (
            self.lammps_header(
                structure=self.structure,
                cell_dimensions=self.simulation_cell(),
                species_lammps_id_dict=species_lammps_id_dict,
                nbonds=len(bonds_lst),
                nangles=len(angles_lst),
                nbond_types=num_bond_types,
                nangle_types=num_angle_types,
            )
            + " \n"
            + atoms
            + "\n"
            + bonds_str
            + "\n"
            + angles_str
            + "\n"
        )

    def structure_charge(self):
        """
        Create atom structure including the atom charges.

        By convention the LAMMPS atom type numbers are chose alphabetically for the chemical species.

        Returns: LAMMPS readable structure.

        """
        species_lammps_id_dict = self.get_lammps_id_dict(self.el_eam_lst)
        atoms = "Atoms\n\n"
        coords = self.rotate_positions(self._structure)
        el_charge_lst = self._structure.get_initial_charges()
        el_lst = self._structure.get_chemical_symbols()
        for id_atom, (el, coord) in enumerate(zip(el_lst, coords)):
            dim = self._structure.dimension
            c = np.zeros(3)
            c[:dim] = coord
            atoms += (
                "{0:d} {1:d} {2:f} {3:.15f} {4:.15f} {5:.15f}".format(
                    id_atom + 1,
                    species_lammps_id_dict[el],
                    el_charge_lst[id_atom],
                    c[0],
                    c[1],
                    c[2],
                )
                + "\n"
            )
        return (
            self.lammps_header(
                structure=self.structure,
                cell_dimensions=self.simulation_cell(),
                species_lammps_id_dict=species_lammps_id_dict,
            )
            + atoms
            + "\n"
        )

    def structure_atomic(self):
        """
        Write routine to create atom structure static file that can be loaded by LAMMPS

        Returns:

        """
        species_lammps_id_dict = self.get_lammps_id_dict(self.el_eam_lst)
        atoms = "Atoms\n\n"
        coords = self.rotate_positions(self._structure)

        el_lst = self._structure.get_chemical_symbols()
        for id_atom, (el, coord) in enumerate(zip(el_lst, coords)):
            dim = self._structure.dimension
            c = np.zeros(3)
            c[:dim] = coord
            atoms += (
                "{0:d} {1:d} {2:.15f} {3:.15f} {4:.15f}".format(
                    id_atom + 1, species_lammps_id_dict[el], c[0], c[1], c[2]
                )
                + "\n"
            )
        return (
            self.lammps_header(
                structure=self.structure,
                cell_dimensions=self.simulation_cell(),
                species_lammps_id_dict=species_lammps_id_dict,
            )
            + atoms
            + "\n"
        )

    def rotate_positions(self, structure):
        """
        Rotate all atomic positions in given structure according to new Prism cell

        Args:
            structure: Atoms-like object. Should has .positions attribute

        Returns:
            (list): List of rotated coordinates
        """
        prism = UnfoldingPrism(self._structure.cell)
        coords = [prism.pos_to_lammps(position) for position in structure.positions]
        return coords

    def rotate_velocities(self, structure):
        """
        Rotate all atomic velocities in given structure according to new Prism cell

        Args:
            structure: Atoms-like object. Should have .velocities attribute.

        Returns:
            (list): List of rotated velocities
        """
        prism = UnfoldingPrism(self._structure.cell)
        vels = [prism.pos_to_lammps(vel) for vel in structure.velocities]
        return vels

    def write_file(self, file_name, cwd=None):
        """
        Write GenericParameters to input file

        Args:
            file_name (str): name of the file, either absolute (then cwd must be None) or relative
            cwd (str): path name (default: None)
        """
        if cwd is not None:
            file_name = posixpath.join(cwd, file_name)

        with open(file_name, "w") as f:
            for line in self._string_input:
                f.write(line)


def write_lammps_datafile(structure, file_name="lammps.data", cwd=None):
    lammps_str = LammpsStructure()
    lammps_str.el_eam_lst = structure.get_species_symbols()
    lammps_str.structure = structure
    lammps_str.write_file(file_name=file_name, cwd=cwd)


def structure_to_lammps(structure):
    """
    Converts a structure to the Lammps coordinate frame

    Args:
        structure (pyiron.atomistics.structure.atoms.Atoms): Structure to convert.

    Returns:
        pyiron.atomistics.structure.atoms.Atoms: Structure with the LAMMPS coordinate frame.
    """
    prism = UnfoldingPrism(structure.cell)
    lammps_structure = structure.copy()
    lammps_structure.set_cell(prism.A)
    lammps_structure.positions = np.matmul(structure.positions, prism.R)
    if structure.velocities is not None:
        lammps_structure.velocities = np.matmul(structure.velocities, prism.R)
    return lammps_structure
