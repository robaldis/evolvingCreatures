from creature.creature import Creature as c
import pybullet as p
from multiprocessing import Pool


class Simulation:
    def __init__(self, sim_id=0):
        self.physicsClientId = p.connect(p.DIRECT)
        print(self.physicsClientId)
        self.sim_id = sim_id

    def run_creature(self, cr, iterations = 24000):
        p.resetSimulation(physicsClientId=self.physicsClientId)
        p.setPhysicsEngineParameter(enableFileCaching=0, physicsClientId=self.physicsClientId)
                
        p.setGravity(0,0,-10, physicsClientId=self.physicsClientId)
        floor_shape = p.createCollisionShape(p.GEOM_PLANE, physicsClientId=self.physicsClientId)
        floor = p.createMultiBody(floor_shape, floor_shape, physicsClientId=self.physicsClientId)

        with open("URDF/" + str(self.sim_id) + ".urdf", "w") as f:
            f.write(cr.to_xml())
            f.close()
        cid = p.loadURDF('URDF/' + str(self.sim_id) + ".urdf", physicsClientId=self.physicsClientId)

        # Reset the cid posistion to be up in the air to drop from a height
        p.resetBasePositionAndOrientation(cid, [0, 0, 2.5], [0, 0, 0, 1], physicsClientId=self.physicsClientId)


        for itter in range(iterations):
            p.stepSimulation(physicsClientId=self.physicsClientId)
            if itter % 24 == 0:
                try:
                    for jid in range(p.getNumJoints(cid, physicsClientId=self.physicsClientId)):
                        m = cr.get_motors()[jid]
                        p.setJointMotorControl2(cid,
                                jid,
                                controlMode=p.VELOCITY_CONTROL,
                                targetVelocity=m.get_output(), 
                                force = 5, physicsClientId=self.physicsClientId)
                except IndexError:
                    print(len(cr.get_motors()))
                    print(p.getNumJoints(cid, physicsClientId=self.physicsClientId))
                    print(cr.to_xml())
                    quit()

                # TODO: this keeps erroring out
                # Try it out without multi-threading and see if it errors the same 
                # way
                try:
                    pos,_ = p.getBasePositionAndOrientation(cid, physicsClientId=self.physicsClientId)
                    cr.update_position(pos)    
                except p.error:
                    print(cid, self.physicsClientId)
                

        dist = cr.get_distance_travled()
        return dist


class ThreadedSim():
    def __init__(self, pool_size=4):
        self.sims = [Simulation(i) for i in range(pool_size)]

    @staticmethod
    def static_run_creature(sim, cr, iterations):
        sim.run_creature(cr, iterations)
        return cr


    def eval_population(self, pop, iterations):
        pool_args = []
        start_ind = 0
        pool_size = len(self.sims)
        while start_ind < len(pop.creatures):
            this_pool_args = []
            for i in range( start_ind, start_ind + pool_size):
                if i == len(pop.creatures): # the end
                    break
                # work out the sim ind
                sim_ind = i % len(self.sims)
                this_pool_args.append([self.sims[sim_ind],
                    pop.creatures[i],
                    iterations])

            pool_args.append(this_pool_args)
            start_ind = start_ind + pool_size
            
        # print(len(pool_args[0]))
        new_creatures = []
        for pool_argset in pool_args:
            with Pool(pool_size) as p:
                creatures = p.starmap(ThreadedSim.static_run_creature, pool_argset)
                new_creatures.extend(creatures)

        pop.creatures = new_creatures

class SingleSim():
    def __init__(self):
        self.sim = Simulation()

    @staticmethod
    def static_run_creature(sim, cr, iterations):
        sim.run_creature(cr, iterations)
        return cr
