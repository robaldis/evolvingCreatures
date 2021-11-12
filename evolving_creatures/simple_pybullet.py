import pybullet as p

p.connect(p.GUI)

floor_shape = p.createCollisionShape(p.GEOM_PLANE)

floor = p.createMultiBody(floor_shape, floor_shape)

box_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[1,1,1])
p.setGravity(0,0,-10)

p.setRealTimeSimulation(1)


