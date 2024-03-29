import os
import time
from parallelHillClimber import PARALLEL_HILL_CLIMBER

afterEvolution = True

if not afterEvolution:
    for i in range(10):
        phc = PARALLEL_HILL_CLIMBER(i)
        phc.Evolve()
        phc.Show_Best()
    afterEvolution = True
else:
    os.system("del *.txt")
    for i in range(5, 7):
        os.system("python simulate.py GUI "+str(i)+" True")
        time.sleep(1)