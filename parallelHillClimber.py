from solution import SOLUTION
import copy
import constants as c
import os
import matplotlib.pyplot as plt
import random

class PARALLEL_HILL_CLIMBER:
    def __init__(self) -> None:
        os.system("del brain*.nndf")
        os.system("del fitness*.txt")
        self.nextAvailableID = 0
        self.parents = {}
        self.fits = {}
        for i in range(c.populationSize):
            random.seed(i)
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID = self.nextAvailableID + 1
            self.fits[i] = []

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
                self.Evolve_For_One_Generation()
            
    def Evolve_For_One_Generation(self):
        self.Spawn()

        self.Mutate()

        self.EvaluateAfterMutation(self.children)

        self.Print()

        self.Select()

    def EvaluateAfterMutation(self, solutions):
        for solution in solutions.values():
            solution.start_simulation_after_mutation('DIRECT')
        for solution in solutions.values():
            solution.Wait_For_Simulation_To_End()

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
            if parent.fitness < child.fitness:
                    self.parents[i] = self.children[i]
            self.fits[i].append(parent.fitness)

    def Print(self):
        print('\n')
        for i in self.parents.keys():
            print(self.parents[i].fitness, self.children[i].fitness)
        print('\n')

    def Show_Best(self):
        best_fitness = 0
        best_parent = 0
        for i in self.parents.keys():
            if self.parents[i].fitness > best_fitness:
                best_fitness = self.parents[i].fitness
                best_parent = i
                plt.plot(range(1, c.numberOfGenerations+1), self.fits[i])
                plt.xlabel('Generations')
                plt.ylabel('Fitness')
                plt.title('Best Fitness:{fitness}'.format(best_fitness))
            self.parents[best_parent].start_simulation_after_mutation('GUI')
        return 0
