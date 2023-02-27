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
    
    def start_simulation_after_mutation(self, strl):
        self.Create_World()
        self.generate_body_after_mutation()
        self.generate_brain_after_mutation()
        os.system('start /B python simulate.py '+ strl + ' ' + str(self.myID))

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
        print(self.fitness)
        f.close()
        os.system("del fitness"+str(self.myID)+".txt")

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        # pyrosim.Send_Cube(name="Box", pos=[0.5+10, 0+10, 0.5], size=[1, 1, 1])
        pyrosim.End()

    def Generate_Body(self):
        # Indices
        self.links = {}
        self.joints = {}
        self.numLinks = random.randint(1, 10)
        self.numSensors = random.randint(1, self.numLinks)
        print(self.numLinks)
        linkList = range(self.numLinks)
        self.sensorList = random.sample(linkList, self.numSensors)
        self.link_names = []
        self.joint_names = []
        direc_avail = ['xp','xm','yp','ym','zp','zm']
        # xplus, xminus, yplus, yminus, zplus, zminus
        self.dict_linkname_direc_avail = {}
        self.dict_linkname_size = {}
        self.dict_link_jointloc_buffer = {}
        pyrosim.Start_URDF("body"+str(self.myID)+".urdf")
        if 0 in self.sensorList:
            pyrosim.Send_Cube(name="Start", pos=[0,0,0], size=[1, 1, 1], color='Green')
            self.links.update({0:{'name':'Start', 'pos':[0,0,0], 'size':[1,1,1], 'color':'Green'}})
        else:
            pyrosim.Send_Cube(name="Start", pos=[0,0,0], size=[1, 1, 1], color= "Blue")
            self.links.update({0:{'name':'Start', 'pos':[0,0,0], 'size':[1,1,1], 'color':'Blue'}})
        self.link_names.append("Start")
        self.dict_linkname_direc_avail.update({"Start":direc_avail.copy()})
        self.dict_linkname_size.update({"Start":[1,1,1]})
        self.dict_link_jointloc_buffer.update({"Start":[0,0,0]})
        for i in range(self.numLinks-1):
            x_l = random.uniform(0.2, 2)
            y_l = random.uniform(0.2, 2)
            z_l = random.uniform(0.2, 2)
            name_link_attached = random.choice(self.link_names)
            pj = self.dict_link_jointloc_buffer.get(name_link_attached)
            direcs_a = self.dict_linkname_direc_avail.get(name_link_attached)
            while(direcs_a == []):
                self.link_names.remove(name_link_attached)
                name_link_attached = random.choice(self.link_names)
                direcs_a = self.dict_linkname_direc_avail.get(name_link_attached)
            direc = random.choice(direcs_a)
            direcs_a.remove(direc)
            self.dict_linkname_direc_avail.update({name_link_attached:direcs_a})
            x, y, z = self.dict_linkname_size.get(name_link_attached)
            linkname = "Link"+str(i)
            self.link_names.append(linkname)
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
            self.joints.update({i:{'name':jname, 'parent':name_link_attached, 'child':linkname, 'type':"revolute", 'position':joint_po, 'jointAxis':a}})
            pyrosim.Send_Cube(name = linkname, pos = p, size = [x_l, y_l, z_l], color= c) 
            self.links.update({i+1:{'name':linkname, 'pos':p, 'size':[x_l, y_l, z_l], 'color':c}})     
            self.dict_linkname_direc_avail.update({linkname:dcopy})
            self.dict_linkname_size.update({linkname:[x_l, y_l, z_l]})
            self.dict_link_jointloc_buffer.update({linkname:pj})
        pyrosim.End()

    def generate_body_after_mutation(self):
        pyrosim.Start_URDF("body"+str(self.myID)+".urdf")
        for i in range(self.numLinks):
            link_dict = self.links[i]
            pyrosim.Send_Cube(name=link_dict['name'], pos=link_dict['pos'], size=link_dict['size'], color=link_dict['color'])
            if i < self.numLinks-1:
                joint_dict = self.joints[i]
                pyrosim.Send_Joint(name=joint_dict['name'], parent=joint_dict['parent'], child=joint_dict['child'], type=joint_dict['type'], position=joint_dict['position'], jointAxis=joint_dict['jointAxis'])
        pyrosim.End()

    def generate_brain_after_mutation(self):
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
        for currentRow in range(self.numSensors):
            for currentColumn in range(self.numLinks-1):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn+ self.numSensors, weight = self.weights[currentRow][currentColumn] )
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
        mutation_method = random.choice(['weights','AddSensor','DeleteSensor','AddLink','DeleteLink','ChangeSize'])
        match mutation_method:
            case 'weights':
                if self.numSensors > 0:
                    randomRow = random.randint(0, self.numSensors - 1)
                randomColumn = random.randint(0, self.numLinks - 2)
                self.weights[randomRow,randomColumn] = random.random() * 2 - 1
            case 'AddSensor':
                if self.numSensors == self.numLinks:
                    self.Mutate()
                elif self.numSensors < self.numLinks:
                    availlinks = []
                    for i in range(self.numLinks):
                        if i not in self.sensorList:
                            availlinks.append(i)
                    link = random.choice(availlinks)
                    self.numSensors += 1
                    self.sensorList.append(link)
                else:
                    print('Error: number of sensors cannot be greater than number of links')
                    return
            case 'DeleteSensor':
                if self.numSensors == 0:
                    self.Mutate()
                elif self.numSensors < 0:
                    print('Error: number of sensors cannot be less than 0')
                    return
                else:
                    self.numSensors -= 1
                    link = random.choice(self.sensorList)
                    self.sensorList.remove(link)
            case 'AddLink':
                x_l = random.uniform(0.2, 2)
                y_l = random.uniform(0.2, 2)
                z_l = random.uniform(0.2, 2)
                name_link_attached = random.choice(self.link_names)
                pj = self.dict_link_jointloc_buffer.get(name_link_attached)
                direcs_a = self.dict_linkname_direc_avail.get(name_link_attached)
                while(direcs_a == []):
                    self.link_names.remove(name_link_attached)
                    name_link_attached = random.choice(self.link_names)
                    direcs_a = self.dict_linkname_direc_avail.get(name_link_attached)
                direc = random.choice(direcs_a)
                direcs_a.remove(direc)
                self.dict_linkname_direc_avail.update({name_link_attached:direcs_a})
                x, y, z = self.dict_linkname_size.get(name_link_attached)
                linkname = "Link"+str(i)
                self.link_names.append(linkname)
                joint_po = pj.copy()
                dcopy = self.direc_avail.copy()
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
                self.joints.update({i:{'name':jname, 'parent':name_link_attached, 'child':linkname, 'type':"revolute", 'position':joint_po, 'jointAxis':a}})
                pyrosim.Send_Cube(name = linkname, pos = p, size = [x_l, y_l, z_l], color= c) 
                self.links.update({i+1:{'name':linkname, 'pos':p, 'size':[x_l, y_l, z_l], 'color':c}})           
                self.dict_linkname_direc_avail.update({linkname:dcopy})
                self.dict_linkname_size.update({linkname:[x_l, y_l, z_l]})
                self.dict_link_jointloc_buffer.update({linkname:pj})
                self.numLinks += 1
            case 'DeleteLink':
                availlinks = []
                for linkname in self.dict_linkname_direc_avail.keys():
                    direcs = self.dict_linkname_direc_avail.get(linkname)
                    if len(direcs) > 4:
                        availlinks.append((linkname, self.link_names.index(linkname)))
                if len(availlinks) == 0:
                    print('Error: Cyclic links or Bug')
                    return
                else:
                    linkname, linkindex = random.choice(availlinks)
                    self.links.pop(linkindex)
                    self.dict_linkname_direc_avail.pop(linkname)
                    self.dict_linkname_size(linkname)
                    self.numLinks -= 1
            case 'ChangeSize':
                linkindex = random.choice(range(self.numLinks))
                link_dict = self.links.get(linkindex)
                size = link_dict.get('size')
                ax = random.choice(range(3))
                size[ax] = random.uniform(0.2, 2)
                link_dict.update({'size':size})
                self.links.update({linkindex:link_dict})