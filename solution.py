import numpy
import pyrosim.pyrosim as pyrosim
import os
import random
import time

class SOLUTION:
    def __init__(self, id) -> None:
        self.myID = id

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
        # pyrosim.Send_Cube(name="Box", pos=[0.5+10, 0+10, 0.5], size=[1, 1, 1])
        pyrosim.End()

    def Generate_Body(self):
        self.numLinks = random.randint(1, 9)
        # numLinks + 1 = Total number of Link
        # numLinks = number of joints
        self.numSensors = random.randint(1, self.numLinks+1)
        linkList = range(self.numLinks+1)
        self.sensorList = random.sample(linkList, self.numSensors)
        pyrosim.Start_URDF("body.urdf")
        if 0 in self.sensorList:
            pyrosim.Send_Cube(name="Start", pos=[0,0,0], size=[1, 1, 1], color='Green')
        else:
            pyrosim.Send_Cube(name="Start", pos=[0,0,0], size=[1, 1, 1], color= "Blue")
        pyrosim.Send_Joint(name = "Start_Link0", parent="Start", child="Link0", type="revolute", position=[0.5, 0, 0], jointAxis= "1 0 0")
        for i in range(self.numLinks):
            x_l = random.uniform(0.2, 2)
            y_l = random.uniform(0.2, 2)
            z_l = random.uniform(0.2, 2)
            pname = "Link"+str(i)
            if i+1 in self.sensorList:
                pyrosim.Send_Cube(name = pname, pos = [x_l/2,0,0], size = [x_l, y_l, z_l], color= "Green")
            else:
                pyrosim.Send_Cube(pname, pos = [x_l/2,0,0], size = [x_l, y_l, z_l], color="Blue")
            if i < self.numLinks -1:
                cname = "Link"+str(i+1)
                pyrosim.Send_Joint(name = pname+"_"+cname, parent= pname, child = cname, type="revolute", position=[x_l, 0, 0], jointAxis= "1 0 0")
        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain"+str(self.myID)+".nndf")
        name = 0
        for i in self.sensorList:
            if i == 0:
                pyrosim.Send_Sensor_Neuron(name = name, linkName= "Start")
                name =  name + 1
            else:
                pyrosim.Send_Sensor_Neuron(name = name, linkName= "Link"+str(i-1))
                name =  name + 1
        pyrosim.Send_Motor_Neuron(name=self.numSensors, jointName="Start_Link0")
        for i in range(self.numSensors+1, self.numSensors+self.numLinks):
            pyrosim.Send_Motor_Neuron(name=i, jointName="Link"+str(i-self.numSensors-1)+"_Link"+str(i-self.numSensors))
        self.weights = numpy.random.rand(self.numSensors, self.numLinks)
        self.weights = self.weights * 2 - 1
        for currentRow in range(self.numSensors):
            for currentColumn in range(self.numLinks):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn+ self.numSensors, weight = self.weights[currentRow][currentColumn] )
        pyrosim.End()

    def Mutate(self):
        if self.numSensors > 0:
            randomRow = random.randint(0, self.numSensors - 1)
        randomColumn = random.randint(0, self.numLinks - 1)
        self.weights[randomRow,randomColumn] = random.random() * 2 - 1
