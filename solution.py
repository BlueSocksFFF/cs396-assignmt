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

    def best_simulation(self, strl):
        self.Create_World()
        self.generate_body_after_mutation()
        self.generate_brain_after_mutation()
        os.system('start /B python simulate.py '+ strl + ' ' + str(self.myID))
        os.rename("body"+str(self.myID)+".urdf", "bestbody.urdf")
        os.rename("brain"+str(self.myID)+".nndf", "bestbrain.nndf")
    
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
        while True:
            try:
                f = open("fitness"+str(self.myID)+".txt","r")
                break
            except:
                pass
        lines = f.readlines()
        self.fitness = float(lines[0])
        f.close()
        os.system("del fitness"+str(self.myID)+".txt")

    def Create_World(self):
        while not os.path.exists("world.sdf"):
            time.sleep(0.01)
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def Generate_Body(self):
        self.links = {}
        self.joints = {}
        self.numLinks = random.randint(2, 10)
        self.numSensors = random.randint(1, self.numLinks)
        linkList = range(self.numLinks)
        self.sensorList = random.sample(linkList, self.numSensors)
        self.link_names = []
        self.joint_names = []
        self.direc_avail = ['xp','xm','yp','ym','zp','zm']
        self.dict_linkname_direc_avail = {}
        self.dict_linkname_size = {}
        self.dict_link_jointloc_buffer = {}
        self.link_name_index = {}
        pyrosim.Start_URDF("body"+str(self.myID)+".urdf")
        if 0 in self.sensorList:
            pyrosim.Send_Cube(name="Start", pos=[0,0,0], size=[1, 1, 1], color='Green')
            self.links.update({0:{'name':'Start', 'pos':[0,0,0], 'size':[1,1,1], 'color':'Green'}})
            self.link_name_index.update({"Start":0})
        else:
            pyrosim.Send_Cube(name="Start", pos=[0,0,0], size=[1, 1, 1], color= "Blue")
            self.links.update({0:{'name':'Start', 'pos':[0,0,0], 'size':[1,1,1], 'color':'Blue'}})
            self.link_name_index.update({"Start":0})
        self.link_names.append("Start")
        self.dict_linkname_direc_avail.update({"Start":self.direc_avail.copy()})
        self.dict_linkname_size.update({"Start":[1,1,1]})
        self.dict_link_jointloc_buffer.update({"Start":[0,0,0]})
        self.link_joint_ind = {}
        for i in range(1, self.numLinks):
            x_l = random.uniform(0.2, 2)
            y_l = random.uniform(0.2, 2)
            z_l = random.uniform(0.2, 2)
            linkname = "Link"+str(i)
            avail_linknames_to_join = self.link_names.copy()
            name_link_attached = random.choice(avail_linknames_to_join)
            pj = self.dict_link_jointloc_buffer.get(name_link_attached)
            direcs_a = self.dict_linkname_direc_avail.get(name_link_attached)
            while(direcs_a == []):
                avail_linknames_to_join.remove(name_link_attached)
                name_link_attached = random.choice(avail_linknames_to_join)
                direcs_a = self.dict_linkname_direc_avail.get(name_link_attached)
            direc = random.choice(direcs_a)
            direcs_a.remove(direc)
            self.dict_linkname_direc_avail.update({name_link_attached:direcs_a})
            x, y, z = self.dict_linkname_size.get(name_link_attached)
            self.link_names.append(linkname)
            joint_po = pj.copy()
            dcopy = self.direc_avail.copy()
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
            if i in self.sensorList:
                c = 'Green'
            else:
                c = 'Blue'
            jname = name_link_attached+"_"+linkname
            self.joint_names.append(jname)
            pyrosim.Send_Cube(name = linkname, pos = p, size = [x_l, y_l, z_l], color= c)
            self.links.update({i:{'name':linkname, 'pos':p, 'size':[x_l, y_l, z_l], 'color':c}})     
            self.link_name_index.update({linkname:i})
            pyrosim.Send_Joint(name = jname, parent= name_link_attached, child = linkname, type="revolute", position=joint_po, jointAxis= a)
            self.joints.update({i-1:{'name':jname, 'parent':name_link_attached, 'child':linkname, 'type':"revolute", 'position':joint_po, 'jointAxis':a}})
            self.link_joint_ind.update({i-1:(self.link_name_index.get(name_link_attached), self.link_name_index.get(linkname))})
            self.dict_linkname_direc_avail.update({linkname:dcopy})
            self.dict_linkname_size.update({linkname:[x_l, y_l, z_l]})
            self.dict_link_jointloc_buffer.update({linkname:pj})
        pyrosim.End()

    def generate_body_after_mutation(self):
        pyrosim.Start_URDF("body"+str(self.myID)+".urdf")
        for i in self.links.keys():
            link_dict = self.links.get(i)
            pyrosim.Send_Cube(name=link_dict['name'], pos=link_dict['pos'], size=link_dict['size'], color=link_dict['color'])
        for i in self.joints.keys():
            joint_dict = self.joints[i]
            pyrosim.Send_Joint(name=joint_dict['name'], parent=joint_dict['parent'], child=joint_dict['child'], type=joint_dict['type'], position=joint_dict['position'], jointAxis=joint_dict['jointAxis'])
        pyrosim.End()

    def generate_brain_after_mutation(self):
        pyrosim.Start_NeuralNetwork("brain"+str(self.myID)+".nndf")
        name = 0
        joint_name = {}
        for i in self.sensorList:
            if i not in self.links.keys():
                print("Error when generating brain")
                print(self.sensorList)
                print(self.links.keys())
                exit()
            if i == 0:
                pyrosim.Send_Sensor_Neuron(name = name, linkName= "Start")
                name =  name + 1
            else:
                pyrosim.Send_Sensor_Neuron(name = name, linkName= "Link"+str(i))
                name =  name + 1
        for key in self.joints.keys():
            joint_dict = self.joints.get(key)
            pyrosim.Send_Motor_Neuron(name=name, jointName=joint_dict.get('name'))
            joint_name.update({key:name})
            name = name + 1
        for currentRow in self.sensorList:
            for currentColumn in self.joints.keys():
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = joint_name.get(currentColumn), weight = self.weights[currentRow][currentColumn] )
        pyrosim.End()
            

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain"+str(self.myID)+".nndf")
        name = 0
        for i in self.sensorList:
            if i == 0:
                pyrosim.Send_Sensor_Neuron(name = name, linkName= "Start")
                name =  name + 1
            else:
                pyrosim.Send_Sensor_Neuron(name = name, linkName= "Link"+str(i))
                name =  name + 1
        for i in range(self.numSensors, self.numSensors+self.numLinks-1):
            pyrosim.Send_Motor_Neuron(name=i, jointName=self.joint_names[i-self.numSensors])
        self.weights = numpy.random.rand(20, 20)
        self.weights = self.weights * 2 - 1
        for currentRow in range(self.numSensors):
            for currentColumn in range(self.numLinks-1):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn+ self.numSensors, weight = self.weights[currentRow][currentColumn] )
        pyrosim.End()

    def Mutate(self):
        avail_mutations = ['weights','AddSensor','DeleteSensor','AddLink','DeleteLink','ChangeSize']
        mutation_method = random.choice(avail_mutations)
        print(mutation_method)
        print(self.numLinks)
        print(self.links.keys())
        print(self.joints.keys())
        if len(self.sensorList) != self.numSensors:
            print("Error: number of sensors and sensor list does not match")
            print(self.sensorList)
            print(self.numSensors)
            exit()
        match mutation_method:
            case 'weights':
                if self.numSensors > 0:
                    randomRow = random.randint(0, self.numSensors - 1)
                randomColumn = random.randint(0, self.numLinks - 1)
                self.weights[randomRow,randomColumn] = random.random() * 2 - 1
            case 'AddSensor':
                if self.numSensors == self.numLinks:
                    self.Mutate()
                    return
                elif self.numSensors < self.numLinks:
                    availlinks = []
                    for i in self.links.keys():
                        if i not in self.sensorList:
                            availlinks.append(i)
                    link = random.choice(availlinks)
                    self.numSensors += 1
                    self.sensorList.append(link)
                else:
                    print('Error: number of sensors cannot be greater than number of links')
                    exit()
            case 'DeleteSensor':
                if self.numSensors == 1:
                    self.Mutate()
                    return
                elif self.numSensors < 0:
                    print('Error: number of sensors cannot be less than 0')
                    exit()
                else:
                    self.numSensors -= 1
                    link = random.choice(self.sensorList)
                    self.sensorList.remove(link)
                    link_dict = self.links.get(link).copy()
                    link_dict.update({'color':'Blue'})
                    self.links.update({link:link_dict})
            case 'AddLink':
                if self.numLinks > 9:
                    self.Mutate()
                    return
                i = list(self.links.keys())[-1]+1
                j = list(self.joints.keys())[-1]+1
                if (i-1)!=j:
                    print("Error: link and joint indices do not match")
                    exit()
                x_l = random.uniform(0.2, 2)
                y_l = random.uniform(0.2, 2)
                z_l = random.uniform(0.2, 2)
                linkname = "Link"+str(i)
                availLinknametoJoin = self.link_names.copy()
                name_link_attached = random.choice(availLinknametoJoin)
                pj = self.dict_link_jointloc_buffer.get(name_link_attached)
                direcs_a = self.dict_linkname_direc_avail.get(name_link_attached)
                while(len(direcs_a)==0):
                    availLinknametoJoin.remove(name_link_attached)
                    name_link_attached = random.choice(availLinknametoJoin)
                    direcs_a = self.dict_linkname_direc_avail.get(name_link_attached)
                direc = random.choice(direcs_a)
                direcs_a.remove(direc)
                self.dict_linkname_direc_avail.update({name_link_attached:direcs_a})
                x, y, z = self.dict_linkname_size.get(name_link_attached)
                self.link_names.append(linkname)
                joint_po = pj.copy()
                dcopy = self.direc_avail.copy()
                if name_link_attached == linkname:
                    print(self.links)
                    print(self.joints)
                    print("Error: in adding a link")
                    exit()
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
                if random.random()<0.5:
                    self.sensorList.append(i)
                    self.numSensors += 1
                    c = 'Green'
                else:
                    c = 'Blue'
                jname = name_link_attached+"_"+linkname
                self.joint_names.append(jname)
                self.links.update({i:{'name':linkname, 'pos':p, 'size':[x_l, y_l, z_l], 'color':c}})
                self.link_name_index.update({linkname:i})     
                self.joints.update({i-1:{'name':jname, 'parent':name_link_attached, 'child':linkname, 'type':"revolute", 'position':joint_po, 'jointAxis':a}})
                self.link_joint_ind.update({i-1:(self.link_name_index.get(name_link_attached), self.link_name_index.get(linkname))})
                self.dict_linkname_direc_avail.update({linkname:dcopy})
                self.dict_linkname_size.update({linkname:[x_l, y_l, z_l]})
                self.dict_link_jointloc_buffer.update({linkname:pj})
                self.numLinks += 1
            case 'DeleteLink':
                if self.numLinks < 3:
                    self.Mutate()
                    return
                availlinks = []
                parents = []
                for key in self.link_joint_ind.keys():
                        parent_ind, child_ind = self.link_joint_ind.get(key)
                        parents.append(parent_ind)
                for i in self.links.keys():
                    if i not in parents:
                        availlinks.append(i)
                if len(availlinks) == 0:
                    print('Error: Cyclic links or Bug')
                    exit()
                else:
                    linkindex = random.choice(availlinks)
                    linkname = self.links.get(linkindex).get('name')
                    joints_to_delete = []
                    if linkindex in self.sensorList:
                        self.sensorList.remove(linkindex)
                        self.numSensors -= 1
                    for key in self.link_joint_ind.keys():
                        parent_ind, child_ind = self.link_joint_ind.get(key)
                        if linkindex == child_ind:
                            joints_to_delete.append(key)
                    for i in joints_to_delete:
                        self.link_joint_ind.pop(i)
                        self.joint_names.remove(self.joints.get(i).get('name'))
                        self.joints.pop(i)
                    self.links.pop(linkindex)
                    self.link_names.remove(linkname)
                    self.link_name_index.pop(linkname)
                    self.dict_linkname_direc_avail.pop(linkname)
                    self.dict_linkname_size.pop(linkname)
                    self.dict_link_jointloc_buffer.pop(linkname)
                    self.numLinks -= 1
            case 'ChangeSize':
                linkindex = random.choice(list(self.links.keys()))
                link_dict = self.links.get(linkindex)
                size = link_dict.get('size')
                ax = random.choice(range(3))
                size[ax] = random.uniform(0.2, 2)
                link_dict.update({'size':size})
                self.links.update({linkindex:link_dict})