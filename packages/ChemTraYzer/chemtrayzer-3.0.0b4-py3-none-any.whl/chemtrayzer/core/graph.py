"""Graph theory

This module contains classes for representing graphs and performing graph
theory operations on them. It is meant as general, application-agnostic code
and should not contain graph classes designed for a single purpose only.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import functools
import itertools
import warnings
from abc import abstractmethod
from collections import Counter, deque
from collections.abc import Iterable, Iterator, Sequence
from copy import deepcopy
from enum import Enum
from numbers import Number
from operator import eq, itemgetter
from typing import (Any, ClassVar, Optional, TypeAlias,
                    Protocol, Literal, runtime_checkable)

import networkx as nx  # type: ignore
import numpy as np
import rdkit  # type: ignore
import rdkit.Chem  # type: ignore
import scipy.sparse  # type: ignore
from rdkit import Chem
from typing_extensions import Self  # Self is included in typing from 3.11

from chemtrayzer.core._bond_order import connectivity2bond_orders
from chemtrayzer.core.coords import ChainOfStates, Geometry
from chemtrayzer.core.periodic_table import PERIODIC_TABLE as PTOE
from chemtrayzer.core.periodic_table import Element
from chemtrayzer.reaction_sampling.atomutils import (
    ISwitchingFunction,
    StepSwitchingFunction,
)

bond_type_dict = {
    0.5: Chem.BondType.HYDROGEN,  # to be drawn as a dotted line
                                 #(looks better than other options)
    0: Chem.BondType.UNSPECIFIED,
    1: Chem.BondType.SINGLE,
    2: Chem.BondType.DOUBLE,
    3: Chem.BondType.TRIPLE,
    4: Chem.BondType.QUADRUPLE,
    5: Chem.BondType.QUINTUPLE,
    6: Chem.BondType.HEXTUPLE,
    1.5: Chem.BondType.ONEANDAHALF,
    2.5: Chem.BondType.TWOANDAHALF,
    3.5: Chem.BondType.THREEANDAHALF,
    4.5: Chem.BondType.FOURANDAHALF,
    5.5: Chem.BondType.FIVEANDAHALF,
    "AROMATIC": Chem.BondType.AROMATIC,
    "IONIC": Chem.BondType.IONIC,
    "HYDROGEN": Chem.BondType.HYDROGEN,
    "THREECENTER": Chem.BondType.THREECENTER,
    "DATIVEONE": Chem.BondType.DATIVEONE,
    "DATIVE": Chem.BondType.DATIVE,
    "DATIVEL": Chem.BondType.DATIVEL,
    "DATIVER": Chem.BondType.DATIVER,
    "OTHER": Chem.BondType.OTHER,
    "ZERO": Chem.BondType.ZERO,
}

def cyclic_perm(a: list) -> list[list]:
    def reorder_from_idx(idx: int, a: list) -> list:
        return a[idx:] + a[:idx]

    return [functools.partial(reorder_from_idx, i)(a) for i in range(len(a))]


class _Graph:
    """
    Graph class which currently uses networkx graphs in the background.
    Consists of nodes and edges. Can have attributes on nodes and edges.
    Graphs are considered equal if they have identical nodes and edges with the
    identical attributes.

    Please use the DirectedGraph or UndirectedGraph classes instead of this
    class.

    """

    _nx_graph: nx.Graph

    def __init__(self) -> None:
        self._nx_graph = nx.Graph()

    @classmethod
    def _from_nx_graph(cls, nx_graph: nx.Graph) -> Self:
        newgraph = cls()
        newgraph._nx_graph = nx_graph.copy()
        return newgraph

    @classmethod
    def from_numpy_array(
        cls, np_array: np.array, edge_attr: Optional[str] = None
    ) -> Self:
        newgraph = cls()
        nx_graph = nx.from_numpy_array(
            np_array,
            create_using=newgraph._nx_graph.__class__,
            edge_attr=edge_attr,
        )
        newgraph._nx_graph = nx_graph
        return newgraph

    @classmethod
    def from_numpy_sparse_array(
        cls, sp_arr: scipy.sparse.sparray, edge_attr: Optional[str] = None
    ) -> Self:
        newgraph = cls()
        nx_graph = nx.from_scipy_sparse_array(
            sp_arr,
            create_using=newgraph._nx_graph.__class__,
            edge_attr=edge_attr,
        )
        newgraph._nx_graph = nx_graph
        return newgraph

    @classmethod
    def from_composed_graphs(cls, graphs: Iterable[Self]) -> Self:
        """
        Unifies many graphs to one. Duplicate nodes or edges or attributes are
        overwritten in order of iteration.
        :param graphs: iterable container of Graphs
        :return: one Graph with all nodes, edges and attributes of the input
                 Graphs
        """
        new_nxgraph = nx.compose_all([g._nx_graph for g in graphs])
        return cls._from_nx_graph(new_nxgraph)

    def __len__(self) -> int:
        """
        Returns the number of nodes in the graph.
        :return: Number of nodes in the graph
        :rtype: int
        """
        return len(self._nx_graph)

    def neighbors(self, node: Any) -> tuple[Any, ...]:
        """
        Return all neighboring nodes.
        :param node: Name of the node.
        :return: All neighboring nodes.
        """
        return tuple(sorted([*self._nx_graph.neighbors(node)]))

    def add_node(self, node: Any, **attr) -> None:
        self._nx_graph.add_node(node, **attr)

    def has_node(self, node: Any) -> bool:
        return self._nx_graph.has_node(node)

    def remove_node(self, node: Any) -> None:
        self._nx_graph.remove_node(node)

    def get_node_attributes(self, node: Any) -> dict[str, Any]:
        return self._nx_graph.nodes[node]

    def get_node_attribute(
        self, node: Any, attr: str, default: Optional[Any] = None
    ) -> Any:
        return self._nx_graph.nodes[node].get(attr, default)

    def set_node_attribute(self, node: Any, attr: str, value: Any) -> None:
        self._nx_graph.nodes[node][attr] = value

    def set_node_attributes(self, values: dict[Any, Any], name: str) -> None:
        """sets node attributes from a given value or dictionary of values

        :param values: dictionary of values to be set and node names as keys
        :type values: dict[Any, Any]
        :param name: Name of the attribute to be set
        :type name: str
        """
        nx.set_node_attributes(self._nx_graph, name=name, values=values)

    def delete_node_attribute(self, node: Any, attr: str) -> None:
        del self._nx_graph.nodes[node][attr]

    def has_edge(self, node1: Any, node2: Any) -> bool:
        """
        Test on edge existence.
        :param node1: Name of first node
        :param node2: Name of second node
        :return: True if edge exists, false otherwise.
        """
        return self._nx_graph.has_edge(node1, node2)

    def add_edge(self, node1: Any, node2: Any, **attr) -> None:
        """
        Add an edge.
        :param node1: Name of first node
        :param node2: Name of second node
        :param attr: Optional extra attributes to be set.
        """
        self._nx_graph.add_edge(node1, node2, **attr)

    def remove_edge(self, node1: Any, node2: Any) -> None:
        """
        Remove an edge.
        :param node1: Name of first node
        :param node2: Name of second node
        """
        self._nx_graph.remove_edge(node1, node2)

    def get_edge_attributes(self, node1: Any, node2: Any) -> dict[str, Any]:
        """
        Get all edge attributes.
        :param node1: Name of first node
        :param node2: Name of second node
        :return: All edge attributes.
        """
        return dict(self._nx_graph.edges[node1, node2])

    def get_edge_attribute(
        self, node1: Any, node2: Any, attr: str, default: Optional[Any] = None
    ) -> Any:
        """
        Get an edge attribute.
        :param node1: Name of first node
        :param node2: Name of second node
        :param attr: Name of attribute to retrieve
        :return: The value of the attribute.
        """
        return self._nx_graph.get_edge_data(node1, node2, default={}).get(
            attr, default
        )

    def set_edge_attribute(
        self, node1: Any, node2: Any, attr: str, value: Any
    ) -> None:
        """
        set an edge attribute.
        :param node1: Name of first node
        :param node2: Name of second node
        :param attr: Name of attribute to be set
        :param value: Value to be set
        """
        self._nx_graph[node1][node2][attr] = value

    def delete_edge_attribute(self, node1: Any, node2: Any, attr: str) -> None:
        """
        Delete an edge attribute. Raises an exception if the attribute doesn't
        exist.
        :param node1: Name of first node
        :param node2: Name of second node
        :param attr: Name of attribute to be deleted
        """
        del self._nx_graph[node1][node2][attr]

    def __eq__(self, other: Any) -> bool:
        if self.__class__ != other.__class__:
            return False
        else:
            return (
                self.get_nodes_with_attributes()
                == other.get_nodes_with_attributes()
                and self.get_edges_with_attributes()
                == other.get_edges_with_attributes()
            )

    @property
    def nodes(self) -> tuple[Any, ...]:
        return tuple(sorted(self._nx_graph.nodes(data=False)))

    def get_nodes_with_attributes(self) -> dict[Any, dict[str, Any]]:
        """
        Returns a list of nodes or a dictionary of nodes with a node data
        dictionary as values.
        :param data: toggle extra node data
        """
        return dict(self._nx_graph.nodes(data=True))

    @property
    def edges(self) -> tuple[tuple[Any, Any], ...]:
        """
        Returns a list of edges or a dictionary of nodes with an edge data
        dictionary as values.
        :param data: toggle extra edge data
        """
        return tuple(self._nx_graph.edges)

    def get_edges_with_attributes(
        self,
    ) -> dict[tuple[Any, Any], dict[str, Any]]:
        return {
            (atom1, atom2): attr_dict
            for atom1, atom2, attr_dict in self._nx_graph.edges(data=True)
        }

    def connectivity_matrix(self) -> np.ndarray:
        """
        Returns a connectivity matrix of the graph. Order is the same as in
        self.nodes()
        1 if nodes are connected, 0 if not.
        :return: Connectivity matrix
        :rtype: np.ndarray
        """
        return nx.to_numpy_array(
            self._nx_graph, nodelist=self.nodes, dtype=int
        )

    def relabel_nodes(
        self, mapping: dict[Any, Any], copy: bool = False
    ) -> Self:
        """
        Renames the nodes according to the mapping. Nodes are renamed in place,
        unless the attribute copy is set to True.
        :param mapping: dictionary in {old: new, ...} format
        :param copy: if True, a copy of this object is returned
        :return: a graph with relabeled nodes
        """
        new_graph = nx.relabel_nodes(
            self._nx_graph, mapping=mapping, copy=copy
        )
        if copy:
            return self._from_nx_graph(new_graph)
        return self

    def subgraph(self, nodes: Iterable[Any]) -> Self:
        """Returns a true copy of the subgraph consisting of the chosen nodes

        :param nodes: Iterable of nodes from graph to include in subgraph
        :type nodes: Iterable
        :return: Subgraph including given nodes
        :rtype: Self
        """
        return self._from_nx_graph(nx.subgraph(self._nx_graph, nodes).copy())

    def copy(self) -> Self:
        """
        Returns a copy of Graph.
        :return: a copy of this Graph
        """
        return self._from_nx_graph(self._nx_graph.copy())

    def get_subgraph_isomorphic_mappings(
        self,
        other: Self,
    ) -> Iterator[dict[Any, Any]]:
        """Subgraph isomorphic mappings from "other" onto "self".

        Generates all node-iduced subgraph isomorphic mappings.
        All nodes of "other" have to be present in "self".
        The edges of "other" have to be the subset of the edges of "self"
        relating to the nodes of "other".

        :param other: Graph to be mapped onto self
        :type other: Self
        :return: Mappings from the nodes of self onto the nodes of other
        :rtype: Iterator[dict[Any, Any]]
        """
        return self._get_subgraph_isomorphic_mappings(
            other=other, _node_match=eq, _edge_match=eq
        )

    def _get_subgraph_isomorphic_mappings(
        self, other: Self, _node_match=eq, _edge_match=eq
    ) -> Iterator[dict[Any, Any]]:
        return nx.isomorphism.GraphMatcher(
            self._nx_graph,
            other._nx_graph,
            node_match=_node_match,
            edge_match=_edge_match,
        ).subgraph_isomorphisms_iter()

    def _get_subgraph_monomorphic_mappings(
        self, other: Self, _node_match=eq, _edge_match=eq
    ) -> Iterator[dict[Any, Any]]:
        return nx.isomorphism.GraphMatcher(
            self._nx_graph,
            other._nx_graph,
            node_match=_node_match,
            edge_match=_edge_match,
        ).subgraph_monomorphisms_iter()

    def get_subgraph_monomorphic_mappings(
        self,
        other: Self,
    ) -> Iterator[dict[Any, Any]]:
        """Subgraph monomorphic mappings from "other" onto "self".

        Generates all subgraph monomorphic mappings.
        All nodes of other have to be present in "self".
        The edges of "other" have to be a subset of the edges of "self".

        :param other: Graph to be mapped onto self
        :type other: Self
        :return: Mappings from the nodes of self onto the nodes of other
        :rtype: Iterator[dict[Any, Any]]
        """
        return self._get_subgraph_monomorphic_mappings(
            other=other, _node_match=eq, _edge_match=eq
        )

    def _get_isomorphic_mappings(
        self, other: Self, _node_match=eq, _edge_match=eq
    ) -> Iterator[dict[Any, Any]]:
        return nx.isomorphism.GraphMatcher(
            self._nx_graph,
            other._nx_graph,
            node_match=_node_match,
            edge_match=_edge_match,
        ).isomorphisms_iter()

    def get_isomorphic_mappings(self, other: Self) -> Iterator[dict[Any, Any]]:
        """Isomorphic mappings between "self" and  "other".

        Generates all isomorphic mappings between "other" and "self".
        All nodes and edges have to be present  in both graphs.

        :param other: Other Graph to be mapped onto self
        :type other: Self
        :return: Mappings from the nodes of self onto the nodes of other
        :rtype: Generator[dict[Any, Any]]
        """
        return self._get_isomorphic_mappings(
            other=other, _node_match=eq, _edge_match=eq
        )

    def is_isomorphic(self, other: Self) -> bool:
        """Check if the graphs are isomorphic

        :param other: Self to compare against.
        :type other: Self
        :return: True/False if isomorphic
        :rtype: bool
        """
        return any(self.get_isomorphic_mappings(other))

    def _get_automorphic_mappings(
        self, _node_match=eq, _edge_match=eq
    ) -> Iterator[dict[Any, Any]]:
        return self._get_isomorphic_mappings(
            other=self, _node_match=_node_match, _edge_match=_edge_match
        )

    def get_automorphic_mappings(self) -> Iterator[dict[Any, Any]]:
        """Automorphic mappings of the graph onto itself.

        Generates all isomorphic mappings of the graph onto itself.
        :return: Automorphic Mappings
        :rtype: Iterator[dict[Any, Any]]
        """
        return self._get_automorphic_mappings(_node_match=eq, _edge_match=eq)


class UndirectedGraph(_Graph):
    """
    Graph class which currently uses networkx graphs in the background.
    Consists of nodes and edges. Can have attributes on nodes and edges.
    Only one edge between two nodes is allowed. Edges do not have a direction.
    Graphs are considered equal if they have identical nodes and edges with the
    identical attributes.
    """

    @property
    def connected_components(self) -> tuple[set[int], ...]:
        """A generator of sets of nodes, one for each component of the graph

        :return: sets of connected nodes
        :rtype: Generator[set]
        """
        return tuple(nx.connected_components(self._nx_graph))


class DirectedGraph(_Graph):
    """
    Graph class which currently uses networkx graphs in the background.
    Consists of nodes and edges. Can have attributes on nodes and edges.
    Edges have a direction. Only one edge between two nodes is allowed per
    direction.
    Graphs are considered equal if they have identical nodes and edges with the
    identical attributes.
    """

    _nx_graph: nx.DiGraph

    def __init__(self) -> None:
        self._nx_graph = nx.DiGraph()

    @classmethod
    def _from_nx_graph(cls, nx_graph: nx.DiGraph) -> Self:
        newgraph = cls()
        newgraph._nx_graph = nx_graph.copy()
        return newgraph

    def in_degree(self) -> Iterable[tuple[int, int]]:
        """
        Holds tuples of nodes and their node in-degree, which is the sum of
        (the weights of) all entering edges.
        :return: an iterator of two-tuples of (node, in-degree)
        :rtype: Iterable[tuple[int, int]]
        """
        return self._nx_graph.in_degree

    def out_degree(self) -> Iterable[tuple[int, int]]:
        """
        Holds tuples of nodes and their node out-degree, which is the sum of
        (the weights of) all leaving edges.
        :return: an iterator of two-tuples of (node, out-degree)
        :rtype: Iterable[tuple[int, int]]
        """
        return self._nx_graph.out_degree

    def connected_components(self) -> Iterable[set]:
        """
        Finds and returns all sets of nodes which are connected,
        while disregarding any edge direction.
        :return: iterable sets of nodes
        :rtype: Iterable[set]
        """
        return nx.weakly_connected_components(self._nx_graph)

    def get_subgraph_isomorphic_mappings(
        self,
        other: Self,
    ) -> Iterator[dict[Any, Any]]:
        """Subgraph isomorphic mappings from "self" onto "other".

        Generates all node-iduced subgraph isomorphic mappings.
        All nodes of "other" have to be present in "self".
        The edges of "other" have to be the subset of the edges of "self"
        relating to the nodes of "other".

        :param other: Graph to be mapped onto self
        :type other: Self
        :return: Mappings from the nodes of self onto the nodes of other
        :rtype: Iterator[dict[Any, Any]]
        """
        return self._get_subgraph_isomorphic_mappings(
            other=other, _node_match=eq, _edge_match=eq
        )

    def _get_subgraph_isomorphic_mappings(
        self, other: Self, _node_match=eq, _edge_match=eq
    ) -> Iterator[dict[Any, Any]]:
        return nx.isomorphism.DiGraphMatcher(
            self._nx_graph,
            other._nx_graph,
            node_match=_node_match,
            edge_match=_edge_match,
        ).subgraph_isomorphisms_iter()

    def get_subgraph_monomorphic_mappings(
        self, other: Self
    ) -> Iterator[dict[Any, Any]]:
        """Subgraph monomorphic mappings from "self" onto "other".

        Generates all subgraph monomorphic mappings.
        All nodes of other have to be present in "self".
        The edges of "other" have to be a subset of the edges of "self".

        :param other: Graph to be mapped onto self
        :type other: Self
        :return: Mappings from the nodes of self onto the nodes of other
        :rtype: Iterator[dict[Any, Any]]
        """
        return self._get_subgraph_monomorphic_mappings(
            other=other, _node_match=eq, _edge_match=eq
        )

    def _get_subgraph_monomorphic_mappings(
        self, other: Self, _node_match=eq, _edge_match=eq
    ) -> Iterator[dict[Any, Any]]:
        return nx.isomorphism.DiGraphMatcher(
            self._nx_graph,
            other._nx_graph,
            node_match=_node_match,
            edge_match=_edge_match,
        ).subgraph_monomorphisms_iter()

    def get_isomorphic_mappings(
        self, other: _Graph
    ) -> Iterator[dict[Any, Any]]:
        """
        Returns all possible mappings of the graph and the other graph
        onto eachother.
        :param other: Other Graph to compare with
        :type other: Graph
        :return: All possible mappings of the graph and the other graph
                 onto eachother
        :rtype: Generator[dict[self_node:other_node]]
        """
        return self._get_isomorphic_mappings(
            other=other, _node_match=eq, _edge_match=eq
        )

    def _get_isomorphic_mappings(
        self, other: _Graph, _node_match=eq, _edge_match=eq
    ) -> Iterator[dict[Any, Any]]:
        return nx.isomorphism.DiGraphMatcher(
            self._nx_graph,
            other._nx_graph,
            node_match=_node_match,
            edge_match=_edge_match,
        ).isomorphisms_iter()


class MolGraph:
    """
    Graph representing a molecular entity. Nodes represent atoms and edges
    represent bonds. All nodes have an `atom_type` attribute of type `Element`.
    The node ids should be integers. The graph is considered equal to another
    graph, iff. they are isomorphic and of the same type.
    """

    _graph: UndirectedGraph

    def __init__(self, mol_graph: Optional[MolGraph] = None):
        if (
            mol_graph is not None
            and getattr(mol_graph, "_graph", None) is not None
        ):
            self._graph = deepcopy(mol_graph._graph)
        else:
            self._graph = UndirectedGraph()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        else:
            return self.is_isomorphic(other)

    @property
    def atoms(
        self,
    ) -> tuple[int, ...]:
        """
        :return: Returns all atoms of the molecule
        :rtype: tuple[int]
        """
        atoms = self._graph.nodes
        return atoms

    @property
    def atom_types(
        self,
    ) -> tuple[Element, ...]:
        """
        :return: Returns a list of all atom types in the MolGraph
        :rtype: list
        """
        return tuple(
            self.get_atom_attribute(atom, "atom_type") for atom in self.atoms
        )

    @property
    def n_atoms(
        self,
    ) -> int:
        """
        :return: Returns number of atoms in the MolGraph
        :rtype: int
        """
        return len(self._graph.nodes)

    def __len__(self) -> int:
        return self.n_atoms

    def has_atom(self, atom: int) -> bool:
        """Returns True if the molecules contains an atom with this id.

        :param atom: Atom
        :type atom: int
        :return: value
        :rtype: bool
        """
        return self._graph.has_node(atom)

    def add_atom(
        self, atom: int, atom_type: int | str | Element, **attr
    ) -> None:
        """Adds atom to the MolGraph

        :param atom: Atom ID
        :type atom: int
        :param atom_type: Atom Type
        :type atom_type: Element
        """
        atom_type = PTOE[atom_type]

        # parse numpy.int64, etc. to int
        self._graph.add_node(int(atom), atom_type=atom_type, **attr)

    def remove_atom(self, atom: int) -> None:
        """Removes atom from graph.

        :param atom: Atom ID
        :type atom: int
        """
        self._graph.remove_node(atom)

    def get_atom_attribute(
        self, atom: int, attr: str, default: Optional[Any] = None
    ) -> Any:
        """
        :param atom: Atom
        :type atom: int
        :param attr: Attribute
        :type attr: str
        :return: Returns the value of the attribute of the atom
        :rtype: Any
        """
        return self._graph.get_node_attribute(atom, attr=attr, default=default)

    def set_atom_attribute(self, atom: int, attr: str, value: Any) -> None:
        """
        sets the Value of the Attribute on Atom.
        :param atom: Atom
        :type atom: int
        :param attr: Attribute
        :type attr: str
        :param value: Value
        :type value: Any
        :raises ValueError: The attribute "atom_type" can only have values of
                            type Element
        """
        if attr == "atom_type":
            try:
                value = PTOE[value]
            except KeyError:
                raise ValueError(
                    f"'{value}' can not be used as atom_type for "
                    f"{self.__class__.__name__}"
                )
        self._graph.set_node_attribute(atom, attr=attr, value=value)

    def delete_atom_attribute(self, atom: int, attr: str) -> None:
        """
        Deletes the Attribute of the Atom
        :param atom: Atom ID
        :type atom: int
        :param attr: Attribute
        :type attr: str
        :raises ValueError: The attribute "atom_type" can not be deleted
        """
        if attr == "atom_type":
            raise ValueError("atom_type can not be deleted")
        else:
            self._graph.delete_node_attribute(atom, attr=attr)

    def get_atom_attributes(
        self, atom: int, attributes: Optional[Iterable[str]] = None
    ) -> dict[str, Any]:
        """
        :param atom: Atom
        :type atom: int
        :param attributes: Specific attributes to return
        :type attributes: Optional[Iterable[str]]
        :return: Returns all or just the chosen attributes of the atom
        :rtype: dict[str, Any]
        """
        if attributes is None:
            return self._graph.get_node_attributes(atom)
        else:
            return {
                attr: self.get_atom_attribute(atom, attr)
                for attr in attributes
            }

    def get_atoms_with_attributes(self) -> dict[int, dict[str, Any]]:
        """
        :return: Returns all atoms in the MolGraph with their attributes
        :rtype: dict[int:dict[str:Any]]
        """
        return self._graph.get_nodes_with_attributes()

    @property
    def bonds(
        self,
    ) -> tuple[tuple[int, int], ...]:
        """
        :return: Returns all bonds in the MolGraph
        :rtype: tuple[tuple[int, int], ...]
        """
        bonds = self._graph.edges
        return bonds

    def has_bond(self, atom1: int, atom2: int) -> bool:
        """Returns True if bond is in MolGraph.

        :param atom1: Atom1
        :type atom1: int
        :param atom2: Atom2
        :type atom2: int
        :return: If the bond is in MolGraph
        :rtype: bool
        """
        return self._graph.has_edge(atom1, atom2)

    def add_bond(self, atom1: int, atom2: int, **attr) -> None:
        """Adds bond between Atom1 and Atom2.

        :param atom1: Atom1
        :type atom1: int
        :param atom2: Atom2
        :type atom2: int
        """
        # parse numpy.int64, etc. to int
        if atom1 not in self.atoms or atom2 not in self.atoms:
            raise ValueError("Atoms not in MolGraph")
        self._graph.add_edge(int(atom1), int(atom2), **attr)

    def remove_bond(self, atom1: int, atom2: int) -> None:
        """
        Removes bond between Atom1 and Atom2.
        :param atom1: Atom1
        :type atom1: int
        :param atom2: Atom2
        :type atom2: int
        """
        self._graph.remove_edge(atom1, atom2)

    def get_bond_attribute(
        self, atom1: int, atom2: int, attr: str, default: Optional[Any] = None
    ) -> Any:
        """
        :param atom1: Atom1
        :type atom1: int
        :param atom2: Atom2
        :type atom2: int
        :param attr: Attribute
        :type attr: str
        :return: Returns the value of the attribute of the bond
                 between Atom1 and Atom2
        :rtype: Any
        """
        return self._graph.get_edge_attribute(
            atom1, atom2, attr=attr, default=default
        )

    def set_bond_attribute(
        self, atom1: int, atom2: int, attr: str, value: Any
    ) -> None:
        """
        sets the Attribute of the bond between Atom1 and Atom2.
        The Attribute "bond_order" can only have numerical values
        :param atom1: Atom1
        :type atom1: int
        :param atom2: Atom2
        :type atom2: int
        :param attr: Attribute
        :type attr: str
        :param value: Value
        :type value: Any
        :raises ValueError: The attribute "bond_order" has to be a number
        """
        if attr == "bond_order" and not isinstance(value, Number):
            raise ValueError("bond_order has to be a number")
        else:
            self._graph.set_edge_attribute(
                atom1, atom2, attr=attr, value=value
            )

    def delete_bond_attribute(self, atom1: int, atom2: int, attr: str) -> None:
        """
        Deletes the Attribute of the bond between Atom1 and Atom2
        :param atom1:
        :type atom1: int
        :param atom2: Atom1
        :type atom2: int
        :param attr: Attribute
        :type attr: str
        """
        self._graph.delete_edge_attribute(atom1, atom2, attr=attr)

    def get_bond_attributes(
        self,
        atom1: int,
        atom2: int,
        attributes: Optional[Iterable[str]] = None,
    ) -> dict[str, Any]:
        """
        :param atom1: Atom1
        :type atom1: int
        :param atom2: Atom2
        :type atom2: int
        :param attributes: Specific attributes to return
        :type attributes: Optional[Iterable[str]]
        :return: Returns chosen attributes of the bond between Atom1 and Atom2
        :rtype: dict[str, Any]
        """
        if attributes is None:
            return self._graph.get_edge_attributes(atom1, atom2)
        else:
            return {
                attr: self._graph.get_edge_attribute(atom1, atom2, attr)
                for attr in attributes
            }

    def get_bonds_with_attributes(
        self,
    ) -> dict[tuple[int, int], dict[str, Any]]:
        """
        :return: Returns all bonds in the MolGraph
        :rtype: dict[tuple[int,int]:dict[str:Any]]
        """
        return self._graph.get_edges_with_attributes()

    def bonded_to(self, atom: int) -> tuple[int, ...]:
        """
        Returns the atoms connected to the atom.
        :param atom: Id of the atom.
        :type atom: int
        :return: tuple of atoms connected to the atom.
        :rtype: tuple[int]
        """
        return self._graph.neighbors(atom)

    def connectivity_matrix(self) -> np.ndarray:
        """
        Returns a connectivity matrix of the graph. Order is the same as
        in self.nodes()
        1 if nodes are connected, 0 if not.
        :return: Connectivity matrix
        :rtype: np.ndarray
        """
        return self._graph.connectivity_matrix()

    def _to_mol(
        self, generate_bond_orders=True, charge=0
    ) -> tuple[rdkit.Chem.rdchem.RWMol, dict[int, int]]:
        mol = rdkit.Chem.RWMol()

        atom_types_strings = []
        idx_map_num_dict = {}

        for atom in self.atoms:
            atom_type = self.get_atom_attribute(atom, "atom_type")
            if atom_type is None:
                raise RuntimeError(atom, self.atoms, self.atom_types)
            rd_atom = rdkit.Chem.Atom(atom_type.symbol)
            rd_atom.SetNoImplicit(True)
            atom_index = mol.AddAtom(rd_atom)
            idx_map_num_dict[atom_index] = atom
            atom_types_strings.append(atom_type.atomic_nr)
            mol.GetAtomWithIdx(atom_index).SetAtomMapNum(atom, strict=True)

        for i in range(self.n_atoms):
            for j in range(i + 1, self.n_atoms):
                if self.has_bond(idx_map_num_dict[i], idx_map_num_dict[j]):
                    mol.AddBond(i, j)
                    mol.GetBondBetweenAtoms(i, j).SetBondType(
                        rdkit.Chem.rdchem.BondType.SINGLE
                    )

        if generate_bond_orders is True:
            bond_order_mat = connectivity2bond_orders(
                atom_types=self.atom_types,
                connectivity_matrix=self.connectivity_matrix(),
                charge=0,
            )

            index_map_num_dict = {
                i: map_num for i, map_num in enumerate(self.atoms)
            }

            map_num_idx_dict = {
                map_num: idx for idx, map_num in idx_map_num_dict.items()
            }

            for bond in self.bonds:
                atom1, atom2 = bond
                bond_order = bond_order_mat[
                    index_map_num_dict[atom1], index_map_num_dict[atom2]
                ]

                mol.GetBondBetweenAtoms(
                    map_num_idx_dict[atom1], map_num_idx_dict[atom2]
                ).SetBondType(bond_type_dict[bond_order])

        return mol, idx_map_num_dict

    def to_mol(
        self, generate_bond_orders=True, charge=0
    ) -> rdkit.Chem.rdchem.Mol:
        """
        Creates a RDKit mol object using the connectivity of the mol graph
        without bond orders.


        :return: RDKit molecule
        :rtype: rdkit.Chem.rdchem.Mol
        """

        mol, _ = self._to_mol(
            generate_bond_orders=generate_bond_orders, charge=charge
        )
        for atom in mol.GetAtoms():
            atom.SetAtomMapNum(0)
        return mol

    @classmethod
    def from_rdmol(cls, rdmol, use_atom_map_number=False) -> Self:
        """
        Creates a StereoMolGraph from an RDKit Mol object.
        Implicit Hydrogens are added to the graph.
        Stereo information is conserved. Double bonds, aromatic bonds and
        conjugated bonds are interpreted as planar. Atoms with 5 bonding
        partners are assumed to be TrigonalBipyramidal and allow interchange
        of the substituents (berry pseudorotation). Atoms with 6 bonding
        partners are assumed to be octahedral and do not allow interchange of
        the substituents.

        :param rdmol: RDKit Mol object
        :type rdmol: rdkit.Chem.Mol
        :param use_atom_map_number: If the atom map number should be used
                                    instead of the atom index
        :return: StereoMolGraph
        :rtype: StereoMolGraph
        """
        rdmol = Chem.AddHs(rdmol, explicitOnly=True, addCoords=True)
        if use_atom_map_number is False:
            rdmol = rdkit.Chem.rdmolops.AddHs(rdmol, explicitOnly=True)

        graph = cls()

        if use_atom_map_number:
            id_atom_map = {
                atom.GetIdx(): atom.GetAtomMapNum()
                for atom in rdmol.GetAtoms()
            }
        else:
            id_atom_map = {
                atom.GetIdx(): atom.GetIdx() for atom in rdmol.GetAtoms()
            }

        for atom in rdmol.GetAtoms():
            graph.add_atom(id_atom_map[atom.GetIdx()], atom.GetSymbol())

        for bond in rdmol.GetBonds():
            graph.add_bond(
                id_atom_map[bond.GetBeginAtomIdx()],
                id_atom_map[bond.GetEndAtomIdx()],
            )
        return graph

    def relabel_atoms(
        self, mapping: dict[int, int], copy: bool = True
    ) -> Self:
        """Changes the atom labels according to mapping.
        :param mapping: dict used for map old atom labels to new atom labels
        :type mapping: dict[int, int]
        :param copy: defines if the relabeling is done inplace or a new object
                     should be created
        :type copy: bool
        :return: this object (self) or a new instance of self.__class__
        :rtype: Self
        """
        new_graph = self._graph.relabel_nodes(mapping=mapping, copy=copy)
        if copy is True:
            new_mol_graph = self.__class__()
            new_mol_graph._graph = new_graph
            return new_mol_graph
        if copy is False:
            return self

    def connected_components(self) -> tuple[set[int], ...]:
        """
        :return: Returns the connected components of the graph
        :rtype: tuple[set[int], ...]
        """
        return self._graph.connected_components

    def node_connected_component(self, atom: int) -> set[int]:
        """
        :param atom: atom id
        :type atom: int
        :return: Returns the connected component that includes atom_id
        :rtype: set[Atoms]
        """
        return nx.node_connected_component(self._graph._nx_graph, atom)

    def subgraph(self, atoms: Iterable[int]) -> Self:
        """
        Returns a subgraph copy only containing the given atoms
        :param atoms: Iterable of atom ids to be
        :type atoms: Iterable[Int]
        :return: Subgraph
        :rtype: Self
        """
        subgraph = self.__class__()
        subgraph._graph = self._graph.subgraph(atoms)
        return subgraph

    def copy(self) -> Self:
        """
        :return: returns a copy of self
        :rtype: Self
        """
        graph = self.__class__()
        graph._graph = self._graph.copy()
        return graph

    def bonds_from_bond_order_matrix(
        self,
        matrix: np.ndarray | scipy.sparse.sparray,
        threshold: float = 0.5,
        include_bond_order: bool = False,
    ) -> None:
        """
        Adds bonds the the graph based on bond orders from a matrix
        :param matrix: Bond order Matrix
        :type matrix: np.ndarray
        :param threshold: Threshold for bonds to be included as edges,
                          defaults to 0.5
        :type threshold: float, optional
        :param include_bond_order: If bond orders should be included as edge
                                   attributes, defaults to False
        :type include_bond_order: bool, optional
        """
        if not np.shape(matrix) == (len(self), len(self)):
            raise ValueError(
                "Matrix has the wrong shape. shape of matrix is "
                f"{np.shape(matrix)}, but {len(self), len(self)} "
                "expected"
            )

        bonds = (matrix > threshold).nonzero()

        for i, j in zip(*bonds):
            if include_bond_order:
                self.add_bond(i, j, bond_order=matrix[i, j])
            else:
                self.add_bond(i, j)

    @classmethod
    def from_composed_molgraphs(cls, mol_graphs: Iterable[Self]) -> Self:
        """
        Combines all graphs in the iterable into one. Duplicate nodes or edges
        are overwritten, such that the resulting graph only contains one node
        or edge with that name. Duplicate attributes of duplicate nodes or
        edges are also overwritten in order of iteration.
        :param molgraphs: Iterable of MolGraph that will be composed into a
                          single MolGraph
        :type molgraphs: Iterable[Self]
        """
        new_graph = cls()
        new_graph._graph = UndirectedGraph.from_composed_graphs(
            [m._graph for m in mol_graphs]
        )
        return new_graph

    @classmethod
    def from_atom_types_and_bond_order_matrix(
        cls,
        atom_types: Sequence[int | Element | str],
        matrix: np.ndarray,
        threshold=0.5,
        include_bond_order=False,
    ):
        """

        :param atom_types: list of atom types as integers or symbols,
                           must correspond to the matrix
        :type atom_types:
        :param matrix: np.matrix of bond orders or connectivities ([0..1])
        :type matrix: np.ndarray
        :param threshold: Threshold for bonds to be included as edges,
                          defaults to 0.5
        :type threshold: float, optional
        :param include_bond_order: If bond orders should be included as edge
                                   attributes, defaults to False
        :type include_bond_order: bool, optional
        :return: Returns MolGraph
        :rtype: MolGraph
        """
        if not len(atom_types) == np.shape(matrix)[0] == np.shape(matrix)[1]:
            raise ValueError(
                "atom_types and matrix have to have the same length"
            )
        new_mol_graph = cls()
        gt_thresh = (matrix > threshold) * matrix

        if include_bond_order is True:
            new_graph = new_mol_graph._graph.from_numpy_array(
                gt_thresh, edge_attr="bond_order"
            )
        else:
            new_graph = new_mol_graph._graph.from_numpy_array(gt_thresh)

        new_graph.set_node_attributes(
            {i: PTOE[atom_type] for i, atom_type in enumerate(atom_types)},
            name="atom_type",
        )

        new_mol_graph._graph = new_graph

        return new_mol_graph

    @classmethod
    def from_atom_types_and_bond_order_sparse_array(
        cls,
        atom_types: Sequence[int | Element | str],
        sp_arr: scipy.sparse.sparray,
        threshold: float = 0.5,
        include_bond_order=False,
    ):
        """

        :param atom_types: list of atom types as integers or symbols,
                           must correspond to the array
        :type atom_types:
        :param matrix: scipy.sparse.sparray of bond orders or connectivities
                       ([0..1])
        :type matrix: scipy.sparse.sparray
        :param threshold: Threshold for bonds to be included as edges,
                          defaults to 0.5
        :type threshold: float, optional
        :param include_bond_order: If bond orders should be included as edge
                                   attributes, defaults to False
        :type include_bond_order: bool, optional
        :return: Returns MolGraph
        :rtype: MolGraph
        """
        if not len(atom_types) == np.shape(sp_arr)[0] == np.shape(sp_arr)[1]:
            raise ValueError(
                "atom_types and matrix have to have the same length"
            )
        new_mol_graph = cls()
        with warnings.catch_warnings():
            warnings.simplefilter(
                action="ignore", category=scipy.sparse.SparseEfficiencyWarning
            )

            # catching SparseEfficiencyWarning:
            # Comparing a sparse matrix with a scalar greater than zero
            # using < is inefficient, try using >= instead.
            gt_thresh = (threshold > sp_arr) * sp_arr

        if include_bond_order is True:
            new_graph = new_mol_graph._graph.from_numpy_array(
                gt_thresh, edge_attr="bond_order"
            )
        else:
            new_graph = new_mol_graph._graph.from_numpy_array(gt_thresh)

        new_graph.set_node_attributes(
            {i: PTOE[atom_type] for i, atom_type in enumerate(atom_types)},
            name="atom_type",
        )

        new_mol_graph._graph = new_graph

        return new_mol_graph

    @classmethod
    def from_geometry_and_bond_order_matrix(
        cls: type[Self],
        geo: Geometry,
        matrix: np.ndarray,
        threshold: float = 0.5,
        include_bond_order: bool = False,
    ) -> Self:
        """
        Creates a graph of a molecule from a Geometry and a bond order matrix.
        :param geo: Geometry
        :type geo: Geometry
        :param matrix: Bond order matrix
        :type matrix: np.ndarray
        :param threshold: Threshold for bonds to be included as edges,
                          defaults to 0.5
        :type threshold: float, optional
        :param include_bond_order: If bond orders should be included as edge
                                   attributes, defaults to False
        :type include_bond_order: bool, optional
        :return: Graph of Molecule
        :rtype: Self
        """
        new_mol_graph = cls.from_atom_types_and_bond_order_matrix(
            geo.atom_types,
            matrix,
            threshold=threshold,
            include_bond_order=include_bond_order,
        )
        return new_mol_graph

    @classmethod
    def from_geometry(
        cls: type[Self],
        geo: Geometry,
        switching_function: Optional[ISwitchingFunction] = None,
    ) -> Self:
        """
        Creates a graph of a molecule from a Geometry and a switching Function.
        Uses the Default switching function if none are given
        :param geo:
        :type geo: Geometry
        :param switching_function: Function to determine if two atoms are
                                    connected
        :type switching_function: ISwitchingFunction, optional
        :return: graph of molecule
        :rtype: Self
        """
        switching_function = (
            switching_function
            if switching_function is not None
            else StepSwitchingFunction()
        )
        connectivity_matrix = switching_function.array(
            geo.coords, geo.atom_types
        )
        return cls.from_geometry_and_bond_order_matrix(
            geo,
            connectivity_matrix,
        )

    def get_subgraph_isomorphic_mappings(
        self, other: Self
    ) -> Iterator[dict[int, int]]:
        """Subgraph isomorphic mappings from "other" onto "self".

        Generates all node-iduced subgraph isomorphic mappings.
        All atoms of "other" have to be present in "self".
        The bonds of "other" have to be the subset of the bonds of "self"
        relating to the nodes of "other".

        :param other: Other Graph to compare with
        :type other: Self
        :return: Mappings from the atoms of self onto the atoms of other
        :rtype: Iterator[dict[int, int]]
        :raises
        """
        return self._get_subgraph_isomorphic_mappings(
            other=other, _node_match=eq, _edge_match=eq
        )

    def _get_subgraph_isomorphic_mappings(
        self, other: Self, _node_match=eq, _edge_match=eq
    ) -> Iterator[dict[int, int]]:
        """Subgraph isomorphic mappings from "other" onto "self".

        Generates all node-iduced subgraph isomorphic mappings.
        All atoms of "other" have to be present in "self".
        The bonds of "other" have to be the subset of the bonds of "self"
        relating to the nodes of "other".

        :param other: Other Graph to compare with
        :type other: Self
        :return: Mappings from the atoms of self onto the atoms of other
        :rtype: Iterator[dict[int, int]]
        :raises TypeError: Not defined for objects different types
        """
        if not isinstance(self, type(other)):
            raise TypeError("Not defined for objects of different types")
        return self._graph._get_subgraph_isomorphic_mappings(
            other._graph, _node_match=_node_match, _edge_match=_edge_match
        )

    def get_subgraph_monomorphic_mappings(
        self, other: Self
    ) -> Iterator[dict[int, int]]:
        """Subgraph monomorphic mappings from "other" onto "self".

        Generates all subgraph monomorphic mappings.
        All atoms of other have to be present in "self".
        The bonds of "other" have to be a subset of the bonds of "self".

        :param other: Other Graph to compare with
        :type other: Self
        :return: Mappings from the atoms of self onto the atoms of other
        :rtype: Iterator[dict[int, int]]
        :raises TypeError: Not defined for objects different types
        """
        return self._get_subgraph_monomorphic_mappings(
            other=other, _node_match=eq, _edge_match=eq
        )

    def _get_subgraph_monomorphic_mappings(
        self, other: Self, _node_match=eq, _edge_match=eq
    ) -> Iterator[dict[int, int]]:
        if not isinstance(self, type(other)):
            raise TypeError("Not defined for objects of different types")
        return self._graph.get_subgraph_monomorphic_mappings(other._graph)

    def get_isomorphic_mappings(self, other: Self) -> Iterator[dict[int, int]]:
        """Isomorphic mappings between "self" and "other".

        Generates all isomorphic mappings between "other" and "self".
        All atoms and bonds have to be present in both graphs.

        :param other: Other Graph to compare with
        :type other: Self
        :return: Mappings from the atoms of self onto the atoms of other
        :rtype: Iterator[dict[int, int]]
        :raises TypeError: Not defined for objects different types
        """
        return self._get_isomorphic_mappings(
            other=other, _node_match=eq, _edge_match=eq
        )

    def _get_isomorphic_mappings(
        self, other: Self, _node_match=eq, _edge_match=eq
    ) -> Iterator[dict[int, int]]:
        if not isinstance(self, type(other)):
            raise TypeError("Not defined for objects of different types")
        return self._graph._get_isomorphic_mappings(
            other._graph, _node_match=_node_match, _edge_match=_edge_match
        )

    def is_isomorphic(self, other: Self) -> bool:
        """
        Checks if the graph is isomorphic to another graph.

        :param other: other graph
        :type other: Self
        :return: True if isomorphic
        :rtype: bool
        """
        return any(self.get_isomorphic_mappings(other))

    def get_automorphic_mappings(self) -> Iterator[dict[int, int]]:
        """
        :return: Returns all possible mappings of the MolGraph onto itself
        :rtype: dict[atom, atom]
        """
        return self._get_automorphic_mappings(_node_match=eq, _edge_match=eq)

    def _get_automorphic_mappings(
        self, _node_match=eq, _edge_match=eq
    ) -> Iterator[dict[int, int]]:
        return self._get_isomorphic_mappings(
            other=self, _node_match=_node_match, _edge_match=_edge_match
        )

    def get_automorphic_structures(
        self,
        atoms: tuple[int, ...],
    ) -> frozenset[tuple[int, ...]]:
        """
        Returns all automorphic reoccurrences of the given atoms in structure
        Can be used for single atoms, two atoms (for bonds),
        three atoms(for angles), four atoms (for dihedrals) and n atoms for any
        structure for example identical reactive sides.

        :param atoms: Atoms to be used for search
        :type atoms: tuple[int, ...]
        :return: Automorphically equivalent sets of atoms
        :rtype: set[tuple[atom_id]]
        """
        return frozenset(
            (
                tuple(mapping[atom] for atom in atoms)
                for mapping in self.get_automorphic_mappings()
            )
        )

    def hash_1_wl(
        self,
        max_steps=None,
        atom_attrs: Iterable[str] = (),
        bond_attrs: Iterable[str] = (),
    ) -> int:
        """1-WL algorithm (Weisfeiler-Lehman).

        Fast graph hashing alorithm for nearly all chemically relevant systems.
        1-WL is not able to distinguish between highly symmetric cyclic graphs.

        Shervashidze, Nino, Pascal Schweitzer, Erik Jan Van Leeuwen,
        Kurt Mehlhorn, and Karsten M. Borgwardt. Weisfeiler Lehman
        Graph Kernels. Journal of Machine Learning Research. 2011.
        http://www.jmlr.org/papers/volume12/shervashidze11a/shervashidze11a.pdf

         :param max_steps: Maximal number of weisfeiler Lehman steps to use.
                         If None the algorithim is continued to convergence,
                         defaults to None
         :type max_steps: int|None, optional
        """

        atom_attrs = set(atom_attrs)
        atom_attrs.add("atom_type")

        node_labels = {
            atom: hash(
                (
                    frozenset(
                        self.get_atom_attributes(atom, atom_attrs).items()
                    ),
                    frozenset(
                        (
                            frozenset(
                                self.get_atom_attributes(n, atom_attrs).items()
                            ),
                            frozenset(
                                self.get_bond_attributes(
                                    atom, n, bond_attrs
                                ).items()
                            ),
                        )
                        for n in self.bonded_to(atom)
                    ),
                )
            )
            for atom in self.atoms
        }

        subgraph_hash_counts:list = []

        for _ in itertools.count(0) if max_steps is None else range(max_steps):
            old_counter = Counter(node_labels.values())

            node_labels = self._wl_step(
                node_labels,
                bond_attrs=bond_attrs,
            )

            counter = Counter(node_labels.values())

            if frozenset(counter.values()) == frozenset(old_counter.values()):
                break

            subgraph_hash_counts.extend(frozenset(counter.items()))

        return hash(tuple(subgraph_hash_counts))

    def _wl_step(
        self,
        labels: dict[int, Any],
        bond_attrs: Iterable[str],
    ) -> dict[int, Any]:
        """
        Apply neighborhood aggregation to each node
        in the graph.
        Computes a dictionary with labels for each node.
        """
        new_labels = {}
        for atom in self.atoms:
            neighbor_labels = Counter(
                [labels[neighbor] for neighbor in self.bonded_to(atom)]
            )

            new_labels[atom] = hash(
                (labels[atom], frozenset(neighbor_labels.items()))
            )

        return new_labels


class MDMoleculeNetwork(DirectedGraph):
    """A directed graph representing a network of molecules from molecular
    dynamics simulations.
    """

    def __init__(self):
        """Initialize an empty MDMoleculeNetwork."""
        super().__init__()

    @property
    def nodes(self) -> Iterable[int]:
        """Get all nodes in the network without their data attributes.

        :return: Iterable of node IDs
        :rtype: Iterable[int]
        """
        return self._nx_graph.nodes(data=False)

    def predecessors(self, node: int) -> Iterable[int]:
        """Get all predecessor nodes that have edges pointing to the
            given node.

        :param node: Node ID to get predecessors for
        :type node: int
        :return: Iterable of predecessor node IDs
        :rtype: Iterable[int]
        """
        return self._nx_graph.predecessors(node)