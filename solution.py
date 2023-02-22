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
        # Indices
        self.numLinks = random.randint(1, 10)
        self.numSensors = random.randint(1, self.numLinks)
        print(self.numLinks)
        linkList = range(self.numLinks)
        self.sensorList = random.sample(linkList, self.numSensors)
        link_names = []
        self.joint_names = []
        direc_avail = ['xp','xm','yp','ym','zp','zm']
        # xplus, xminus, yplus, yminus, zplus, zminus
        dict_linkname_direc_avail = {}
        dict_linkname_size = {}
        dict_link_jointloc_buffer = {}
        pyrosim.Start_URDF("body.urdf")
        if 0 in self.sensorList:
            pyrosim.Send_Cube(name="Start", pos=[0,0,0], size=[1, 1, 1], color='Green')
        else:
            pyrosim.Send_Cube(name="Start", pos=[0,0,0], size=[1, 1, 1], color= "Blue")
        link_names.append("Start")
        dict_linkname_direc_avail.update({"Start":direc_avail.copy()})
        dict_linkname_size.update({"Start":[1,1,1]})
        dict_link_jointloc_buffer.update({"Start":[0,0,0]})
        for i in range(self.numLinks-1):
            x_l = random.uniform(0.2, 2)
            y_l = random.uniform(0.2, 2)
            z_l = random.uniform(0.2, 2)
            name_link_attached = random.choice(link_names)
            pj = dict_link_jointloc_buffer.get(name_link_attached)
            direcs_a = dict_linkname_direc_avail.get(name_link_attached)
            while(direcs_a == []):
                link_names.remove(name_link_attached)
                name_link_attached = random.choice(link_names)
                direcs_a = dict_linkname_direc_avail.get(name_link_attached)
            direc = random.choice(direcs_a)
            direcs_a.remove(direc)
            dict_linkname_direc_avail.update({name_link_attached:direcs_a})
            x, y, z = dict_linkname_size.get(name_link_attached)
            linkname = "Link"+str(i)
            link_names.append(linkname)
            joint_po = pj.copy()
            dcopy = direc_avail.copy()
            print(name_link_attached, direc, linkname)
            match direc:
                case 'xp':
                    joint_po[0] = pj[0]+x/2
                    p = [x_l/2, 0, 0]
                    pj = [x_l/2, 0, 0]
                    a = "1 0 0"
                    dcopy.remove('xm')
                case 'xm':
                    joint_po[0] = pj[0]-x/2
                    p = [-x_l/2, 0, 0]
                    pj = [-x_l/2, 0, 0]
                    a = "1 0 0"
                    dcopy.remove('xp')
                case 'yp':
                    joint_po[1] = pj[1]+y/2
                    p = [0, y_l/2, 0,]
                    pj = [0, y_l/2, 0]
                    a = "0 1 0"
                    dcopy.remove('ym')
                case 'ym':
                    joint_po[1] = pj[1]-y/2
                    p = [0, -y_l/2, 0,]
                    pj = [0, -y_l/2, 0]
                    a = "0 1 0"
                    dcopy.remove('yp')
                case 'zp':
                    joint_po[2] = pj[2]+z/2
                    p = [0, 0, z_l/2]
                    pj = [0, 0, z_l/2]
                    a = "0 0 1"
                    dcopy.remove('zm')
                case 'zm':
                    joint_po[2] = pj[2]-z/2
                    p = [0, 0, -z_l/2]
                    pj = [0, 0, -z_l/2]
                    a = "0 0 1"
                    dcopy.remove('zp')
            if i+1 in self.sensorList:
                c = 'Green'
            else:
                c = 'Blue'
            jname = name_link_attached+"_"+linkname
            self.joint_names.append(jname)
            pyrosim.Send_Joint(name = jname, parent= name_link_attached, child = linkname, type="revolute", position=joint_po, jointAxis= a)
            pyrosim.Send_Cube(name = linkname, pos = p, size = [x_l, y_l, z_l], color= c)            
            dict_linkname_direc_avail.update({linkname:direc_avail.copy()})
            dict_linkname_size.update({linkname:[x_l, y_l, z_l]})
            dict_link_jointloc_buffer.update({linkname:pj})
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
        for i in range(self.numSensors+1, self.numSensors+self.numLinks):
            pyrosim.Send_Motor_Neuron(name=i, jointName=self.joint_names[i-self.numSensors-1])
        self.weights = numpy.random.rand(self.numSensors, self.numLinks-1)
        self.weights = self.weights * 2 - 1
        for currentRow in range(self.numSensors):
            for currentColumn in range(self.numLinks-1):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn+ self.numSensors, weight = self.weights[currentRow][currentColumn] )
        pyrosim.End()

    def Mutate(self):
        if self.numSensors > 0:
            randomRow = random.randint(0, self.numSensors - 1)
        randomColumn = random.randint(0, self.numLinks - 2)
        self.weights[randomRow,randomColumn] = random.random() * 2 - 1
