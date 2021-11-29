from creature import creature
import time
import pybullet as p
import numpy as np



p.connect(p.GUI)
floor_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(floor_shape, floor_shape)
p.setGravity(0,0,-10)


c = creature.Creature(gene_count = 5)

with open('test', 'w') as f:
    f.write(c.to_xml())
    f.close()

cid = p.loadURDF('URDF/0.urdf')


p.setRealTimeSimulation(1)

count = 0

# Get the start position of the creature
start_pos, ori = p.getBasePositionAndOrientation(cid)
print(start_pos) # start pos = (0, 0, 0)

while True:
    for jid in range(p.getNumJoints(cid)):
        m = c.get_motors()[jid]
        p.setJointMotorControl2(cid,
                jid,
                controlMode=p.VELOCITY_CONTROL,
                targetVelocity=m.get_output(), 
                force = 5)

    if count >= 200:
        end_pos, ori = p.getBasePositionAndOrientation(cid)
        break
    count += 1
    time.sleep(0.1)


distance = np.linalg.norm(np.asarray(start_pos) - np.asarray(end_pos))
print(f"Distance travled: {distance}")



