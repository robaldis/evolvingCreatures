from src import genome
from xml.dom.minidom import getDOMImplementation

class Creature():
    def __init__(self, gene_count):
        self.spec = genome.Genome.get_gene_spec()
        self.dna = genome.Genome.get_random_genome(len(self.spec), gene_count)
        self.falt_liknks = None
        self.exp_links = None

    def get_flat_links(self):
        gdict = genome.Genome.get_genome_dict(self.dna, self.spec)
        self.flat_links = genome.Genome.genome_to_links(gdict)
        return self.flat_links

    def get_expanded_links(self):
        self.get_flat_links()
        self.exp_links = []
        genome.Genome.expand_links(self.flat_links[0], self.flat_links[0].name, self.flat_links, self.exp_links)
        return self.exp_links

    def to_xml(self):
        """
        converts the genome to an URDF xml
        """
        self.get_expanded_links()
        # Create the dom
        domimpl = getDOMImplementation()
        adom = domimpl.createDocument(None, "start", None)

        # Convert all the links
        robot_tag = adom.createElement("robot")
        for link in self.exp_links:
            robot_tag.appendChild(link.to_link_element(adom))

        # Convert all the joints
        first = True
        for link in self.exp_links:
            if first: # Skip the first node
                first = False
                continue
            robot_tag.appendChild(link.to_joint_element(adom))
            robot_tag.setAttribute("name", "ted")
        return robot_tag.toprettyxml()







