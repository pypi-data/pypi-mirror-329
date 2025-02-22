# ruff: noqa
import warnings
import logging
from collections import Counter, defaultdict
from typing import Dict, List, Union, Iterable, Tuple, overload, Optional
from chemtrayzer.core.graph import MDMoleculeNetwork, MolGraph
import numpy as np

from numpy import pi, arccos, clip, dot
from numpy.linalg import norm
from scipy.optimize import leastsq
from scipy.special import lambertw, gammaincc

import chemtrayzer.core.md
from chemtrayzer.core.chemid import Species, Reaction
from chemtrayzer.core.coords import Geometry, TSGeometry, ChainOfStates
# TODO move detection algorithm classesm such as MDMoleculem from core.md here
from chemtrayzer.core.md import (
    BoxType,
    RateConstantRecord,
    TrajectoryParser,
    MDMetadata,
    Trajectory,
    MDMolecule
)


###############################################################################
# CTY Reaction Detection
###############################################################################

class ReactiveEvent:
    """
    Represents a chemical reaction event with bond order changes.

    The relation of bonds to atoms in the `geometries` attribute is determined
    using the IDs in the `atom_ids` attribute. Bonds, geometries, and atom IDs
    are stored in ascending order. The index in the `atom_ids` array
    corresponds to the index in the geometry. For example, `atom_ids[0]` stores
    the ID of the first atom in the `geometries` attribute. These IDs can then
    be used to determine the bond orders for each atom in the geometry.
    See example below

    Due to the reaction path margin, the first and last frames may be offset
    from the actual reactant and product states to capture the full reaction
    path.

    Example:
        If geometries.atom_types = ['C','H','O'] and atom_ids=[2,5,7], then:
        - atom_types[0], Carbon atom has ID 2
        - atom_types[1], Hydrogen atom has ID 5
        - atom_types[2], Oxygen atom has ID 7

        If path_bond_orders={(2,5): 1.0, (5,7): 1.0} then:
        - Atoms 2 (C) and 5 (H) are connected with a single bond
        - Atoms 5 (H) and 7 (O) are connected with a single bond
        - Atoms 2 (C) and 7 (O) are not directly connected

    :param reaction_time: Time when the reaction occurred in fs
    :param atom_ids: Ordered list of IDs of atoms involved in the reaction,
                     either as part of the reactants or products. The IDs are
                     derived from the parent trajectory.
    :param geometries: Chain of states object containing a snippet from the
                       trajectory that contains all reactant and product atoms
                       along the reaction path. Atoms are sorted by their
                       corresponding atom_ids. E.g. Atom/coords 0 corresponds
                       to ID at atom_ids[0].
    :param reaction: Associated reaction object. E.g. A + B >> C, where A, B
                     and C are chemtrayzer species objects.
    :param path_bond_orders: Time series (list) of dictionaries, mapping tuples
                             of atom indices (i,j), with i < j, to their bond
                             orders. Only contains entries for connected
                             atoms. Note that the atom indices are based on the
                             IDs in the atom_ids list. Be aware that Atom IDs
                             are derived from the parent trajectory and are
                             unrelated to the index/position in the geometries
                             object. See example below.
    :param bond_changes: Dictionary containing lists of bond changes:
                        - 'formed': bonds formed during reaction
                        - 'broken': bonds broken during reaction
                        - 'unchanged': bonds that remain constant
                        Each bond is a tuple of atom indices (i,j) with i < j.
                        Does not include intermediate bonds that are temporarily
                        formed or broken during the reaction.
    :param reactant_geometries: Dictionary mapping Species or Reaction objects
                               to a list of their corresponding geometries.
                               Contains the geometries of each reactant molecule
                               detected during the reaction.
    :param product_geometries: Dictionary mapping Species or Reaction objects
                               to a list of their corresponding geometries.
                               Contains the geometries of each product molecule
                               detected during the reaction.
    :param ts_geo: Geometry object representing the transition state structure
                   of the reaction, taken at the frame where the reaction is
                   detected to occur. Contains the atomic coordinates at the
                   approximate transition state geometry.
    """

    reaction_time: float
    atom_ids: list[int]
    geometries: ChainOfStates
    reaction: Reaction
    path_bond_orders: list[Dict[Tuple[int, int], float]]
    bond_changes: dict[str, list[tuple[int, int]]]

    #TODO: find a better way to store ts_geo and product_geometries
    #TODO: also store reactant geometries
    reactant_geometries: defaultdict[Union[Species, Reaction], List[Geometry]]
    product_geometries: defaultdict[Union[Species, Reaction], List[Geometry]]
    ts_geo: Geometry

    def __init__(
        self,
        reaction_time,
        atom_ids,
        geometries,
        reaction,
        path_bond_orders,
        bond_changes,
        reactant_geometries,
        product_geometries,
        ts_geo,
    ):
        self.reaction_time = reaction_time
        self.geometries = geometries
        self.reaction = reaction
        self.atom_ids = atom_ids
        self.path_bond_orders = path_bond_orders
        self.bond_changes = bond_changes
        self.reactant_geometries = reactant_geometries
        self.product_geometries = product_geometries
        self.ts_geo = ts_geo

    def __repr__(self):
        """
        String representation showing reaction and reaction time.
        """
        return (f"ReactiveEvent(reaction={self.reaction}, "
                f"@ {self.reaction_time}fs)")


class ReactionDetector:
    """
    Class for detecting and extracting reactions and their geometries from a MD trajectory

    :param trajectory: CTY3 Trajectory object
    :param _bond_initial_threshold: bonds with orders above this value are considered existing in the first frame of the trajectory
    :param _bond_breaking_threshold: bonds with orders decreasing below this value are considered breaking
    :param _bond_forming_threshold: bonds with orders increasing above this value are considered forming
    :param _molecule_stable_time: detected molecules with lifetimes below this value are considered unstable intermediates in a reaction and are never reported as products
    :param mdreactions: list of detected reactions. Each reaction is a 2-tuple of tuples of MDMolecules (reactants, products)
    :param _initial_mdmolecules: list of MDMolecules in the first frame of the trajectory
    :param initial_composition: composition of the initial frame of the trajectory
    :param _mdmolecule_network: directed graph of MDMolecules and their connections

    :ivar mdreactions: internally used list of detected reactions. Reactions are a 2-tuple of tuples of MDMolecules, reactants and products.
    :ivar _initial_mdmolecules: the list of MDMolecules in the first frame of the trajectory
    :ivar initial_composition: the composition of the initial frame of the trajectory
    :ivar _mdmolecule_network: a directed graph of MDMolecules and their connections
    """

    def __init__(self,
                 parser: TrajectoryParser,
                 bond_initial_threshold: float = 0.5,
                 bond_breaking_threshold: float = 0.3,
                 bond_forming_threshold: float = 0.8,
                 molecule_stable_time: float = 3,
                 reaction_path_margin: int = 20):

        self._parser = parser
        self._bond_initial_threshold = bond_initial_threshold
        self._bond_breaking_threshold = bond_breaking_threshold
        self._bond_forming_threshold = bond_forming_threshold
        self._molecule_stable_time = molecule_stable_time
        self._molecule_stable_frames = None
        self._reaction_path_margin = reaction_path_margin
        #
        self.metadata: MDMetadata = None
        self.current_frame_number: int = 0
        self._first_frame_number: int = None
        self._current_graph: MolGraph = None
        self._atom_to_mol_dict: Dict[int, MDMolecule] = {}
        #
        self._initial_mdmolecules: list[MDMolecule] = []
        self.initial_composition: dict[Species, int] = {}
        self._mdmolecule_network: MDMoleculeNetwork = MDMoleculeNetwork()
        self._trajectory_buffer: Dict[int, Trajectory] = {}
        #
        self.reactive_events: list[ReactiveEvent] = []


    def detect(self, n_frames=-1) -> None:
        """
        Detects reactions from an MD trajectory and creates ReactiveEvents.


        The detection process follows these main steps:
        1. Parse trajectory frames and validate data integrity
        2. Initialize metadata and validate simulation box configuration
        3. Process each frame to identify molecular changes:
           - Track bond formations and breaks
           - Create new molecules when connectivity changes
           - Update molecule network with new relationships
        4. Extract completed reactions from network
        5. Create ReactiveEvents for valid reactions
        6. Clean up processed trajectory data

        :param n_frames: How many frames to process. Default is all (n_frames=-1).
        """
        trajectory = self._parse_trajectory(n_frames)
        if trajectory is None:
            return

        self._initialize_trajectory_data(trajectory)
        self._validate_box_configuration()

        start_frame = self._initialize_graph_if_needed(trajectory)
        self._process_trajectory_frames(trajectory, start_frame)
        self._cleanup_trajectories()

    def _parse_trajectory(self, n_frames: int) -> Optional[Trajectory]:
        """
        Attempts to parse the trajectory frames using the configured parser.

        :param n_frames: Number of frames to parse (-1 for all frames)
        :return: Parsed trajectory or None if parsing failed
        """
        try:
            trajectory = self._parser.parse(n_frames)
            logging.info(f'Reading {"all" if n_frames == -1 else n_frames} frames...')
            self._trajectory_buffer[self.current_frame_number] = trajectory
            return trajectory
        except Exception as e:
            logging.error(
                f"Failed to parse trajectory in ReactionDetector.detect(): "
                f"Parser '{type(self._parser).__name__}' "
                f"raised {type(e).__name__}: {e}"
            )
            return None

    def _initialize_trajectory_data(self, trajectory: Trajectory) -> None:
        """
        Initializes metadata and frame number tracking if not already set.
        Also computes the number of frames needed for molecule stability.

        :param trajectory: The parsed trajectory
        """
        if self.metadata is None:
            self.metadata = trajectory.metadata
        if self._first_frame_number is None:
            self._first_frame_number = trajectory.first_timestep

        self._molecule_stable_frames = self._molecule_stable_time / (
            self.metadata.timestep * self.metadata.sampling_frequency)

    def _validate_box_configuration(self) -> None:
        """
        Validates that the simulation box configuration is supported.

        :raises NotImplementedError: If box type is not orthogonal
        """
        if self.metadata.initial_box.box_type != BoxType.ORTHOGONAL:
            raise NotImplementedError('Only orthogonal boxes are supported.')

    def _initialize_graph_if_needed(self, trajectory: Trajectory) -> None:
        """
        Initialize the current graph if it's the first frame.
        """
        if self._current_graph is None:

            # remove bonds below threshold
            self._current_graph = self._remove_low_bond_orders(trajectory.graphs[0].copy())

            # detect initial atom clusters (hopefully molecules)
            for component in self._current_graph.connected_components():
                subgraph = self._current_graph.subgraph(component)
                mol = MDMolecule(self.current_frame_number, subgraph)
                self._initial_mdmolecules.append(mol)
                # initialize mol container
                for atom_id in subgraph.atoms:
                    self._atom_to_mol_dict[atom_id] = mol

            # update the molecule network with the initial molecules
            self._update_mdmolecule_network(self._initial_mdmolecules)

            # get the initial composition
            self.initial_composition = self._composition_from_mdmolecules(
                                                    self._initial_mdmolecules)

            # increase frame counter, because the very first frame cannot have
            #  bond changes
            self.current_frame_number += 1

            return True
        else:
            return False

    def _process_trajectory_frames(self, trajectory: Trajectory, start_frame: int) -> None:
        """
        Process each frame in the trajectory to detect molecular changes.
        Iterates through trajectory frames, detecting and tracking molecular changes
        by analyzing bond formations and breaks.

        :param trajectory: The trajectory to process
        """
        logging.info('Processing frames to identify molecular changes...')

        # Process each frame sequentially
        for next_graph in trajectory.graphs[start_frame:]:
            new_mdmolecules = self._process_single_frame(next_graph)
            self._build_reaction_network(new_mdmolecules)

        logging.debug(f'Found {len(self.reactive_events)} new molecular entities.')

    def _process_single_frame(self, next_graph: MolGraph) -> List[MDMolecule]:
        """
        Process a single frame to detect molecular changes.

        :param next_graph: The graph of the next frame to process
        :return: List of new molecules detected in this frame
        """
        # Compare current to next trajectory frame
        added_bonds, removed_bonds, changed_bonds = self._get_bond_difference_from_two_graphs(
            self._current_graph, next_graph
        )

        # Skip if no relevant changes
        new_connectivity = added_bonds + removed_bonds
        if not new_connectivity:
            self.current_frame_number += 1
            return []

        # Update molecular graph with changes
        self._update_current_graph(added_bonds, removed_bonds, changed_bonds)

        # Create new molecules based on connectivity changes
        new_mdmolecules = self._get_new_mdmols_from_frame(new_connectivity)
        self.current_frame_number += 1

        return new_mdmolecules

    def _build_reaction_network(self, new_mdmolecules: List[MDMolecule]) -> None:
        """
        Build and process the reaction network from detected molecules.
        Creates and stores ReactiveEvents for completed reactions.

        :param new_mdmolecules: List of new molecules to add to the network
        """
        self._update_mdmolecule_network(new_mdmolecules)
        md_reactions = self._get_mdreactions_from_mdmolecule_network()

        # Process each reaction to create ReactiveEvents
        reactive_events = []
        for reactants, products in md_reactions:
            event = self._process_reaction(reactants, products)
            if event:
                reactive_events.append(event)

        self.reactive_events += sorted(
            reactive_events,
            key=lambda x: (
                x.reaction_time,
                tuple(sorted(x.bond_changes["formed"])),
                tuple(sorted(x.bond_changes["broken"])),
            ),
        )

    def _analyze_bond_changes(
        self,
        reactants: list[MDMolecule],
        products: list[MDMolecule]
    ) -> tuple[list[tuple[int, int]], list[tuple[int, int]], list[tuple[int, int]]]:
        """Extracts the formed, broken and unchanged bonds from reactants and products.

        Each bond is represented as a sorted tuple of two integer atom indices.
        The function compares bonds present in reactants and products to find
        which bonds were formed, broken, or remained unchanged.

        :param reactants: List of reactant molecules
        :param products: List of product molecules
        :return: A tuple containing:
                - List of formed bonds (sorted tuples of atom indices)
                - List of broken bonds (sorted tuples of atom indices)
                - List of unchanged bonds (sorted tuples of atom indices)
        """
        reac_bonds = set()
        prod_bonds = set()

        for reac in reactants:
            reac_bonds.update(
                tuple(sorted(bond)) for bond in reac.graph.bonds
            )
        for prod in products:
            prod_bonds.update(
                tuple(sorted(bond)) for bond in prod.graph.bonds
            )

        formed = sorted(prod_bonds - reac_bonds)
        broken = sorted(reac_bonds - prod_bonds)
        unchanged = sorted(reac_bonds & prod_bonds)

        return {"formed": formed, "broken": broken, "unchanged": unchanged}

    @overload
    def _get_geometries(
        self, frame_numbers: int, atomids, active_atoms: None=None
    ) -> Geometry: ...

    @overload
    def _get_geometries(
        self, frame_numbers: Iterable[int], atomids, active_atoms: None=None
    ) -> list[Geometry]: ...

    @overload
    def _get_geometries(
        self, frame_numbers: Iterable[int], atomids,
        active_atoms: Iterable[int]=None
    ) -> list[TSGeometry]: ...

    def _get_geometries(self, frame_numbers, atomids, active_atoms=None
                ) -> list[TSGeometry]|list[Geometry]|Geometry:
        """
        Extract molecular geometries from trajectory frames.

        This method has three overloaded behaviors:
        1. Single frame, no active atoms -> Returns Geometry
           Used for getting snapshot of molecular structure
        2. Multiple frames, no active atoms -> Returns List[Geometry]
           Used for tracking molecular motion over time
        3. Multiple frames, with active atoms -> Returns List[TSGeometry]
           Used for tracking reaction transition states

        The geometries are automatically unbroken across periodic boundaries
        and shifted to maintain molecular integrity.

        :param frame_numbers: Single frame number or list of frame numbers
        :param atomids: List of atom IDs to extract
        :param active_atoms: Optional list of atoms involved in reaction
        :return: Geometry, List[Geometry], or List[TSGeometry] depending on inputs
        """
        return_geo = False
        if type(frame_numbers) == int:
            frame_numbers = [frame_numbers]
            return_geo = True

        sorted_ids = sorted(atomids)
        reaction_path = []
        for i in frame_numbers:
            read_from = self._find_trajectory_index(i)
            traj = self._trajectory_buffer[read_from]

            # trajectories/ChainOfStates frame indices start from 0
            geo = traj.get_geometry(i - read_from, sorted_ids)

            if active_atoms:
                reaction_path.append(TSGeometry.from_geometry(
                                                    geo, active=active_atoms))
            else:
                reaction_path.append(geo)

        # shift the first geo away from the box limits
        shift = reaction_path[0].unbreak_molecule(
                    tuple(np.diagonal(self.metadata.initial_box.box_vectors)),
                    self.metadata.initial_box.pbc,
                    zero_com=True)

        # shift/unbreak the whole path except the first geo (is already shifted)
        if len(reaction_path) > 1:
            for geo in reaction_path[1:]:
                geo.coords += shift

        if return_geo:
            return reaction_path[0]
        else:
            return reaction_path

    @overload
    def _get_bond_orders(
        self, frame_numbers: int, active_atoms: List[int]
    ) -> Dict[Tuple[int, int], float]: ...

    @overload
    def _get_bond_orders(
        self, frame_numbers: Iterable[int], active_atoms: List[int]
    ) -> List[Dict[Tuple[int, int], float]]: ...

    #TODO: needs tests
    def _get_bond_orders(
        self, frame_numbers, active_atoms, mapping: dict[int,int]=None
    ) -> Dict[Tuple[int, int], float] | List[Dict[Tuple[int, int], float]]:
        """Extract bond orders for all bonds between active atoms from
        trajectory frames.

        :param frame_numbers: Single frame number or list of frame numbers
        :type frame_numbers: Union[int, Iterable[int]]
        :param active_atoms: List of atom indices to get bond orders between
        :type active_atoms: List[int]
        :param mapping: Optional mapping from parent system atom IDs to
                        subsystem IDs
        :type mapping: Dict[int, int]
        :return: Single dictionary or list of dictionaries mapping bond tuples
                to bond orders
        :rtype: Union[Dict[Tuple[int, int], float], List[Dict[Tuple[int, int],
                float]]]
        """
        if not isinstance(active_atoms, set):
            active_atoms_set = set(active_atoms)
        else:
            active_atoms_set = active_atoms

        return_dict = isinstance(frame_numbers, int)
        frame_numbers = [frame_numbers] if return_dict else frame_numbers

        bond_orders_by_frame = []
        for i in frame_numbers:
            read_from = self._find_trajectory_index(i)
            frame_graph = self._trajectory_buffer[read_from].graphs[i - read_from]

            frame_bond_orders = {}
            for bond in frame_graph.bonds:
                if bond[0] in active_atoms_set or bond[1] in active_atoms_set:
                    bo = frame_graph.get_bond_attribute(*bond, 'bond_order')
                    if mapping is not None:
                        mapped_bond = tuple(sorted(mapping[b] for b in bond))
                        frame_bond_orders[mapped_bond] = bo
                    else:
                        frame_bond_orders[bond] = bo

            bond_orders_by_frame.append(frame_bond_orders)

        return bond_orders_by_frame[0] if return_dict else bond_orders_by_frame

    def _frame_to_time(self, frame_number) -> float:
        """
        Convert a frame number to actual simulation time in femtoseconds.

        Time = (first_frame + frame_number) * sampling_frequency * timestep

        :param frame_number: Frame number in the trajectory
        :return: Simulation time in femtoseconds
        """
        # Add offset from first frame number in trajectory
        frame_offset = self._first_frame_number + frame_number

        # Convert to actual simulation frame by multiplying with sampling freq
        # E.g. if we only sample every 10th frame, multiply by 10
        simulated_frame_number = frame_offset*self.metadata.sampling_frequency

        # Convert frame number to time by multiplying with timestep (in fs)
        return simulated_frame_number * self.metadata.timestep

    def _remove_low_bond_orders(self, graph: MolGraph):
        """
        Removes all bonds from a MolGraph that have a bond order less than specified by self._bond_initial_threshold.
        :param graph: a graph of an MD frame
        :return: the graph without bond orders less than self._bond_initial_threshold
        """
        # use initial threshold. This cannot add bonds, only remove
        for u, v in graph.bonds:
            bond_order = graph.get_bond_attribute(u, v, 'bond_order')
            if bond_order < self._bond_initial_threshold:
                graph.remove_bond(u, v)
        return graph

    def _get_bond_difference_from_two_graphs(self, graph: MolGraph, next_graph: MolGraph):
        """
        Find bond changes between two consecutive molecular graphs using hysteresis-based detection.

        Uses configurable thresholds to detect bond formation and breaking:
        - Bond formation: bond order increases above _bond_forming_threshold
        - Bond breaking: bond order decreases below _bond_breaking_threshold
        - Bond order changes: detects transitions between single/double/triple bonds

        The hysteresis approach (different thresholds for formation/breaking) helps
        prevent oscillation in bond detection near the threshold values.

        :param graph: First MolGraph (current frame)
        :param next_graph: Second MolGraph (next frame)
        :return: Three lists of (bond, bond_order) tuples for added, removed, and
                changed bonds. Bond is tuple of (atom1_id, atom2_id).
        """
        edges_in_both_graphs = set(graph.bonds) | set(next_graph.bonds)

        added_edges_list = []
        removed_edges_list = []
        changed_edges_list = []

        for bond in edges_in_both_graphs:

            bo_1 = graph.get_bond_attribute(*bond, attr='bond_order') if graph.has_bond(*bond) else 0
            bo_2 = next_graph.get_bond_attribute(*bond, attr='bond_order') if next_graph.has_bond(*bond) else 0

            # hysteresis-like event detection
            # bond forms
            # covers also double bond/triple/etc. bond forming
            if bo_1 < self._bond_forming_threshold < bo_2 and bond not in graph.bonds:
                bo_guess = 1 + int(bo_2 - self._bond_forming_threshold)
                added_edges_list.append((bond, bo_guess))
                # graph.add_bond(bond[0], bond[1], bond_order=bo_guess)

            # bond breaks
            elif bo_1 > self._bond_breaking_threshold > bo_2 and bond in graph.bonds:
                removed_edges_list.append((bond, 0))

            # single to double bond
            elif bo_1 < 1 + self._bond_forming_threshold < bo_2:
                changed_edges_list.append((bond, 2))

            # double to single bond
            elif bo_1 > 1 + self._bond_breaking_threshold > bo_2:
                changed_edges_list.append((bond, 1))

            # triple bond and higher
            elif 2 + self._bond_forming_threshold < bo_2:
                bo_guess = 1 + int(bo_2 - self._bond_forming_threshold)
                changed_edges_list.append((bond, bo_guess))

        return added_edges_list, removed_edges_list, changed_edges_list

    def _get_oldest_frame_in_mdmol_network(self) -> int:
        """
        Finds the lowest start frame number of all molecules that still remain in the MDMolecule network.
        Used to determine how many frames should be retained for geometry extraction.
        :return:
        """
        oldest_frame = self.current_frame_number
        for (mol, molid) in self._mdmolecule_network.nodes:
            oldest_frame = min(oldest_frame, mol.end_frame())
        return oldest_frame

    def _cleanup_trajectories(self):
        '''
        Delete trajectories from the buffer which are not needed anymore, i.e.,
        they only contain frame numbers that have been processed.
        '''
        # which frame geometries are still needed is dependent on what reactions
        # are still in the temporary network
        lowest_needed_frame_number = self._get_oldest_frame_in_mdmol_network() - self._reaction_path_margin
        lowest_needed_trajectory_key = self._find_trajectory_index(lowest_needed_frame_number)

        # dispose of all trajectories with lower frame numbers than the lowest needed one
        for first_frame_number in sorted(self._trajectory_buffer):
            if first_frame_number < lowest_needed_trajectory_key:
                logging.info('Removing trajectory data earlier than %f fs from'
                             ' memory.', self._frame_to_time(first_frame_number))
                del(self._trajectory_buffer[first_frame_number])
            else:
                break

    def _get_geometry_and_graph_for_mdmolecule(
            self, mol: MDMolecule, timestep:int|None=None
        ) -> tuple[Geometry, MolGraph]:
        """
        Extract the geomertry and the graph of a MDMolecule from the trajectory.
        If no timestep is given, a step from the middle of a molecules lifetime is taken.
        Reconstructs (unbreaks) the molecule when it is broken by the boundary.
        :param mol: the MDMolecule
        :param timestep: the frame number, or None
        :return: Tuple[Geometry, Graph]
        """
        if timestep is None:
            # take a frame from the molecules lifetime,
            # but not too close to the end or start frame, because it's far away from equilibrium there
            # and not further away from its end frame than reaction_path_margin, because the xyz buffer might have been cleared already
            # note: end_frame can be infinite, thus min()
            ultimative_frame_number = min(mol.end_frame(), self.current_frame_number)
            timestep1 = (mol.start_frame + ultimative_frame_number) // 2
            timestep = max(timestep1, ultimative_frame_number - self._reaction_path_margin // 2)
        sorted_ids = sorted(mol.atoms())
        mol_geometry = self._get_geometries(timestep, sorted_ids)
        mol_graph = mol.graph.relabel_atoms(mapping=dict((old, new) for new, old in enumerate(sorted_ids)), copy=True)

        return mol_geometry, mol_graph

    def _find_trajectory_index(self, frame_number) -> int:
        """
        Finds the trajectory in the trajectory buffer which contains the requested frame number.
        The trajectory buffer is a dictionary where keys are the smallest frame number of the trajectory
        :return: key of the trajectory
        """
        trajectory_keys = sorted(self._trajectory_buffer)

        read_from = trajectory_keys[0]
        for first_frame_number in trajectory_keys:
            if first_frame_number > frame_number:
                break
            read_from = first_frame_number

        return read_from

    def _composition_from_mdmolecules(self, mols: list[MDMolecule]
                                      ) -> dict[Species, int]:
        """
        compute the composition for a given set of MDMolecules
        :return: Species and their number in mols
        """
        species = []
        for mol in mols:
            geo, graph = self._get_geometry_and_graph_for_mdmolecule(
                                        mol,
                                        self.current_frame_number)
            species.append(Species.from_geometry_and_graph(geo, graph))

        return Counter(species)

    def _update_current_graph(self, added_bonds: Iterable[Tuple[Tuple[int, int], float]], removed_bonds: Iterable[Tuple[Tuple[int, int], float]], changed_bonds: Iterable[Tuple[Tuple[int, int], float]]):
        """
        Change connections in self._current_graph according to arguments.
        :param added_bonds: Lists new bonds
        :param removed_bonds: Lists old bonds
        :param changed_bonds: Lists bonds that only changed their order
        """
        for bond, bond_order in added_bonds:
            self._current_graph.add_bond(bond[0], bond[1], bond_order=bond_order)
        for bond, bond_order in removed_bonds:
            self._current_graph.remove_bond(bond[0], bond[1])
        for bond, bond_order in changed_bonds:
            self._current_graph.set_bond_attribute(*bond, 'bond_order', bond_order)

    def _get_new_mdmols_from_frame(self, new_connectivity: Iterable[Tuple[Tuple[int, int], float]]) -> List[MDMolecule]:
        """
            Finds or creates atom clusters (MDMolecules) that participate in a change in connectivity, as passed by argument.
            Direct connections between MDMolecules are stored within the MDMolecules as precursors (.predecessors) and follow-up products (.successors).
            This allows the continuous build-up of a MDMolecule network.

            Technical Details:
            The MDMolecules that existed before this change are accessible via self._atom_to_mol_dict[atom_id].
            The MDMolecules that exist after this change will be created from self._current_graph.
            In the end, self._atom_to_mol_dict[atom_id] is updated with the new MDMolecules and matches self._current_graph.
        """
        used_atom_ids = set()
        new_mdmolecules = []

        # loop bond changes per frame
        for (atom_id_1, atom_id_2), _ in new_connectivity:

            # molecules already found?
            if atom_id_1 in used_atom_ids and atom_id_2 in used_atom_ids:
                continue

            # idea: only run sym_diff loop, init sym_diff with atom_id_1
            sym_diff = {atom_id_1}
            reactants = tuple()
            products = tuple()
            used_product_atom_ids = set()
            used_reactant_atom_ids = set()

            # this loop runs until all atoms of participating mols in a connectivity change
            # have been found in reactants and products (i.e. sym diff is empty)
            while sym_diff:
                atom_id = sym_diff.pop()
                if atom_id not in used_reactant_atom_ids:
                    # read existing mols from atom_to_mol_dict
                    new_mol = self._atom_to_mol_dict[atom_id]
                    reactants += (new_mol,)
                    used_reactant_atom_ids.update(new_mol.atoms())
                    sym_diff = used_reactant_atom_ids.symmetric_difference(used_product_atom_ids)
                if atom_id not in used_product_atom_ids:
                    # create new mols from current_graph
                    new_mol = self._get_mdmolecule_from_atom_id(self._current_graph, atom_id, self.current_frame_number)
                    products += (new_mol,)
                    used_product_atom_ids.update(new_mol.atoms())
                    sym_diff = used_reactant_atom_ids.symmetric_difference(used_product_atom_ids)

            # update the set of handled atoms
            used_atom_ids.update(used_reactant_atom_ids)

            # set connections between molecules
            for product in products:
                for reactant in reactants:
                    product.predecessors.append(reactant)
                    reactant.successors.append(product)

            # update atom_to_mol_dict, to make it match the composition in current_graph
            for product in products:
                for atom_id in product.atoms():
                    self._atom_to_mol_dict[atom_id] = product

            new_mdmolecules += products

        return new_mdmolecules

    def _update_mdmolecule_network(self, new_mdmolecules: Iterable[MDMolecule]):
        """
        Puts molecules into the current network. Connections between molecules are read from their variables .predecessors and .successors.
        Molecule that have reached (thermal) stability according to molecule_stable_time are marked and their network nodes are duplicated,
        such that the network can later be sliced into subnetworks, which represent one reaction each.

        Example network with molecules A (inital reactant), B (instable intermediate), C (stable final product), D (some follow-up product):
        Frame  0: A
        Frame  1: A -> B
        Frame  2: A -> B -> C
        Frame 99: A -> B -> C -> D
        Using stability of A, C, and D, the network can be sliced into:
        A -> B -> C'   C -> D'   D
        Note that the nodes C and D have been duplicated, such that A->C' and C->D' can be removed from the network, being detected reactions.
        Node A is a molecule from the first trajectory frame and is not duplicated. Node D remains to be a reactant of some follow-up reaction.

        :param new_mdmolecules: List of MDMolecules to be added to the network
        """
        # add new molecules to the network
        for mol in new_mdmolecules:
            for predecessor in mol.predecessors:
                self._mdmolecule_network.add_edge((predecessor, predecessor.internal_id), (mol, mol.internal_id))

        # loop all nodes/molecules and mark them as "stable" (not a short-lived intermediate)
        # then, cut the network into subnetworks along stable molecules
        for (mol, molid) in list(self._mdmolecule_network.nodes):
            molecule_is_stable = False
            end_frame = mol.end_frame()

            if not mol.predecessors:
                # molecule from the first frame, stable by default
                molecule_is_stable = True
            elif end_frame == float('inf'):
                # molecule with no successor yet, i.e. the end frame is unknown
                if self.current_frame_number - mol.start_frame >= self._molecule_stable_frames:
                    molecule_is_stable = True
            elif (end_frame - mol.start_frame) >= self._molecule_stable_frames:
                # molecule with a lifetime long enough to be stable
                molecule_is_stable = True

            if molecule_is_stable:
                # cut network here. redirect incoming edges (precursors to this mol) to a new node to achieve a cut in the network.
                for pre_node in list(self._mdmolecule_network.predecessors((mol, molid))):
                    self._mdmolecule_network.remove_edge(pre_node, (mol, molid))
                    self._mdmolecule_network.add_edge(pre_node, (mol, -molid))

    def _get_mdreactions_from_mdmolecule_network(self) -> List[Tuple[Tuple[MDMolecule, ...], Tuple[MDMolecule, ...]]]:
        """
        Extract completed reactions from the molecule network.

        The molecule network is a directed graph where:
        - Nodes are MDMolecule
        - Edges represent molecule transformations over time
        - Negative molecule_ids indicate stable products
        - A single molecule species can participate as a reactant in some
          reactions and as a product in others (e.g., intermediates in
          sequential reactions)

        A completed reaction is identified when:
        1. A connected component has ≥2 nodes (reactants + products)
        2. Reactant nodes have no incoming edges (starting molecules)
        3. Product nodes have no outgoing edges and negative IDs
           (stable end products)

        :return: List of completed reactions as (reactants, products) tuples,
                 where reactants and products are tuples of MDMolecule objects
        """
        md_reactions = []
        nodes_to_remove = set()

        # Process each connected component (potential reaction)
        for nodeset in self._mdmolecule_network.connected_components():
            reaction = self._process_network_component(nodeset)
            if reaction:
                md_reactions.append(reaction)
                nodes_to_remove.update(nodeset)

        # Clean up processed reactions
        for node in nodes_to_remove:
            self._mdmolecule_network.remove_node(node)

        return md_reactions

    def _process_network_component(
        self, nodeset: set
    ) -> Optional[Tuple[Tuple[MDMolecule, ...], Tuple[MDMolecule, ...]]]:
        """
        Process a single connected component to extract a reaction.

        :param nodeset: Set of nodes in the component
        :return: Reaction tuple if valid, None otherwise
        """
        molnet = self._mdmolecule_network.subgraph(nodeset)

        # Skip single-node components (no reaction)
        if len(molnet) < 2:
            return None

        # Get reactants and products
        reactant_nodes = [node for node, indegree in molnet.in_degree() if indegree == 0]
        product_nodes = [node for node, outdegree in molnet.out_degree() if outdegree == 0]

        # Skip ongoing reactions (products not yet stable)
        if any(molid >= 0 for mol, molid in product_nodes):
            return None

        # Extract molecules from nodes
        reactants = tuple(mol for mol, _ in reactant_nodes)
        products = tuple(mol for mol, _ in product_nodes)

        return (reactants, products)

    #TODO: check if this method can be sped up: do after the recrossing filter
    def _extract_reaction_data_from_mdreaction(
        self,
        mdreaction: Tuple[Tuple[MDMolecule, ...], Tuple[MDMolecule, ...]]
    ) -> Tuple[List[Species], List[Species], Dict[Species, List[Geometry]],
               Dict[Species, List[Geometry]]]:
        """
        Extract chemical species and their geometries from a mdreaction.

        This method processes both reactants and products from an MDReaction to:
        1. Convert each MDMolecule to its corresponding Species
        2. Extract and store the geometries for each Species
        3. Sort the species lists for deterministic behavior

        :param mdreaction: A tuple containing two inner tuples:
                          - First tuple: Reactant MDMolecule objects
                          - Second tuple: Product MDMolecule objects
        :return: A tuple containing:
                - List of reactant Species objects
                - List of product Species objects
                - Dictionary mapping product Species to their Geometry objects
                - Dictionary mapping reactant Species to their Geometry objects

        Example:
            For a reaction H2 + O2 -> H2O2:
            - reactant_species = [Species(H2), Species(O2)]
            - product_species = [Species(H2O2)]
            - product_geometries = {Species(H2O2): [Geometry(...)]}
            - reactant_geometries = {Species(H2): [Geometry(...)],
                                    Species(O2): [Geometry(...)]}
        """
        reactants, products = mdreaction
        reactant_species = []
        product_species = []
        product_geometries = defaultdict(list)
        reactant_geometries = defaultdict(list)

        # Process reactants
        for mol in reactants:
            geometry, _ = self._get_geometry_and_graph_for_mdmolecule(mol)
            species = self._convert_molecule_to_species(mol)
            reactant_species.append(species)
            reactant_geometries[species].append(geometry)

        # Process products
        for mol in products:
            geometry, _ = self._get_geometry_and_graph_for_mdmolecule(mol)
            species = self._convert_molecule_to_species(mol)
            product_species.append(species)
            product_geometries[species].append(geometry)

        # Sort for deterministic behavior
        reactant_species.sort()
        product_species.sort()

        return (
            reactant_species,
            product_species,
            product_geometries,
            reactant_geometries
        )

    def _convert_molecule_to_species(self, mol: MDMolecule) -> Species:
        """
        Convert an MDMolecule to a chemical Species.

        :param mol: MDMolecule to convert
        :return: Corresponding Species object
        """
        geometry, graph = self._get_geometry_and_graph_for_mdmolecule(mol)
        return Species.from_geometry_and_graph(geometry, graph)

    def _process_reaction(self, reactants: Tuple[MDMolecule, ...], products: Tuple[MDMolecule, ...]) -> Optional[ReactiveEvent]:
        """
        Process a reaction to create a ReactiveEvent if valid.

        A reaction is considered valid if:
        1. No recrossing detected (products ≠ reactants)
        2. All required geometries can be extracted
        3. Bond changes can be properly identified

        Creates a ReactiveEvent containing:
        - Reaction timing and frame information
        - Geometries along reaction path
        - Bond order changes during reaction
        - Formed and broken bonds
        - Transition state geometry guess (from frame where products first appear)

        :param reactants: Tuple of reactant MDMolecule objects
        :param products: Tuple of product MDMolecule objects
        :return: ReactiveEvent if valid reaction, None if invalid or
                 recrossing detected
        """
        # Get species information
        reactant_species, product_species, product_geometries, reactant_geometries = (
            self._extract_reaction_data_from_mdreaction((reactants, products))
        )

        # Skip if recrossing detected
        if set(reactant_species) & set(product_species):
            warnings.warn("Recrossing reaction detected. Skipping.", RuntimeWarning)
            return None

        # Get reaction timing and frames
        reaction_frame = max(p.start_frame for p in products)
        reaction_time = self._frame_to_time(reaction_frame)

        # Get atoms involved in reaction
        active_atoms = sorted(atom_id for mol in products for atom_id in mol.atoms())

        # Get frame range for reaction path
        path_frames = self._get_reaction_path_frames(reaction_frame)

        # Create reaction data
        geometries = ChainOfStates(
            geometries=self._get_geometries(path_frames, active_atoms)
        )
        path_bond_orders = self._get_bond_orders(path_frames, active_atoms)
        bond_changes = self._analyze_bond_changes(reactants, products)
        reaction = Reaction(reactant_species, product_species)

        ts_geo = self._get_geometries(reaction_frame, active_atoms)
        return ReactiveEvent(
            reaction_time,
            active_atoms,
            geometries,
            reaction,
            path_bond_orders,
            bond_changes,
            reactant_geometries,
            product_geometries,
            ts_geo
        )

    def _get_reaction_path_frames(self, reaction_frame: int) -> range:
        """Get the frame range for the reaction path"""
        path_start = max(0, reaction_frame - self._reaction_path_margin)
        path_end = min(
            self.current_frame_number,
            reaction_frame + self._reaction_path_margin
        )
        return range(path_start, path_end)


    def _get_mdmolecule_from_atom_id(self, graph, atom_id, frame_number) -> chemtrayzer.core.md.MDMolecule:
        """
        small helper function that creates a MDMolecule from a networkX subgraph. The MDMolecule contains the atom with the given atom_id
        :param graph: Connectivity graph of one whole MD frame
        :type graph: networkx Graph
        :param atom_id: number of the atom in the MD frame
        :type atom_id: int
        :param frame_number: timestep number of the MD frame, to be stored in the MDMolecule
        :type frame_number: int
        :return: MDMolecule
        """
        component = graph.node_connected_component(atom_id)
        subgraph = graph.subgraph(component)
        mdmol = chemtrayzer.core.md.MDMolecule(frame_number, subgraph)
        return mdmol



class NVTRateConstants:
    """
        Computes rate constants and bounds for a set of reactions.
        See J. Chem. Theory Comput. 2017, 13, 3955−3960, https://pubs.acs.org/doi/10.1021/acs.jctc.7b00524
    :param initial_composition: dictionary of intial species and their numbers
    :param reactions_by_step: dictionary of all reactions with simulation step as key and list of reactions as value
    :param timestep: the used timestep in fs
    :param volume: the volume of the NVT simulation
    :param confidence: confidence level for the rate constant bounds (0..1)
    :param start: Offset to start the rate constant computation from. Needs to be smaller than the time of the first reaction. In fs.
    """
    def __init__(self, initial_composition: Dict[Species, int], reactions_by_time: Dict[float, List[Reaction]], timestep: float, volume: float, confidence: float = 0.9, start: float = 0.0, end: float = -1.0):
        self.ntime = None
        self.volume = volume
        self.timestep = timestep
        self.start = start
        self.end = end
        self.initial_composition = initial_composition

        # catch the case when no reactions where detected and an empty dict was passed
        if len(reactions_by_time) == 0:
            raise ValueError('No reactions to analyze. reactions_by_time is empty.')
        self.reactions_by_time = reactions_by_time
        # confidence for rate constant bounds
        self.confidence = confidence
        # container of points in time where data (reactions)
        self.time = []
        self.ntime = 0

        # factors
        # 1/(vol*NA*1E-24) : [molecules/A3] to [mol/cm3]
        self.fc = 10 / (6.022 * self.volume)
        # 1/femtosecond to 1/s
        self.ft = 1E15

        self.spex, self.reax = dict(), dict()
        # fill containers
        self.init_time_list()
        self.init_species_numbers()

    def compute(self):
        """
            Main method of reaction rate computation.
        :return:
        """
        if not self.time:
            print('No reactions to analyze.')
            return

        # species numbers over time
        self.calculate_species_concentrations()

        # reaction flux
        self.calculate_reaction_concentrations()

        # rate constants and bounds
        self.calculate_rate_coefficients()

        return

    def init_time_list(self):
        """
            Initializes the list of steps and the list of times for the computation.
        """
        list_of_times = sorted(self.reactions_by_time)

        # check user input
        if self.start >= list_of_times[0]:
            logging.warning(f'Reactions must happen after the starting time step ({self.start} fs). The start time was reset to before the first reaction ({list_of_times[0]-self.timestep}).')
            self.start = list_of_times[0]-self.timestep
        if self.end == -1:
            self.end = list_of_times[-1]
        if self.end < self.start:
            logging.warning(f'End time ({self.end} fs) must be larger than the start time. The end time was reset to the last reaction ({list_of_times[-1]} fs)')
            self.end = list_of_times[-1]

        # select reactions to include in analysis
        self.time = [self.start] + [t for t in list_of_times if self.start < t <= self.end]
        if self.end not in self.time:
            self.time = self.time + [self.end]
        self.ntime = len(self.time)

    def init_species_numbers(self):
        """
            Initializes the numbers of each species at time zero.
        """
        # initial molecules
        for species, n in self.initial_composition.items():
            self.spex[species] = [n] * self.ntime
        # later occuring molecules
        for timestep, reactions in self.reactions_by_time.items():
            for reaction in reactions:
                for species in set(reaction.reactants + reaction.products):
                    if species not in self.spex:
                        self.spex[species] = [0] * self.ntime

    def calculate_species_concentrations(self):
        """
            Reenacts the reactive events and notes down the number of species each time step.
        """
        # conversion of reaction history to species concentrations (self.spex)
        for i, t in enumerate(self.time):
            for reaction in self.reactions_by_time[t]:
                for reactant in reaction.reactants:
                    # list of flow of species per time stamp (sparse list, mostly zero)
                    if reactant not in self.spex:
                        # initialize list
                        self.spex[reactant] = [0] * self.ntime
                    # count down the reactant concentration, because they are consumed
                    self.spex[reactant][i] -= 1
                    # set concentration at future time stamps
                    for j in range(i + 1, self.ntime):
                        self.spex[reactant][j] = self.spex[reactant][i]

                # same for products
                for product in reaction.products:
                    if product not in self.spex:
                        self.spex[product] = [0] * self.ntime
                    self.spex[product][i] += 1
                    for j in range(i + 1, self.ntime):
                        self.spex[product][j] = self.spex[product][i]

    def calculate_reaction_concentrations(self):
        """
            Reenacts the reactive events.
        """
        # conversion of reaction history to reaction flux (self.reax)
        for i, t in enumerate(self.time):
            for reaction in self.reactions_by_time[t]:
                reverse_reaction = reaction.reverse()
                # make sure only forward xor backward reaction is registered
                # first come first serve
                # if this results in negative reaction flux, the flux will be inverted later on
                if reaction in self.reax:
                    self.reax[reaction].flux[i] += 1
                elif reverse_reaction in self.reax:
                    self.reax[reverse_reaction].flux[i] -= 1
                else:
                    # initialize
                    numbers = [0] * self.ntime
                    self.reax[reaction] = RateConstantRecord(flux=numbers)
                    self.reax[reaction].flux[i] += 1

        # inversion of reactions with negative net flux
        hashes_to_delete = []
        for reaction in self.reax:
            if sum(self.reax[reaction].flux) < 0:
                hashes_to_delete.append(reaction)
        for reaction in hashes_to_delete:
            reverse_reaction = reaction.reverse()
            self.reax[reverse_reaction] = self.reax.pop(reaction)
            self.reax[reverse_reaction].flux = [-1 * f for f in self.reax[reverse_reaction].flux]

    def calculate_rate_coefficients(self):
        """
            Computes for each reaction (forward and backward) the concentration integrals, rate constants, and bounds estimates.
            For more details, see J. Chem. Theory Comput. 2015, 11, 2517−2524, DOI: 10.1021/acs.jctc.5b00201 and
            J. Chem. Theory Comput. 2017, 13, 3955−3960, DOI: 10.1021/acs.jctc.7b00524

            From the definition of the rate coefficient k of a sample reaction B + C => D,

            d/dt [D] = k * [B][C]

            we can derive

            [D] - [D]_0 = k * Integral( [B][C], dt )

            where [D] - [D]_0 is the concentration increase of D through this reaction channel.
            Then, in terms of discrete reaction events, we can write

            [D] - [D]_0 = k * Sum( [B]_i * [C]_i * t_i , i=1..M)

            where M is the number of reaction events, t_i and [X]_i are the time resp. reactant concentrations between two events
            With [X] = N_x/N_0/V, where N_x is the number of X-molecules, N_0 is 6.022e23/mol, and V is the volume, we can write

            N_d/N_0/V - N_d_0/N_0/V = k * Sum( N_b_i/N_0/V * N_c_i/N_0/V * t_i , i=1..M)
                (N_d - N_d_0)/N_0/V = k * Sum( N_b_i       * N_c_i       * t_i , i=1..M) / (N_0*V)^2

            The count increase of molecule D through this reaction channel, N_D - N_D_0 = N_f, is exactly the number of forward reactions
            of the form B + C => D, (the backward reactions D => B + C are counted separately).

            So, the rate coefficient for B + C => D can be computed with

            k = N_f / Sum( N_b_i * N_c_i * t_i , i=1..M) * (N_0*V)^(r-1)

            where r is the number of reactants (here, r=2).

        """
        for reaction in self.reax:
            # compute sum of "number integrals" intA = sum(i=0..ntime)[ t(i+1)-t(i) * N_1 * N_2 * ... ]
            # where N_1, N_2, ... are numbes of reactants of a given reaction, and t(i+1)-t(i) is a time interval where those numbers are constant
            # Because V=const this can be turned into the concentration integral by multiplying with self.fc
            # A=reactants/forward B=products/backward
            A = reaction.reactants
            B = reaction.products
            nA = len(A) - 1
            nB = len(B) - 1
            intA = 0.0
            intB = 0.0
            pos = 0
            neg = 0
            for i in range(self.ntime - 1):
                dt = self.time[i + 1] - self.time[i]

                # concentration correction if two species of the same kind take part in the reaction
                corrA = {species: A.count(species) - 1 for species in A}
                corrB = {species: B.count(species) - 1 for species in B}

                # consumption of reactants
                tmpA = 1
                for species in A:
                    tmpA *= max(self.spex[species][i] - corrA[species], 0)
                    corrA[species] -= 1
                intA += tmpA * dt
                if self.reax[reaction].flux[i+1] > 0:
                    pos += self.reax[reaction].flux[i+1]

                # production of products
                tmpB = 1
                for species in B:
                    tmpB *= max(self.spex[species][i] - corrB[species], 0)
                    corrB[species] -= 1
                intB += tmpB * dt
                if self.reax[reaction].flux[i+1] < 0:
                    neg -= self.reax[reaction].flux[i+1]

            # estimate uncertainties
            # concentration integrals need be >0 else error
            if intA > 0:
                # k bounds estimation based on Poisson distribution
                # see DOI: 10.1021/acs.jctc.7b00524
                # in case of no event, an upper estimate is still possible.
                # for X=0.9 the following empiric approximations apply:
                #  lambda_lo = N - N^0.6
                #  lambda_up = N + N^0.6 + 2
                #  with kup = lambda_up/int and N = pos (or neg)
                #  tested with X=0.8 and X=0.95 as well
                if pos == 0:
                    kup = self.estNoReacBound(f=intA, X=self.confidence)
                    klo = 0.0
                else:
                    kup_0 = (2 + pos + pos ** 0.6) / intA
                    kup = leastsq(func=self.estRateBounds, x0=kup_0, args=(intA, pos, self.confidence))[0][0]
                    klo = float(np.real(-pos / intA * self.lmbW(lambda_up=kup * intA, N=pos)))
                self.reax[reaction].events = pos
                self.reax[reaction].upper_k = kup * self.ft / (self.fc ** nA)
                self.reax[reaction].lower_k = klo * self.ft / (self.fc ** nA)
                self.reax[reaction].rate = pos / intA * self.ft / (self.fc ** nA)
            if intB > 0:
                if neg == 0:
                    kup = self.estNoReacBound(f=intB, X=self.confidence)
                    klo = 0.0
                else:
                    kup_0 = (2 + neg + neg ** 0.6) / intB
                    kup = leastsq(func=self.estRateBounds, x0=kup_0, args=(intB, neg, self.confidence))[0][0]
                    klo = float(np.real(-neg / intB * self.lmbW(lambda_up=kup * intB, N=neg)))
                self.reax[reaction].eventsB = neg
                self.reax[reaction].upper_kB = kup * self.ft / (self.fc ** nB)
                self.reax[reaction].lower_kB = klo * self.ft / (self.fc ** nB)
                self.reax[reaction].rateB = neg / intB * self.ft / (self.fc ** nB)

    # TODO: add tests if this method is needed, else remove
    def get_rates(self, reaction: Reaction):
        """
            Returns rate constants of one specified reaction, or None if the reaction has no data. Units are cm3, mol and s.
        :param reaction: Reaction object of a reaction.
        :return: tuple of rate constant, lower bound, upper bound, number of events
        :rtype: Tuple[float, float, float, int]
        """
        forward_is_in_here = True
        ayreaction = None
        try:
            ayreaction = self.reax[reaction]
        except KeyError:
            reverse_reaction = reaction.reverse()
            forward_is_in_here = False
            try:
                ayreaction = self.reax[reverse_reaction]
            except KeyError:
                rstr = ' -> '.join(' + '.join([species.smiles for species in species]) for species in [reaction.reactants, reaction.products])
                warnings.warn(f'Reaction "{rstr}" not found in Rate Calculator')
        if ayreaction is None:
            return 0.0, 0.0, 0.0, 0
        else:
            if forward_is_in_here:
                k, k_low, k_up, n = ayreaction.rate, ayreaction.lower_k, ayreaction.upper_k, ayreaction.events
            else:
                k, k_low, k_up, n = ayreaction.rateB, ayreaction.lower_kB, ayreaction.upper_kB, ayreaction.eventsB
            return k, k_low, k_up, n

    # TODO: add tests if this method is needed, else remove
    def write_data(self, species_filename, rates_filename):
        """
            Write species numbers and reaction rate constants into two csv files.
        :param species_filename:
        :param rates_filename:
        """
        # . write species concentrations
        # writer = open(species_filename, 'w')
        with open(species_filename, 'w') as f:
            smiles_str = ','.join(species.smiles for species in self.spex)
            f.write(f't [fs],{smiles_str}\n')
            for i, t in enumerate(self.time):
                numbers_str = ','.join(str(self.spex[species][i]) for species in self.spex)
                f.write(f'{t},{numbers_str}\n')
            f.close()

        # write rate constats for each reaction forward and backward
        with open(rates_filename, 'w') as f:
            f.write('reaction_id,reactant_SMILES,product_SMILES,k,k_lower,k_upper,#events\n')
            for reaction, ayr in self.reax.items():
                smiles_reactants = '.'.join(species.smiles for species in reaction.reactants)
                smiles_products = '.'.join(species.smiles for species in reaction.products)
                reverse = reaction.reverse()
                f.write(f'{reaction.id},{smiles_reactants},{smiles_products},{ayr.rate:},{ayr.lower_k},{ayr.upper_k},{ayr.events}\n')
                f.write(f'{reverse.id},{smiles_products},{smiles_reactants},{ayr.rateB},{ayr.lower_kB},{ayr.upper_kB},{ayr.eventsB}\n')

        return

    def compact_result(self):
        """
            Return the rate data in a compact form as {reaction.id: (k, klo, kup, N)}
        :rtype: Dict[str, Tuple[float, float, float, int]]
        """
        compact_result = {}
        for reaction, ayr in self.reax.items():
            reverse = reaction.reverse()
            compact_result[reaction] = (ayr.rate, ayr.lower_k, ayr.upper_k, ayr.events)
            compact_result[reverse] = (ayr.rateB, ayr.lower_kB, ayr.upper_kB, ayr.eventsB)
        return compact_result

    def lmbW(self, lambda_up, N):
        """
            Adapted Lambert W function for usage in the bounds computation for rate constants.
            See J. Chem. Theory Comput. 2017, 13, 3955−3960, https://pubs.acs.org/doi/10.1021/acs.jctc.7b00524
            Used in equation (13)
        :param lambda_up: upper limit of expected number of events
        :param N: actual number of events
        :return: lambda_low, the lower limit of expected number of events
        """
        return lambertw(np.round(-lambda_up * np.exp(-lambda_up / N) / N, 30), k=0)


    def estRateBounds(self, k_up, f, N, X):
        """
            Helper function of the iterative computation of k_up, the upper rate constant of a given reaction.
            The function computes the difference between the explicitly specified confidence level X
            and the implicitly defined X via N and lambda (to be minimized by scipy.optimize.leastsq).
            See J. Chem. Theory Comput. 2017, 13, 3955−3960, https://pubs.acs.org/doi/10.1021/acs.jctc.7b00524
            Divide Equation (11) by Gamma(N+1) to get X = - gammaincc(N+1,lambda_up) + gammaincc(N+1,lambda_low)
        :param k_up: upper rate constant guess for given actual number of events
        :param f: reactants concentration integral (sum over product of volume, concentrations of reactants, and time interval)
        :param N: actual number of events
        :param X: specified confidence level (0..1)
        :return: difference of explicitly and implicitly defined X
        """
        return X + gammaincc(N + 1, k_up * f) - gammaincc(N + 1, np.real(-N * self.lmbW(lambda_up=k_up * f, N=N)))


    def estNoReacBound(self, f, X):
        """
            Computes the upper bound of a rate constant for a reaction that was not observed.
            See J. Chem. Theory Comput. 2017, 13, 3955−3960, https://pubs.acs.org/doi/10.1021/acs.jctc.7b00524
            Derived from Equation (8) where lambda_low = 0
        :param f: reactants concentration integral (sum over product of volume, concentrations of reactants, and time interval)
        :param X: specified confidence level (0..1)
        :return: upper bound for rate constant
        """
        return -np.log(1 - X) / f
