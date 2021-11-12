from creature import creature
import time
import pybullet as p



p.connect(p.GUI)
floor_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(floor_shape, floor_shape)
p.setGravity(0,0,-10)


c = creature.Creature(gene_count = 5)

c.to_urdf(name = 'test')

cid = p.loadURDF('test.urdf')


p.setRealTimeSimulation(1)


while True:
    for jid in range(p.getNumJoints(cid)):
        m = c.get_motors()[jid]
        p.setJointMotorControl2(cid,
                jid,
                controlMode=p.VELOCITY_CONTROL,
                targetVelocity=m.get_output(), 
                force = 5)

    time.sleep(0.1)

