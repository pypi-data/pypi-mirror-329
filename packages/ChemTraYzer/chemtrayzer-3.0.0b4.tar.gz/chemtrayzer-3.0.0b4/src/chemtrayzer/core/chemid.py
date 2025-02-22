
"""Chemical identifiers

This module contains classes for identifying and representing chemical
species and reactions. It also supplies functions for converting to and from
common chemical identifiers such as InChIs and SMILES.
"""
from __future__ import annotations


import re
import warnings
import hashlib
from dataclasses import dataclass, field
import logging
from collections.abc import Iterable, Sequence
import networkx as nx
import rdkit
from rdkit import Chem
from rdkit.Chem import rdmolops

from chemtrayzer.core.periodic_table import PERIODIC_TABLE as PTOE
from chemtrayzer.core.graph import MolGraph
from chemtrayzer.core.coords import Geometry


class RDKitError(Exception):
    """
    Raised when rdkit can not deal with input.
    """

class InchiReadWriteError(Exception):
    """Problem reading or writing InChI strings"""


def split_chemical_formula(formula: str):
    # This regular expression finds elements and their counts
    pattern = re.compile("([A-Z][a-z]*)(\\d*)")
    elements = pattern.findall(formula)

    # Convert elements into a dictionary
    element_dict = {}
    for (element, count) in elements:
        if count == '':
            count = 1
        else:
            count = int(count)
        element_dict[element] = count
    return element_dict


def _rdkit_mol_from_geometry(geo: 'Geometry', charge: int = 0) -> Chem.Mol:
    ''' creates an RDKit Mol object from a geometry

    .. note:: This function should not be used outside of this module in order
    to avoid a dependency on RDKit
    '''
    graph = MolGraph.from_geometry(geo)
    mol = _rdkit_mol_from_geometry_and_graph(geo, graph,
                                             generate_bond_orders=True,
                                             charge=charge)
    return mol


def _rdkit_mol_from_geometry_and_graph(geo: Geometry, graph: MolGraph,
                                       charge:int = 0,
                                       generate_bond_orders=False) -> Chem.Mol:
    """Stereochemistry and Radicals are assigned by RDKit."""
    if generate_bond_orders is True:
        mol = graph.to_mol(generate_bond_orders=generate_bond_orders,
                           charge=charge)

    else:
        mol = Chem.RWMol()

        for idx, (el, coords) in enumerate(zip(geo.atom_types, geo.coords)):
            atom = Chem.Atom(el.symbol)
            atom.SetAtomicNum(el.atomic_nr)
            atom.SetNoImplicit(True)
            # atom.SetNumExplicitHs(0)
            mol.AddAtom(atom)

        # let RdKit figure out bonds
        for a1, a2 in graph.bonds:
            order = graph.get_bond_attribute(a1, a2, "bond_order")
            mol.RemoveBond(a1, a2)
            if int(round(order)) == 1:
                order = Chem.BondType.SINGLE
            elif int(round(order)) == 2:
                order = Chem.BondType.DOUBLE
            elif int(round(order)) == 3:
                order = Chem.BondType.TRIPLE

            mol.AddBond(a1, a2, order=order)  # RDKit uses BondType enumeration

    conf = Chem.Conformer()
    for idx, (el, coords) in enumerate(zip(geo.atom_types, geo.coords)):
        conf.SetAtomPosition(idx, (float(coords[0]),
                                       float(coords[1]),
                                       float(coords[2])))
    mol = mol.GetMol()
    mol.AddConformer(conf)

    Chem.AssignStereochemistry(mol)
    rdmolops.AssignRadicals(mol)
    # mol = Chem.RemoveHs(mol)
    return mol


def _rdkit_mol_from_inchi(inchi: str) -> Chem.Mol:
    rdkit.rdBase.LogToPythonLogger()
    mol = Chem.MolFromInchi(inchi.strip(), sanitize=True, removeHs=False,
                            treatWarningAsError=True)

    if mol is None:
        mol = Chem.MolFromInchi(inchi.strip(), sanitize=False,
                                removeHs=False, treatWarningAsError=True)
        logging.debug("An unusual inchi was used for rdkit Mol "
                      f"creation: {inchi}")

    mol = Chem.AddHs(mol, explicitOnly=True)
    return mol


@dataclass(frozen=True)
class Species:
    '''
    A chemical species, i.e. a molecule, complex, etc. defined by its
    connectivity. Enantiomers are different species.
    This class is frozen, b/c it is essentially supposed to represent an id. If
    the geometry/species, that the id belongs to changes, you should just
    create a new Species object.

    :param id: identifier for the species used within chemtrayzer to identify
               species
    :param inchi: InChI of this species
    :param smiles: SMILES of this species
    '''

    id: str
    inchi: str
    smiles: str

    @classmethod
    def id_from_geometry(cls, geo: Geometry) -> str:
        '''
        Use this method wherever you want to use species ids

        :param geo: geometry of a species
        :return: id of this species
        '''
        # currently we are using InChIKeys as species ids
        mol = _rdkit_mol_from_geometry(geo)
        return cls._id_from_rdkit_mol(mol)

    @classmethod
    def id_from_geometry_and_graph(cls, geo: Geometry, graph: nx.Graph) -> str:
        '''
        Use this method wherever you want to use species ids

        :param graph: networkX graph with "bond_order" edge attribute and
                      "symbol" node attribute
        :param geo: geometry of a species
        :return: id of this species
        '''
        # currently we are using InChIKeys as species ids
        mol = _rdkit_mol_from_geometry_and_graph(geo, graph)
        return cls._id_from_rdkit_mol(mol)

    @classmethod
    def from_geometry_and_graph(cls, geo: Geometry,
                                graph: nx.Graph) -> Species:
        '''
        Use this method wherever you want to use species ids

        :param graph: networkX graph with "bond_order" edge attribute and
                      "symbol" node attribute
        :param geo: geometry of a species
        :return: a species object for this geometry and connectivity
        '''
        mol = _rdkit_mol_from_geometry_and_graph(geo, graph)
        return Species(id=cls._id_from_rdkit_mol(mol),
                       inchi=cls._inchi_from_rdkit_mol(mol),
                       smiles=cls._smiles_from_rdkit_mol(mol))

    @classmethod
    def from_geometry(cls, geo: Geometry) -> 'Species':
        '''
        :param geo: geometry of some species
        :return: a species object with the correct id for this geometry
        '''
        mol = _rdkit_mol_from_geometry(geo)

        return Species(id=cls._id_from_rdkit_mol(mol),
                       inchi=cls._inchi_from_rdkit_mol(mol),
                       smiles=cls._smiles_from_rdkit_mol(mol))

    @classmethod
    def from_inchi(cls, inchi: str) -> 'Species':
        '''
        creates a species object defined by an InChI
        '''
        try:
            mol = _rdkit_mol_from_inchi(inchi)
        except rdkit.Chem.inchi.InchiReadWriteError as err:
            raise InchiReadWriteError(
                            f"RDKit could not read InChI: {inchi}") from err

        return Species(id=cls._id_from_rdkit_mol(mol),
                       inchi=inchi,
                       smiles=cls._smiles_from_rdkit_mol(mol))

    @classmethod
    def from_smiles(cls, smiles: str) -> 'Species':
        '''
        creates a species object from a SMILES
        '''
        rdkit.rdBase.LogToPythonLogger()
        warnings.warn("Generating a Species object from SMILES can lead to "
                     "unexpected results. In our experience, InChIs are more "
                     "reliable and should be used instead.")

        mol = Chem.MolFromSmiles(smiles.strip())
        if mol is None:
            logging.debug("An unusual SMILES was used for rdkit Mol "
                            f"creation: {smiles}. Using RDKit's sanaization"
                            " to fix this....")
            # sanitize=False is used to avoid RDKit errors for molecules
            # with more than the allowed number of valence electrons, e.g.
            # [OH3]
            mol = Chem.MolFromSmiles(smiles.strip(), sanitize=False)

            if mol is None:
                raise RDKitError(f"RDKit could not create a molecule from "
                                 f"SMILES: {smiles}")

        return Species(id=cls._id_from_rdkit_mol(mol),
                       inchi=cls._inchi_from_rdkit_mol(mol),
                       smiles=smiles)

    @property
    def composition(self) -> dict[str, int]:
        '''maps element symbols to the number of atoms of this element.
        For example for methane, this property is `{'C': 1, 'H': 4}`'''
        rdkit.rdBase.LogToPythonLogger()
        mol = _rdkit_mol_from_inchi(self.inchi)

        formula = Chem.rdMolDescriptors.CalcMolFormula(mol)
        # for atom_id in range(mol.GetNumAtoms()):
        #    atom = mol.GetAtomWithIdx(atom_id)
        #    elem = PTOE[atom.GetAtomicNum()].symbol
        #    if elem not in composition:
        #        composition[elem] = 1
        #    else:
        #        composition[elem] += 1
        composition = split_chemical_formula(formula)
        return composition

    @property
    def molecular_weight(self):
        '''molecular weight of this geometry [amu]'''
        mw = 0.0

        for symbol, amount in self.composition.items():
            elem = PTOE[symbol]
            mw += elem.mass * amount

        return mw

    def guessed_spin(self) -> int():
        '''
        guesses the spin multiplicity based on the inchi property of the
        Species using Rdkit
        '''
        mol = _rdkit_mol_from_inchi(self.inchi)

        def calculate_unpaired_electrons(molecule: Chem.Mol) -> int:
            num_unpaired_electrons = 0
            Chem.AssignRadicals(molecule)
            molecule_new = Chem.MolFromSmiles(Chem.MolToSmiles(molecule))
            for atom in molecule_new.GetAtoms():
                num_unpaired_electrons += atom.GetNumRadicalElectrons()

            return num_unpaired_electrons

        num_unpaired_electrons = calculate_unpaired_electrons(mol)

        spin_multiplicity = num_unpaired_electrons + 1

        guessed_spin = spin_multiplicity

        return guessed_spin

    @property
    def formula(self) -> str:
        """
        Returns a molecular formula, e.g. C6H12O6.
        :return: the molecular formula for this species
        """
        return ''.join(k + str(self.composition[k])
                       for k in sorted(self.composition.keys()))

    @classmethod
    def _id_from_rdkit_mol(cls, mol: Chem.Mol) -> str:
        '''create an InChIKey from an RDKit Mol object '''
        return Chem.MolToInchiKey(mol)

    @classmethod
    def _inchi_from_rdkit_mol(cls, mol: Chem.Mol) -> str:
        '''create an InChI from an RDKit Mol object '''
        return Chem.MolToInchi(mol)

    @classmethod
    def _smiles_from_rdkit_mol(cls, mol: Chem.Mol) -> str:
        '''create a SMILES from an RDKit Mol object '''
        try:
            mol = Chem.RemoveHs(mol)
        except Chem.rdchem.AtomValenceException:
            # To allow species like [OH3] which can occur in ReaxFF simulations
            logging.debug(
                f"Accepted very unusual valence: {Chem.MolToSmiles(mol)}")

        return Chem.MolToSmiles(mol)

    def __str__(self) -> str:
        return self.inchi

    def __format__(self, __format_spec: str) -> str:
        return self.inchi

    def __hash__(self) -> int:
        return hash(self.id)

    def __lt__(self, other: 'Species') -> bool:
        return self.id < other.id

    def __le__(self, other: 'Species') -> bool:
        return self.id <= other.id

    def __eq__(self, other: 'Species') -> bool:
        return self.id == other.id

    def __ne__(self, other: 'Species') -> bool:
        return self.id != other.id

    def __gt__(self, other: 'Species') -> bool:
        return self.id > other.id

    def __ge__(self, other: 'Species') -> bool:
        return self.id >= other.id

    def __rmul__(self, nu: int) -> _StoichCollection:
        if isinstance(nu, int):
            return _StoichCollection([self]*nu)
        else:
            return NotImplemented

    def __rshift__(self, other: Species|_StoichCollection) -> Reaction:
        if isinstance(other, Species):
            return Reaction(reactants=[self], products=[other])
        elif isinstance(other, _StoichCollection):
            return Reaction(reactants=[self], products=other.species)
        else:
            return NotImplemented

    def __add__(self, other: Species|_StoichCollection) -> _StoichCollection:
        if isinstance(other, Species):
            return _StoichCollection([self, other])
        elif isinstance(other, _StoichCollection):
            other.species.append(self)
            return other
        else:
            return NotImplemented

    def __repr__(self) -> str:
        return self.smiles

@dataclass
class _StoichCollection(Sequence[Species]):
    """Helper class for simple construction of reaction objects"""
    species: list[Species] = field(default_factory=list)

    def __rshift__(self, other: Species|_StoichCollection) -> Reaction:
        if isinstance(other, Species):
            return Reaction(reactants=self.species, products=[other])
        elif isinstance(other, _StoichCollection):
            return Reaction(reactants=self.species, products=other.species)
        else:
            return NotImplemented

    def __add__(self, other: Species|_StoichCollection) -> _StoichCollection:
        if isinstance(other, Species):
            self.species.append(other)
            return self
        elif isinstance(other, _StoichCollection):
            self.species.extend(other.species)
            return self
        else:
            return NotImplemented

    def __len__(self) -> int:
        return len(self.species)

    def __getitem__(self, i: int) -> Species:
        return self.species[i]

# frozen, b/c otherwise you would have to change the id, when adding stuff to
# reactants and products
@dataclass(frozen=True, init=False)
class Reaction:
    ''' minimal class to represent a reaction
    The id of a Reaction is determined on the product and reactant ids. It is
    a Sha224 hash stored as string in hexadecimal representation.

    Reactions can be created with operators from species objects. This is may
    be a bit slower than using the constructor.

    .. code::

        CH3 =  Species.from_inchi('InChI=1S/CH3/h1H3')
        OH = Species.from_inchi('InChI=1S/HO/h1H')
        CH3OH = Species.from_inchi('InChI=1S/CH4O/c1-2/h2H,1H3 ')
        reaction = CH3 + OH >> CH3OH

    :param id: reaction id is based on InChIKeys in the current version
    '''
    id: str
    reactants: tuple[Species, ...]
    products: tuple[Species, ...]

    def __init__(self, reactants: Iterable[Species],
                 products: Iterable[Species]) -> None:

        # this function is needed for the sorting
        def get_id(species: Species):
            return species.id

        # this is a bit hacky, but it is necessary because frozen=True.
        # essentially `self.reactants =  tuple(sorted(reactants, key=get_id)`:
        object.__setattr__(self, "reactants",
                           tuple(sorted(reactants, key=get_id))
                           )

        # essentially `self.products =  tuple(sorted(products, key=get_id)`:
        object.__setattr__(self, "products",
                           tuple(sorted(products, key=get_id))
                           )

        # include a separator, s.t. reactions A+B->C and A->B+C produce
        # different hashes
        SEPARATOR = b'spearator'

        # now hash all reactant and product keys to get the reaction id
        hasher = hashlib.sha224()

        for reactant in self.reactants:
            hasher.update(reactant.id.encode('utf-8'))
        hasher.update(SEPARATOR)
        for product in self.products:
            hasher.update(product.id.encode('utf-8'))

        # essentially `self.id = hasher.hexdigest()))`
        object.__setattr__(self, "id", hasher.hexdigest())

    @classmethod
    def from_geometries(cls, reactants: Iterable[Geometry],
                        products: Iterable[Geometry]) -> 'Reaction':
        '''
        :param reactants: reactant geometries used for generating the reaction
                          id
        :param products: product geometries used for generating the reaction id
        :return: reaction object based on reactant and product geometries
        '''
        return cls(reactants=[
            Species.from_geometry(geo)
            for geo in reactants
        ], products=[
            Species.from_geometry(geo)
            for geo in products
        ])

    def reverse(self) -> 'Reaction':
        ''':return: the reverse reaction'''
        return Reaction(self.products, self.reactants)

    def __hash__(self) -> int:
        return hash(self.id)

    def __lt__(self, other: 'Reaction') -> bool:
        return self.id < other.id

    def __le__(self, other: 'Reaction') -> bool:
        return self.id <= other.id

    def __eq__(self, other: 'Reaction') -> bool:
        return self.id == other.id

    def __ne__(self, other: 'Reaction') -> bool:
        return self.id != other.id

    def __gt__(self, other: 'Reaction') -> bool:
        return self.id > other.id

    def __ge__(self, other: 'Reaction') -> bool:
        return self.id >= other.id

    def __str__(self) -> str:
        reactants_str = " + ".join(r.smiles for r in self.reactants)
        products_str = " + ".join(p.smiles for p in self.products)
        return f"{reactants_str} >> {products_str}"

    def __repr__(self) -> str:
        reactants_str = " + ".join(r.smiles for r in self.reactants)
        products_str = " + ".join(p.smiles for p in self.products)
        return f"{reactants_str} >> {products_str}"
