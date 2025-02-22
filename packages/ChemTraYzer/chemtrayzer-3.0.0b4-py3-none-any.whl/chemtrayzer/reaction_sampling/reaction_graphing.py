# ruff: noqa
from pathlib import Path
import csv
from tempfile import TemporaryDirectory
import chemtrayzer.reaction_sampling.reaction_detection as reaction_detection
from chemtrayzer.reaction_sampling.reaction_detection import ReactionDetector
from chemtrayzer.core.md import TrajectoryParser
from chemtrayzer.jobs.ams import Trajectory
import chemtrayzer.core.graph as graphing
from chemtrayzer.core import chemid
from rdkit.Chem import MolFromSmiles
from rdkit.Chem import MolFromSmarts
from rdkit.Chem import rdDepictor
from rdkit.Chem import Draw
import logging
import rdkit
from enum import Enum
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


class DataOrigin(Enum):
    """
    Enum representing the origin of data used to instantiate a ReactionGraph object.

    Possible values:
    - MECHANISM: Data originated from a Chemkin mechanism file.
    - REACTION_OUTPUT_STRING: Data originated from a reaction output string.
    - TRAJECTORY: Data originated from a chemtrayzer trajectory.
    """

    MECHANISM = "mechanism"
    REACTION_OUTPUT_STRING = "reaction_output_string"
    TRAJECTORY = "trajectory"

class ReactionGraph():
    """Class that implements a reaction network and filter functions to edit the graph.
       objects of this class should be created by calling one of its class methods.
    """


    def __init__(self, _data_origin: DataOrigin, _reactions: dict[chemid.Species, dict],
                     _has_weights: bool = False):
        self.is_directed = True

        self.has_weights = _has_weights
        self.data_origin = _data_origin
        self.reactions = _reactions

        self.graph = self._create_reaction_network()
        self.unique_species_smiles = list(self.graph.nodes)


        unique_species = set()
        for r in _reactions:
            unique_species.update(r.reactants)
            unique_species.update(r.products)
        self.unique_species = unique_species

        if self.has_weights is True:
            self._calculate_net_flow()
        else:
            for u, v in self.graph.edges:
                self.graph.set_edge_attribute(u, v, 'weight', 1.0)



    @classmethod
    def from_mechanism(cls, mech_location:Path, species_dict_location:Path):
        """constructor to create a reaction graph object from a chemkin mechanism file and an
           csv file that contains the smiles for the aliases of the molecules in the chemkin file

        :param mech_location: location of the chemkin mechanism file
        :type mech_location: Path
        :param species_dict_location: path to a csv file containing the name of the species as used
                                      in the mechanism in the first column and the corresponding SMILES
                                      in the second column
        :type species_dict_location: Path
        :return: reaction graph object
        :rtype: ReactionGraph
        """

        #create dict from speices dict csv
        smiles_dictionary=dict()
        with open(species_dict_location, "r", encoding='utf-8-sig') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in csv_reader:
                key_, smiles_=row[0:2]
                smiles_dictionary[key_] = smiles_

        #remove comments from mech file
        buffer = []
        with open(mech_location, 'r') as f:
            for line in f:
                if '!' in line:
                    pos = line.find('!')
                    line_wo_comment = line[:pos]
                    if '<=>' in line_wo_comment or '=>' in line_wo_comment or '<=' in line_wo_comment or '=' in line_wo_comment:
                        pos = line.find(' ')
                        if pos > 0:
                            buffer.append(line[:pos])
                        else:
                            buffer.append(line[:-1])

        mech_reactions = [] # list of tuples (reactions) of tuples (mols)
        for line in buffer:
            line = line.replace('(+M)','') # remove stosspartner info
            line = line.replace('+M','') # remove stosspartner info
            if '<=>' in line:
                sline = line.split('<=>')
                left  = tuple(sline[0].split('+'))
                right = tuple(sline[1].split('+'))
                mech_reactions.append( tuple([ left , right ]) )
                mech_reactions.append( tuple([ right , left ]) ) # reverse
            elif '=>' in line:
                sline = line.split('=>')
                left  = tuple(sline[0].split('+'))
                right = tuple(sline[1].split('+'))
                mech_reactions.append( tuple([ left , right ]) )
            elif '<=' in line:
                sline = line.split('<=')
                left  = tuple(sline[0].split('+'))
                right = tuple(sline[1].split('+'))
                mech_reactions.append( tuple([ right , left ]) )
            elif '=' in line:
                sline = line.split('=')
                left  = tuple(sline[0].split('+'))
                right = tuple(sline[1].split('+'))
                mech_reactions.append( tuple([ right , left ]) )

        # reduce mech list to reactions that have a SMILES
        reactions = {}
        for reac,prod in mech_reactions:
            reactant_smiles = []
            product_smiles = []
            skip = False
            for s in reac:
                if s in smiles_dictionary:
                    reactant_smiles.append(smiles_dictionary[s])
                else:
                    skip = True # ignore and continue with next
                    break
            if skip:
                continue
            for s in prod:
                if s in smiles_dictionary:
                    product_smiles.append(smiles_dictionary[s])
                else:
                    skip = True # ignore and continue with next
                    break
            if skip:
                continue



            reactant_species = [chemid.Species.from_smiles(smiles= s) for s in reactant_smiles]
            product_species = [chemid.Species.from_smiles(smiles= s) for s in product_smiles]

            r=chemid.Reaction(reactants=reactant_species, products=product_species)
            reactions.update({r : {"count" : 1}})


        return cls(_data_origin=DataOrigin.MECHANISM, _reactions=reactions)

    @classmethod
    def from_reaction_output_string(cls, reaction_string:str):
        """constructor to create a reaction graph object from a string of reactions.

        :param reaction_string: reaction string output from the chemtrayzer in the form:
                                "<Reaction_Nr>: <reactant1> + <reactant2> -> <product1> + <product2>"
                                replacing the values in the <> with the corresponding smiles or Number
        :type reaction_string: str
        :return: reaction graph object
        :rtype: ReactionGraph
        """

        reaction_string = reaction_string.split("\n")[1:-1]

        reactions = {}
        has_weights = False
        for i, reaction in enumerate(reaction_string):
            _, reaction = reaction.split(":")

            right, left = reaction.split(" -> ")
            reactant_smiles = right.split(" + ")
            reactant_smiles = [reac.strip() for reac in reactant_smiles]

            product_smiles = left.split(" + ")
            product_smiles = [prod.strip() for prod in product_smiles]

            reactant_species = [chemid.Species.from_smiles(smiles= s) for s in reactant_smiles]
            product_species = [chemid.Species.from_smiles(smiles= s) for s in product_smiles]

            reaction = chemid.Reaction(reactants=reactant_species, products=product_species)

            if reaction in reactions:
                reactions[reaction]["count"] += 1
                has_weights = True
            elif reaction not in reactions:
                reactions.update({reaction : {"count" : 1}})


        return cls(_data_origin=DataOrigin.REACTION_OUTPUT_STRING, _reactions = reactions, _has_weights=has_weights)

    @classmethod
    def from_parser(
        cls,
        parser: TrajectoryParser,
        n_frames: int = -1,
        bond_initial_threshold: float = 0.5,
        bond_breaking_threshold: float = 0.3,
        bond_forming_threshold: float = 0.8,
        molecule_stable_time: float = 0.1,
    ) -> "ReactionGraph":
        """Create a ReactionGraph from a TrajectoryParser instance.

        This method analyzes the trajectory and detects reactions based on the
        given bond thresholds and molecule stability criteria.

        :param parser: Parser containing trajectory data
        :param n_frames: Number of frames to analyze. Defaults to entire
                         trajectory
        :param bond_initial_threshold: Threshold for initial bond detection
        :param bond_breaking_threshold: Threshold below which a bond is
                                        considered broken
        :param bond_forming_threshold: Threshold above which a bond is
                                        considered formed
        :param molecule_stable_time: Time a molecule must be stable to be
                                     considered a product/reactant
        :return: New ReactionGraph instance containing detected reactions
        :rtype: ReactionGraph
        """

        reaction_detector = ReactionDetector(
            parser=parser,
            bond_initial_threshold=bond_initial_threshold,
            bond_breaking_threshold=bond_breaking_threshold,
            bond_forming_threshold=bond_forming_threshold,
            molecule_stable_time=molecule_stable_time,
        )

        # go through the trajectory connectivity
        # and create molecules and reactions
        reaction_detector.detect(n_frames=n_frames)

        reactions = {}
        for reactive_event in reaction_detector.reactive_events:
            reaction = reactive_event.reaction
            if reaction in reactions:
                reactions[reaction]["count"] += 1
            elif reaction not in reactions:
                reactions.update({reaction : {"count" : 1}})
            else:
                raise Exception(
                    "Error: The reaction detector does not contain any "
                    "reactive events"
                )

        return cls(
            _data_origin=DataOrigin.TRAJECTORY,
            _reactions=reactions,
            _has_weights=True,
        )


    def _create_reaction_network(self):
        """Function to generate a graph of the reaction network. May be replaced later
           by a different implementation

        :return: graph of the reaction network
        :rtype: graphing.Graph
        """
        graph = graphing.UndirectedGraph()
        # add nodes for each reaction
        for i, reaction in enumerate(self.reactions):
            for reactant_ in reaction.reactants:
                graph.add_node(reactant_.smiles, hash = reactant_.id )
                for product_ in reaction.products:
                    graph.add_node(product_.smiles, hash = product_.id)
        # add edges
        for i, reaction in enumerate(self.reactions):
            for reactant_ in reaction.reactants:
                for product_ in reaction.products:
                    graph.add_edge(reactant_.smiles, product_.smiles)
        return graph

    #########################################
    ##            utilities                ##
    #########################################


    def _calculate_net_flow(self):
        """
        Assigns the weight count of each reaction to the corresponding edge in the graph.
        """
        for u, v in self.graph.edges:
            self.graph.set_edge_attribute(u, v, "weight", 1)

        for reaction in self.reactions:
            weight = self.reactions[reaction]["count"]
            for reactant in reaction.reactants:
                for product in reaction.products:
                    self.graph.set_edge_attribute(reactant.smiles, product.smiles, "weight", weight)


    def _get_CH_count(self, mol):
        """Function to calculate the number of carbon and hydrogen atoms in a molecule.

        :param mol: RDkit Molecule object
        :type mol: rdkit.Chem.rdchem.Mol
        :return: number of carbon and hydrogen atoms in the molecule
        :rtype: list
        """

        # https://www.daylight.com/dayhtml_tutorials/languages/smarts/smarts_examples.html
        # https://en.wikipedia.org/wiki/SMILES_arbitrary_target_specification
        # https://www.ics.uci.edu/~dock/manuals/DaylightTheoryManual/theory.smarts.html
        carbon_saturation = []
        for smarts in ["[#6H0]", "[#6H1]", "[#6H2]", "[#6H3]", "[#6H4]"]:  # quarternary carbon etc, aromatic C "[cH1]"
            patt = MolFromSmarts(smarts)
            pm = mol.GetSubstructMatches(patt)
            carbon_saturation.append(len(pm))
        carbon_saturation = tuple(carbon_saturation)
        carbon_hydrogen_numbers = [sum(carbon_saturation), carbon_saturation[1] + 2 * carbon_saturation[2] + 3 * carbon_saturation[3] + 4 * carbon_saturation[4]]
        return carbon_hydrogen_numbers

    def min_edge_flow(self, min_edge_flow: int):
        """Function to delete edges that have less than desired flow (number of reaction events).
            Only if a correct timeseries of reactions is given.

        :param min_edge_flow: minimum edge weight, e.g. the minimum number of observations
                              for the reactions
        :type min_edge_flow: int
        :raises Exception: Raises an exception when the user attempts to use this function on
                           Graphs that do not contain any edge weight information
        """

        if self.has_weights is True:
            if min_edge_flow > 1:
                for (u, v), attributes in self.graph.get_edges_with_attributes().items():
                    if attributes["weight"] < min_edge_flow:
                        self.graph.remove_edge(u,v)

        elif self.has_weights is False:
            raise Exception("Error: The graph edges do not have weights")

    def min_CH_count(self, min_CH_count: int):
        """Function to delete nodes that have less than desired carbon atoms.

        :param min_CH_count: integer of minimum required carbon atoms per molecule
        :type min_CH_count: int
        """


        if min_CH_count > 0:
            for smiles in self.unique_species_smiles:
                mol = MolFromSmiles(smiles)
                if mol is not None:
                    c_count, h_count = self._get_CH_count(mol)
                    if c_count < min_CH_count:
                        self.graph.remove_node(smiles)
                        self.unique_species_smiles.remove(smiles)
                        self.unique_species = [spec for spec in self.unique_species if spec.smiles != smiles ]

    def remove_nodes_from_blacklist(self, species_blacklist: list):
        """Function to delete nodes that are on the blacklist.

        :param species_blacklist: list of molecule smiles that are forbidden in the graph
        :type species_blacklist: list
        """

        if isinstance(species_blacklist, list) and len(species_blacklist) != 0:
            for smile in species_blacklist:
                if self.graph.has_node(smile):
                    self.graph.remove_node(smile)

    def remove_nodes_not_on_whitelist(self, species_whitelist: list):
        """Function to delete nodes that are not on the whitelist.

        :param species_whitelist: list of molecule smiles that are allowed in the graph
        :type species_whitelist: list
        """
        if isinstance(species_whitelist, list) and len(species_whitelist) != 0:
            for smiles in self.unique_species_smiles:
                if smiles not in species_whitelist:
                    if self.graph.has_node(smiles):
                        self.graph.remove_node(smiles)

class YED_Graph():
    """Class that represents a YED graph. With added functionality to write to a graphml file,
       to be read by the yed software.
    """
    def __init__(self, r_graph:ReactionGraph):
        self.r_graph = r_graph

        self.temp_image_dir = TemporaryDirectory()
        self.imgSize = (300,300)

        #create pictures for each speceies in the set of reactions
        for species in self.r_graph.unique_species:
            mol = MolFromSmiles(species.smiles)
            if mol is not None:
                self._mol_to_svg(mol=mol, id=species.id)
            else:
                #if no image can be molecule, create a svg image of the molecular formula
                logging.debug(f"An unusual smile was used for rdkit Mol creation: {species.smiles}")
                self._formula_to_svg(mol_formula=species.formula, id=species.id)


    def _formula_to_svg(self, mol_formula:str, id:str):
        """function to create a simple svg (image) of the molecular formula of a molecule.
        Only to be used if molecule generation using rdkit failed

        :param mol_formula: string of the molecular formula. E.g "H2O"
        :type mol_formula: str
        :param id: id or name of the image file that will be generated
        :type id: str
        """

        formula_svd="""<?xml version='1.0' encoding='iso-8859-1'?>
<svg version='1.1' baseProfile='full'
xmlns='http://www.w3.org/2000/svg'
        xmlns:rdkit='http://www.rdkit.org/xml'
        xmlns:xlink='http://www.w3.org/1999/xlink'
    xml:space='preserve'
width='{imgSizex}px' height='{imgSizey}px' viewBox='0 0 300 300'>
<text x="50%" y="50%" text-anchor="middle" alignment-baseline="middle" font-size="48" fill="black">{formula}</text>
</svg>""".format(formula=mol_formula, imgSizex=self.imgSize[0], imgSizey=self.imgSize[1])


        with open(self.temp_image_dir.name + id + ".svg", "w") as wf:
            wf.write(formula_svd)
        return


    def _mol_to_svg(self, mol, id:str):
        """Function to generate svg image from rdkit mol object

        :param mol: RDkit molecule object from which the image will ge generated
        :type mol: rdkit.Chem.rdchem.Mol
        :param id: id or name of the image file that will be generated
        :type id: str
        """
        rdDepictor.Compute2DCoords(mol)

        drawer = Draw.MolDraw2DSVG(self.imgSize[0], self.imgSize[1])
        drawer.DrawMolecule(mol)
        drawer.FinishDrawing()
        svg = drawer.GetDrawingText()

        # Write the SVG string to a file

        with open(self.temp_image_dir.name + id + ".svg", "w") as wf:
            wf.write(svg)
        return


    def _mol_to_png(self, mol, id:str):
        """Function to generate png image from rdkit mol object

        :param mol: RDkit molecule object from which the image will ge generated
        :type mol: rdkit.Chem.rdchem.Mol
        :param id: id or name of the image file that will be generated
        :type id: str
        """

        rdDepictor.Compute2DCoords(mol)
        img = Draw.MolToImage(mol, size=(self.imgSize[0], self.imgSize[1]))

        # Save the image to a file
        img.save(self.temp_image_dir.name + id + ".svg")

        return


    def save_reaction_network_GraphML(self, file_dir:Path, file_name:str):
        """function to save a reaction graph in the graphml file format with additional
           informationf for YED.

        :param file_dir: Path where the file should be stored
        :type file_dir: Path
        :param file_name: Name for the graphml file. Should end in .graphml
        :type file_name: str
        """


        ##############
        # l0   ####
        ##############


        root = ET.Element( "graphml", {"xmlns" : "http://graphml.graphdrawing.org/xmlns",
                                    "xmlns:java" : "http://www.yworks.com/xml/yfiles-common/1.0/java",
                                    "xmlns:sys" : "http://www.yworks.com/xml/yfiles-common/markup/primitives/2.0",
                                    "xmlns:x" : "http://www.yworks.com/xml/yfiles-common/markup/2.0",
                                    "xmlns:xsi" : "http://www.w3.org/2001/XMLSchema-instance",
                                    "xmlns:y" : "http://www.yworks.com/xml/graphml",
                                    "xmlns:yed" : "http://www.yworks.com/xml/yed/3",
                                    "xsi:schemaLocation" : ["http://graphml.graphdrawing.org/xmlns",
                                                            "http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd"]})


        ##############
        ## l1   ####
        ##############


        # Create the key element
        ET.SubElement(root, "key", {
            "for": "port",
            "id": "d1",
            "yfiles.type": "portgraphics"
        })
        ET.SubElement(root, "key", {
            "for": "port",
            "id": "d2",
            "yfiles.type": "portgeometry"
        })
        ET.SubElement(root, "key", {
            "for": "port",
            "id": "d3",
            "yfiles.type": "portuserdata"
        })
        ET.SubElement(root, "key", {
            "for": "node",
            "id": "d6",
            "yfiles.type": "nodegraphics"
        })
        ET.SubElement(root, "key", {
            "for": "graphml",
            "id": "d7",
            "yfiles.type": "resources"
        })
        ET.SubElement(root, "key", {
            "for": "edge",
            "id": "d10",
            "yfiles.type": "edgegraphics"
        })
        ET.SubElement(root, "key", {
            "attr.name": "url",
            "attr.type": "string",
            "for": "node",
            "id": "d4"
        })
        ET.SubElement(root, "key", {
            "attr.name": "url",
            "attr.type": "string",
            "for": "edge",
            "id": "d8"
        })
        ET.SubElement(root, "key", {
            "attr.name": "description",
            "attr.type": "string",
            "for": "node",
            "id": "d5"
        })
        ET.SubElement(root, "key", {
            "attr.name": "description",
            "attr.type": "string",
            "for": "edge",
            "id": "d9"
        })
        ET.SubElement(root, "key", {
            "attr.name": "Description",
            "attr.type": "string",
            "for": "graph",
            "id": "d0"
        })

        # Create the graph element
        graph_elem = ET.SubElement(root, "graph", {
            "edgedefault": "directed" if self.r_graph.is_directed else "undirected",
            "id": "G"
        })

        # Create the data element
        data_elem_d7 = ET.SubElement(root, "data", {"key" : "d7" })


        ##############
        #### l2   ####
        ##############
        ET.SubElement(graph_elem, "data", {"key":"d0"})

        # Iterate over nodes and create node elements
        for i, node in enumerate(self.r_graph.graph.nodes):
            node_elem = ET.SubElement(graph_elem, "node", {"id": str(node)})

            node_data_elem = ET.SubElement(node_elem, "data", {"key":"d5"})
            node_data_elem = ET.SubElement(node_elem, "data", {"key":"d6"})
            SVGNode = ET.SubElement(node_data_elem, "y:SVGNode")
            ET.SubElement(SVGNode, "y:Geometry", {
                                                                "height":str(self.imgSize[1]),
                                                                "width":str(self.imgSize[1]),
                                                                "x":"0",
                                                                "y":"0"
                                                            })
            ET.SubElement(SVGNode, "y:Fill", {"color":"#CCCCFF", "transparent": "false"})
            ET.SubElement(SVGNode, "y:BorderStyle" , {"color": "#000000",
                                                                    "type": "line",
                                                                    "width": "1.0"})
            ET.SubElement(SVGNode, "y:NodeLabel",  {"alignment":"center",
                                                                "autoSizePolicy":"content",
                                                                "fontFamily":"Dialog",
                                                                "fontSize":"12",
                                                                "fontStyle":"plain",
                                                                "hasBackgroundColor":"false",
                                                                "hasLineColor":"false",
                                                                "hasText":"false",
                                                                "height":"4.0",
                                                                "horizontalTextPosition":"center",
                                                                "iconTextGap":"4",
                                                                "modelName":"sandwich",
                                                                "modelPosition":"s",
                                                                "textColor":"#000000",
                                                                "verticalTextPosition":"bottom",
                                                                "visible":"true",
                                                                "width":"4.0",
                                                                "x":"0",
                                                                "y":"0"})


            ET.SubElement(SVGNode, "y:SVGNodeProperties", {"usingVisualBounds":"true"})
            SVGModel = ET.SubElement(SVGNode, "y:SVGModel", {"svgBoundsPolicy":"0"})
            ET.SubElement(SVGModel, "y:SVGContent", {"refid" : str(i)})


        # calculate optimal line widths by interpolating between the min and max weights in the graph
        # e.g. find a map [weight_min, weight_max] -> [width_min, width_max]

        width_min = 1
        width_max = 10
        weight_min = 1
        weight_max = max([attributes['weight'] for attributes in self.r_graph.graph.get_edges_with_attributes().values()])



        for u, v in self.r_graph.graph.edges:
            edge_elem = ET.SubElement(graph_elem, "edge", {
                            "source": str(u),
                            "target": str(v)})

            ET.SubElement(edge_elem, "data", {"key" : "d9" }) # data_d9
            data_d10=ET.SubElement(edge_elem, "data", {"key" : "d10" })

            PolyLineEdge=ET.SubElement(data_d10, "y:PolyLineEdge")
            ET.SubElement(PolyLineEdge, "y:Path",)
            if self.r_graph.has_weights is True:
                weight = self.r_graph.graph.get_edge_attribute(u, v, "weight")
                width = (weight - weight_min) * (width_max - width_min) / (weight_max - weight_min) + width_min
            else :
                width = 1
            ET.SubElement(PolyLineEdge, "y:LineStyle",{"color":"#000000",
                                                                "type":"line",
                                                                "width": str(width)})
            ET.SubElement(PolyLineEdge, "y:Arrows",{"source":"none",
                                                            "target":"standard"})
            ET.SubElement(PolyLineEdge, "y:EdgeLabel",{})
            ET.SubElement(PolyLineEdge, "y:BendStyle", {"smoothed":"true"})
            #line_elem=ET.SubElement(PolyLineEdge, "y:PolyLineEdge")



        ##############
        #### l2   ####
        ##############

        Resources_elem = ET.SubElement(data_elem_d7, "y:Resources")
        for i, node in enumerate(self.r_graph.graph.nodes):
            svg_file = open(self.temp_image_dir.name + self.r_graph.graph.get_node_attribute(node,"hash") + ".svg")
            #svg_file = open(os.path.join(self.temp_image_dir, self.r_graph.G.nodes[node]["hash"] + ".svg"))
            svg_cont = svg_file.read()


            node_img = ET.SubElement(Resources_elem, "y:Resource", {"id":str(i), "xml:space":"preserve"})
            node_img.text = svg_cont




        # Create the ElementTree object
        ET.ElementTree(root)

        # Generate well-formatted XML as a string
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")

        # Write the XML string to a file
        with open(str(file_dir / file_name) , "w") as file:
            file.write(xml_str)
