
import pybullet as p
import time

def setupSim():
# Setup the GUI
    pysicsClient = p.connect(p.GUI)
    p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)

# Gravity
    p.setGravity(0,0,-10)

# Doesn't cache the URDF file so can be updated when run again in ipython
    p.setPhysicsEngineParameter(enableFileCaching=0)

# Floor
    floor_shape = p.createCollisionShape(p.GEOM_PLANE)
    floor = p.createMultiBody(floor_shape, floor_shape)

    return pysicsClient

def box():
# BOX
    """
    box_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[1,1,1])
    box_body = p.createMultiBody(box_shape, box_shape)
    return box
    """

def myRobot():
# Robot 1
    rob1 = p.loadURDF('../first.urdf')
    p.setJointMotorControl2(rob1, 0, controlMode=p.VELOCITY_CONTROL, targetVelocity=1)
    p.resetBasePositionAndOrientation(rob1, [0,3,1], [0,0,0,1])
    return rob1

def robot1 ():
# Online Robot
    robot = p.loadURDF('URDF/twoLeggedRobot.urdf')
    mode = p.VELOCITY_CONTROL

    for jid in range(p.getNumJoints(robot)):
        p.setJointMotorControl2(robot, jid, 
                controlMode=mode, targetVelocity=1)

    p.resetBasePositionAndOrientation(robot, [0,0,1], [0,0,0,1])
    return robot

def robot2():
    bot1 = p.loadURDF('URDF/bot2.urdf')
    p.resetBasePositionAndOrientation(bot1, [0, 0, 1], [0, 0, 0, 1])
    vel = 10

    for i in range(p.getNumJoints(bot1)):
        p.setJointMotorControl2(bot1, i, controlMode=p.VELOCITY_CONTROL, targetVelocity=vel)

    p.resetBasePositionAndOrientation(bot1, [0,-3,1], [0,0,6,1])
    return bot1

def reset(robots):
    p.resetBasePositionAndOrientation(robots[0], [0,3,1], [0,0,0,1])
    p.resetBasePositionAndOrientation(robots[1], [0,0,1], [0,0,0,1])
    p.resetBasePositionAndOrientation(robots[2], [0,-3,1], [0,0,6,1])

def get_key_pressed():
    pressed_keys = []
    events  = p.getKeyboardEvents()
    key_codes = events.keys()
    for key in key_codes:
        pressed_keys.append(key)
    return pressed_keys


def main():
    pysicsClient = setupSim()

    robots = []
    robots.append( myRobot())
    robots.append( robot1())
    robots.append( robot2())


    for i in range(10000):
        pressed_keys = get_key_pressed()
        if 114 in pressed_keys:
            reset(robots)
        p.stepSimulation()
        time.sleep(1./240.)

    p.disconnect()


if __name__ == "__main__":
    main()
