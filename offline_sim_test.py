from creature import creature
import time
import pybullet as p
import numpy as np



p.connect(p.DIRECT)
floor_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(floor_shape, floor_shape)
p.setGravity(0,0,-10)


c = creature.Creature(gene_count = 5)

with open("URDF/" + "test" + ".urdf", "w") as f:
    f.write(c.to_xml())
    f.close()

cid = p.loadURDF('URDF/test.urdf')


# Get the start position of the creature
start_pos, ori = p.getBasePositionAndOrientation(cid)
end_pos = []
print(start_pos) # start pos = (0, 0, 0)

total_frames = 2400 # at 240Hz, that's 10 seconds
for frame in range(total_frames):
    p.stepSimulation()
    if frame % 24 == 0:
        for jid in range(p.getNumJoints(cid)):
            m = c.get_motors()[jid]
            p.setJointMotorControl2(cid,
                    jid,
                    controlMode=p.VELOCITY_CONTROL,
                    targetVelocity=m.get_output(), 
                    force = 5)
        cur_pos, ori = p.getBasePositionAndOrientation(cid)
        # print(cur_pos)

    end_pos, ori = p.getBasePositionAndOrientation(cid)


distance = np.linalg.norm(np.asarray(start_pos) - np.asarray(end_pos))
print(f"Distance travled: {distance}")



