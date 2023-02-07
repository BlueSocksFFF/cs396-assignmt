import pybullet as p
import pyrosim.pyrosim as pyrosim

class MOTOR:
    def __init__(self, jointName) -> None:
        self.jointName = jointName

    def Set_Value(self, idn, desiredAngle):
        pyrosim.Set_Motor_For_Joint(
                bodyIndex = idn,
                jointName = self.jointName,
                controlMode = p.POSITION_CONTROL,
                targetPosition = desiredAngle,
                maxForce = 25)
