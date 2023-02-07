from solution import SOLUTION
import copy
import constants as c
import os
import random as rand

class PARALLEL_HILL_CLIMBER:
    def __init__(self) -> None:
        os.system("del brain*.nndf")
        os.system("del fitness*.txt")
        self.nextAvailableID = 0
        self.parents = {}
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID = self.nextAvailableID + 1

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
                self.Evolve_For_One_Generation()
            
    def Evolve_For_One_Generation(self):
        self.Spawn()

        self.Mutate()

        self.Evaluate(self.children)

        self.Print()

        self.Select()

    def Spawn(self):
        self.children = {}
        for i in self.parents.keys():
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID = self.nextAvailableID + 1

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()

    def Evaluate(self, solutions):
        for solution in solutions.values():
            solution.Start_Simulation('DIRECT')
        for solution in solutions.values():
            solution.Wait_For_Simulation_To_End()


    def Select(self):
        for i in self.parents.keys():
            parent = self.parents[i]
            child = self.children[i]
            parent_fell = parent.fell_on_ground
            child_fell = child.fell_on_ground
            if (parent_fell and child_fell) or ((not parent_fell) and (not child_fell)):
                if parent.fitness > child.fitness:
                    self.parents[i] = self.children[i]
            else:
                if parent_fell:
                    self.parents[i] = self.children[i]

    def Print(self):
        print('\n')
        for i in self.parents.keys():
            print(self.parents[i].fell_on_ground, self.children[i].fell_on_ground)
            print(self.parents[i].fitness, self.children[i].fitness)
        print('\n')

    def Show_Best(self):
        best_fitness = 10
        best_parent = 0
        for i in self.parents.keys():
            if self.parents[i].fitness < best_fitness:
                best_fitness = self.parents[i].fitness
                best_parent = i
        self.parents[best_parent].Start_Simulation('GUI')
