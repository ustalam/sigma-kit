from src.classes.math import Vec3

class Entity:

    def __init__(self, memory, controllerPtr: int, pawnPtr: int):
        self.Memory = memory
        self.OFFSETS = memory.OFFSETS
        self.controllerPtr: int = controllerPtr
        self.pawnPtr: int = pawnPtr
        pass

    def getEyeAngles(self) -> tuple:
        return self.Memory.readVec3(self.pawnPtr + self.OFFSETS.getClientOffset('C_CSPlayerPawnBase', 'm_angEyeAngles'))
    
    def getPos(self) -> Vec3:
        return self.Memory.readVec3(self.pawnPtr + self.OFFSETS.getClientOffset('C_BasePlayerPawn', 'm_vOldOrigin'))
    
    def getTeam(self) -> int:
        return self.Memory.readInt(self.pawnPtr + self.OFFSETS.getClientOffset('C_BaseEntity', 'm_iTeamNum'))
 
    def getHealth(self) -> int:
        return self.Memory.readInt(self.pawnPtr + self.OFFSETS.getClientOffset('C_BaseEntity', 'm_iHealth'))

    def getName(self) -> str:
        return self.Memory.readString(self.controllerPtr + self.OFFSETS.getClientOffset('CBasePlayerController', 'm_iszPlayerName'), 256)
