from creature import creature
import time
import pybullet as p
import numpy as np
from creature import genome



p.connect(p.GUI)
floor_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(floor_shape, floor_shape)
p.setGravity(0,0,-10)


c = creature.Creature(gene_count = 10)
dna = genome.Genome.from_csv('csv/19_elite.csv')
print(dna)
c.set_dna(dna)

with open('URDF/test.urdf' ,'w') as f:
    f.write(c.to_xml())
    f.close()

cid = p.loadURDF('URDF/test.urdf')

p.resetBasePositionAndOrientation(cid, [0,0, 2.5], [0,0,0,1])
p.setRealTimeSimulation(1)

count = 0

# Get the start position of the creature
start_pos, ori = p.getBasePositionAndOrientation(cid)
print(start_pos) # start pos = (0, 0, 0)

while True:

    motors = c.get_motors()                                                                                                                                                                                 
    assert len(motors) == p.getNumJoints(cid), "Something went wrong"                                                                                                                                       
    for jid in range(p.getNumJoints(cid)):                                                                                                                                                                  
        mode = p.VELOCITY_CONTROL                                                                                                                                                                            
        vel = motors[jid].get_output()                                                                                                                                                                       
        print(vel)
        p.setJointMotorControl2(cid,                                                                                                                                                                        
                        jid,                                                                                                                                                                                 
                        controlMode=mode,                                                                                                                                                                    
                        targetVelocity=vel)



    if count >= 200:
        end_pos, ori = p.getBasePositionAndOrientation(cid)
        break
    count += 1
    time.sleep(0.1)


distance = np.linalg.norm(np.asarray(start_pos) - np.asarray(end_pos))
print(f"Distance travled: {distance}")



