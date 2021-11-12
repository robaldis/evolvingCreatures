from creature import genome
from xml.dom.minidom import getDOMImplementation
from enum import Enum
import numpy as np

class MotorType(Enum):
    PULSE = 1
    SINE = 2

class Motor():
    def __init__(self, control_waveform, control_amp, control_freq):
        if control_waveform <= 0.5:
            self.motor_type = MotorType.PULSE
        else:
             self.motor_type = MotorType.SINE
        self.amp = control_amp
        self.freq = control_freq
        self.phase = 0

    def get_output(self):
        self.phase = (self.phase + self.freq) % (np.pi * 2)

        if self.motor_type == MotorType.PULSE:
            if self.phase < np.pi:
                output = 1
            else:
                output = -1
        else :
            output = np.sin(self.phase)

        return output


class Creature():
    def __init__(self, gene_count):
        self.spec = genome.Genome.get_gene_spec()
        self.dna = genome.Genome.get_random_genome(len(self.spec), gene_count)
        self.falt_liknks = None
        self.exp_links = []

    def get_flat_links(self):
        gdict = genome.Genome.get_genome_dict(self.dna, self.spec)
        self.flat_links = genome.Genome.genome_to_links(gdict)
        return self.flat_links

    def get_expanded_links(self):
        self.get_flat_links()
        self.exp_links = [self.flat_links[0]]
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
        return robot_tag

    def to_urdf(self, name):
        robot_tag = self.to_xml()
        xml_text = '<?xml version="1.0"?>' + robot_tag.toprettyxml()
        with open(name + ".urdf", 'w+') as file:
            file.write(xml_text)
        

    def get_motors(self):
        motors = []
        for i in range(1, len(self.exp_links)):
            l = self.exp_links[i]
            M = Motor(l.control_waveform, l.control_amp, l.control_freq)
            motors.append(M)

        self.motors = motors
        return self.motors




