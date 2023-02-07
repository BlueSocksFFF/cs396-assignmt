import numpy
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, id) -> None:
        self.myID = id
        self.weights = numpy.random.rand(c.numSensorNeurons, c.numMotorNeurons)
        self.weights = self.weights * 2 - 1

    def Set_ID(self, id):
        self.myID = id
    
    def Evaluate(self, strl):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system('start /B python simulate.py '+ strl + ' ' + str(self.myID))
        while not os.path.exists("fitness"+str(self.myID)+".txt"):
            time.sleep(0.01)
        f = open("fitness"+str(self.myID)+".txt","r")
        lines = f.readlines()
        self.fitness = float(lines[0])
        str_bool = lines[1]
        if str_bool == 'True':
            self.fell_on_ground = True
        elif str_bool == 'False':

            self.fell_on_ground = False
        else:
            raise ValueError("Can not convert to boolean")
        print(self.fitness, self.fell_on_ground)
        f.close()

    def Start_Simulation(self, strl):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system('start /B python simulate.py '+ strl + ' ' + str(self.myID))

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness"+str(self.myID)+".txt"):
            time.sleep(0.01)
        f = open("fitness"+str(self.myID)+".txt","r")
        lines = f.readlines()
        self.fitness = float(lines[0])
        str_bool = lines[1]
        if str_bool == 'True':
            self.fell_on_ground = True
        elif str_bool == 'False':
            self.fell_on_ground = False
        else:
            raise ValueError("Can not convert to boolean")
        print(self.fitness, self.fell_on_ground)
        f.close()
        os.system("del fitness"+str(self.myID)+".txt")

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[0.5+10, 0+10, 0.5], size=[1, 1, 1])
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0,0,6], size=[4, 1, 1])
        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type= "revolute", position=[-2,0,6], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[0,0,-3], size=[1, 1, 6])
        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type= "revolute", position=[2,0,6], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0,0,-3], size=[1, 1, 6])
        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain"+str(self.myID)+".nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "LeftLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "RightLeg")
        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_RightLeg")
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn+ c.numSensorNeurons, weight = self.weights[currentRow][currentColumn] )
        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons - 1)
        randomColumn = random.randint(0, c.numMotorNeurons - 1)
        self.weights[randomRow,randomColumn] = random.random() * 2 - 1
