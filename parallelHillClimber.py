from solution import SOLUTION
import copy
import constants as c
import os
import matplotlib.pyplot as plt
import random

class PARALLEL_HILL_CLIMBER:
    def __init__(self, seed) -> None:
        os.system("del brain*.nndf")
        os.system("del body*.urdf")
        os.system("del fitness*.txt")
        self.nextAvailableID = 0
        self.parents = {}
        self.fits = []
        self.seed = seed
        random.seed(self.seed)
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

        self.EvaluateAfterMutation(self.children)

        # self.Print()

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
        best_fit = 0
        for i in self.parents.keys():
            parent = self.parents[i]
            child = self.children[i]
            if parent.fitness < child.fitness:
                    self.parents[i] = self.children[i]
            parent = self.parents[i]
            if parent.fitness > best_fit:
                best_fit = parent.fitness    
        self.fits.append(best_fit)

    def Print(self):
        print('\n')
        for i in self.parents.keys():
            print(self.parents[i].fitness, self.children[i].fitness)
        print('\n')

    def Show_Best(self):
        best_fitness = 0
        best_parent = 0
        for i in self.parents.keys():
            fit = self.parents[i].fitness
            if fit > best_fitness:
                best_fitness = fit
                best_parent = i
        plt.figure()
        plt.plot(range(1, c.numberOfGenerations+1), self.fits)
        plt.xlabel('Generations')
        plt.ylabel('Fitness')
        plt.title('Best Fitness:{}'.format(best_fitness))
        plt.savefig('population'+str(self.seed)+'.png')
        self.parents[best_parent].best_simulation('GUI')
        os.rename("bestbody.urdf",str(self.seed)+".urdf")
        os.rename("bestbrain.nndf",str(self.seed)+".nndf")
        return 0
