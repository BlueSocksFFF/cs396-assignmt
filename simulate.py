from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
try:
    afterEvolution = bool(sys.argv[3])
    simulation = SIMULATION(directOrGUI, solutionID, afterEvolution)
except:
    simulation = SIMULATION(directOrGUI, solutionID)

simulation.Run()

