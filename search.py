import os
import random
from parallelHillClimber import PARALLEL_HILL_CLIMBER

for i in range(10):
    phc = PARALLEL_HILL_CLIMBER(i)
    phc.Evolve()
    phc.Show_Best()