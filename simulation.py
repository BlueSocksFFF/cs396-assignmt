from world import WORLD
from robot import ROBOT
import time
import constants as c
import pybullet as p

class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        self.directOrGUI = directOrGUI
        self.world = WORLD(directOrGUI)
        self.robot = ROBOT(solutionID)

    def Run(self):
        for i in range(c.steps_num):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act()
            if self.directOrGUI == 'GUI':
                time.sleep(1/120)
            # print(i)
        self.Get_Fitness()

    def Get_Fitness(self):
        self.robot.Get_Fitness()

    def __del__(self):
        p.disconnect()
        