import numpy as np
import copy


class Genome():

    @staticmethod
    def get_random_gene(length=10):
        """
        Generates a list of random float values of a given length
        """
        gene = np.array([np.random.random() for i in range(length)])
        return gene

    @staticmethod
    def get_random_genome(gene_length, genome_count):
        """
        Generates a random list of a gene of a determined length, list of lists,
        """
        genome = [Genome.get_random_gene(gene_length) for i in range(genome_count)]
        return genome

    @staticmethod
    def get_gene_spec():
        """
        Lays out the specification for what a gene looks like. allows us to 
        unpack the gene
        """

        spec =  {
                "link-shape": {"scale":1},
                "link-length": {"scale":1},
                "link-radius": {"scale":1},
                "link-recurrence": {"scale":4},
                "link-mass": {"scale":1},
                "joint-mass":{"scale":1},
                "joint-type":{"scale":1},
                "joint-parent":{"scale":1},
                "joint-axis-xyz":{"scale":1},
                "joint-origin-rpy-1": {"scale":np.pi*2},
                "joint-origin-rpy-2": {"scale":np.pi*2},
                "joint-origin-rpy-3": {"scale":np.pi*2},
                "joint-origin-xyz-1": {"scale":1},
                "joint-origin-xyz-2": {"scale":1},
                "joint-origin-xyz-3": {"scale":1},
                "control-waveform": {"scale":1},
                "control-amp": {"scale":0.25},
                "control-freq": {"scale": 1}
                }

        ind = 0 
        for key in spec.keys():
            spec[key]["ind"] = ind
            ind = ind + 1

        return spec

    @staticmethod
    def expand_links(parent_link, uniq_parent_name, flat_links, exp_links):
        """
        Recurcivly expand the flat links to indervidual, more like how it will 
        be represented as a graph
        """
        children = [l for l in flat_links if l.parent_name == parent_link.name]
        sibling_ind = 1
        for c in children:
            for r in range(int(c.recur)):
                sibling_ind = sibling_ind + 1
                c_copy = copy.copy(c)
                c_copy.parent_name = uniq_parent_name
                uniq_name = c_copy.name + str(len(exp_links))
                c_copy.name = uniq_name
                c_copy.sibling_ind = sibling_ind
                exp_links.append(c_copy)
                Genome.expand_links(c, uniq_name, flat_links, exp_links)

    @staticmethod
    def get_gene_dict(gene, spec):
        gdict = {}
        for key in spec:
            ind = spec[key]["ind"]
            scale = spec[key]["scale"]
            gdict[key] = gene[ind] * scale

        return gdict

    @staticmethod
    def get_genome_dict(genome, spec):
        gdicts = []
        for gene in genome:
            gdicts.append(Genome.get_gene_dict(gene, spec))

        return gdicts

    @staticmethod
    def genome_to_links(dnaDict):
        links = []
        link_ind = 0
        parent_names = [str(link_ind)]

        for gdict in dnaDict:
            link_name = str(link_ind)
            parent_ind = gdict["joint-parent"] * len(parent_names)
            parent_name = parent_names[int(parent_ind)]
            recur = gdict["link-recurrence"] + 1
            link_length = gdict["link-length"]

            link = URDFLink(name = link_name, 
                    parent_name = parent_name,
                    recur = recur,
                    link_length = link_length, 
                    link_shape = gdict["link-shape"],
                    link_radius = gdict["link-radius"],
                    link_mass = gdict["link-mass"],
                    joint_type = gdict["joint-type"],
                    joint_axis_xyz = gdict["joint-axis-xyz"],
                    joint_origin_rpy_1 = gdict["joint-origin-rpy-1"],
                    joint_origin_rpy_2 = gdict["joint-origin-rpy-2"],
                    joint_origin_rpy_3 = gdict["joint-origin-rpy-3"],
                    joint_origin_xyz_1 = gdict["joint-origin-xyz-1"],
                    joint_origin_xyz_2 = gdict["joint-origin-xyz-2"], 
                    joint_origin_xyz_3 = gdict["joint-origin-xyz-3"],
                    control_waveform = gdict["control-waveform"],
                    control_amp = gdict["control-amp"],
                    control_freq = gdict["control-freq"])

            links.append(link)
            if link_ind != 0: # don't re-add the first link
                parent_names.append(link_name)
            link_ind  = link_ind + 1
        links[0].parent_name = "None" # Make sure the first parents name is none
        return links



class URDFLink():
    def __init__(self, name, parent_name, recur, 
            link_shape=0, link_length=0.1, link_radius=1, link_mass=1, joint_mass=1, 
            joint_type=1, joint_axis_xyz=1, joint_origin_rpy_1=1, joint_origin_rpy_2=1,
            joint_origin_rpy_3=1, joint_origin_xyz_1=1,joint_origin_xyz_2=1, 
            joint_origin_xyz_3=1, control_waveform=1, control_amp=1, control_freq=0.1):

        self.name = name
        self.parent_name = parent_name
        self.recur = recur
        self.link_shape = link_shape
        self.link_length = link_length
        self.link_radius = link_radius
        self.link_mass = link_mass
        self.joint_mass = joint_mass
        self.joint_type = joint_type
        self.joint_axis_xyz = joint_axis_xyz
        self.joint_origin_rpy_1 = joint_origin_rpy_1
        self.joint_origin_rpy_2 = joint_origin_rpy_2
        self.joint_origin_rpy_3 = joint_origin_rpy_3
        self.joint_origin_xyz_1 = joint_origin_xyz_1
        self.joint_origin_xyz_2 = joint_origin_xyz_2
        self.joint_origin_xyz_3 = joint_origin_xyz_3
        self.control_waveform = control_waveform
        self.control_amp = control_amp
        self.control_freq = control_freq

        self.sibling_ind = 1

    def to_link_element(self, adom):

        # Visual tags
        link_tag = adom.createElement("link")
        link_tag.setAttribute("name", self.name)
        vis_tag = adom.createElement("visual")
        geom_tag = adom.createElement("geometry")
        cyl_tag = adom.createElement("cylinder")
        cyl_tag.setAttribute("length", str(self.link_length))
        cyl_tag.setAttribute("radius", str(self.link_radius))

        geom_tag.appendChild(cyl_tag)
        vis_tag.appendChild(geom_tag)

        # Collisison tags
        col_tag = adom.createElement("collision")

        col_geom_tag = adom.createElement("geometry")
        col_cyl_tag = adom.createElement("cylinder")
        col_cyl_tag.setAttribute("length", str(self.link_length))
        col_cyl_tag.setAttribute("radius", str(self.link_radius))
        
        col_geom_tag.appendChild(col_cyl_tag)
        col_tag.appendChild(col_geom_tag) # collision will have the sam geometry
        
        inertial_tag = adom.createElement("inertial")
        mass_tag = adom.createElement("mass")
        mass_tag.setAttribute("value", str(self.link_mass))
        inertia_tag = adom.createElement("inertia")
        # TODO: Check if these need to be changed
        inertia_tag.setAttribute("ixx", "0.0003")
        inertia_tag.setAttribute("iyy", "0.0003")
        inertia_tag.setAttribute("izz", "0.0003")
        
        inertial_tag.appendChild(mass_tag)
        inertial_tag.appendChild(inertia_tag)

        link_tag.appendChild(vis_tag)
        link_tag.appendChild(col_tag)
        link_tag.appendChild(inertial_tag)

        return link_tag

    def to_joint_element(self, adom):
        joint_tag = adom.createElement('joint')
        joint_tag.setAttribute('name', str(self.parent_name) + "_to_" + str(self.name))
        if self.link_shape >= 0.5:
            joint_tag.setAttribute('type', 'revolute')
        else: 
            joint_tag.setAttribute('type', 'fixed')

        # Parent and child
        parent_tag = adom.createElement('parent')
        parent_tag.setAttribute('link', str(self.parent_name))
        child_tag = adom.createElement('child')
        child_tag.setAttribute('link', self.name)

        # Axis
        axis_tag = adom.createElement('axis')
        axis_tag.setAttribute('xyz', '1 0 0')

        # Limit
        limit_tag = adom.createElement('limit')
        limit_tag.setAttribute('effort', '1')
        limit_tag.setAttribute('velocity', '1')

        # Origin
        rpy1 = self.joint_origin_rpy_1 * self.sibling_ind
        origin_tag = adom.createElement('origin')
        rpy = str(rpy1) + " " + str(self.joint_origin_rpy_2) + " " + str(self.joint_origin_rpy_3)
        origin_tag.setAttribute('rpy', rpy)
        xyz = str(self.joint_origin_xyz_1) + " " + str(self.joint_origin_xyz_2) + " " + str(self.joint_origin_xyz_3)
        origin_tag.setAttribute('xyz', xyz)


        joint_tag.appendChild(parent_tag)
        joint_tag.appendChild(child_tag)
        joint_tag.appendChild(axis_tag)
        joint_tag.appendChild(limit_tag)
        joint_tag.appendChild(origin_tag)

        return joint_tag
