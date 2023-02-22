import pybullet_data
import pybullet as p

class WORLD:
    def __init__(self, directOrGUI) -> None:
        if directOrGUI == 'DIRECT':
            self.physicsClient = p.connect(p.DIRECT)
        elif directOrGUI == 'GUI':
            self.physicsClient = p.connect(p.GUI)
            p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        else:
            print('Error: Wrong input. Please write DIRECT or GUI')
            exit()
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        p.loadSDF("world.sdf")
        self.planeId = p.loadURDF("plane.urdf")
    