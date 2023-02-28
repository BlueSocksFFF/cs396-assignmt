from sensor import SENSOR
from motor import MOTOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c

class ROBOT:
    def __init__(self, solutionID):
        self.solutionID = solutionID
        self.fell_on_ground = False
        self.robotId = p.loadURDF("body"+str(self.solutionID)+".urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.nn = NEURAL_NETWORK("brain"+str(self.solutionID)+".nndf")
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        os.system("del brain"+str(self.solutionID)+".nndf")
        os.system("del body"+str(self.solutionID)+".urdf")

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, t):
        for sensor in self.sensors.values():
            sensor.Get_Value(t)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            # print(jointName)
            self.motors[jointName] = MOTOR(jointName)

    def Act(self):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                if jointName.encode('UTF-8') not in self.motors.keys():
                    print(self.nn.Get_Neuron_Names())
                    print(self.motors)
                    print(jointName)
                self.motors[jointName.encode('UTF-8')].Set_Value(self.robotId, desiredAngle)

    def Save_Values(self):
        for sensor in self.sensors.values():
            sensor.Save_Values()
        for motor in self.motors.values():
            motor.Save_Values()

    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        # yPosition = basePosition[1]
        # zPosition = basePosition[2]
        f = open("tmp"+str(self.solutionID)+".txt","w")
        f.write(str(xPosition))
        f.close()
        os.rename("tmp"+str(self.solutionID)+".txt", "fitness"+str(self.solutionID)+".txt")
