import time, os
from src.classes.memory import Memory

class Client:

    def __init__(self):

        self.Memory = Memory()
        print('[sigma-kit] Initialized client')
        pass 

    def _(self): # shit example
        os.system('cls')
        for entity in self.Memory.getEntities():
            name = entity.getName()
            team = entity.getTeam()
            health = entity.getHealth()
            pos_x, pos_y, pos_z = entity.getPos().unpack()
            eyeAngles_x, eyeAngles_y, eyeAngles_z = entity.getEyeAngles().unpack()

            print(f'name: {name} \nteam: {team} \nhealth: {health}  \nplayer pos:  x: {pos_x} y: {pos_y} z: {pos_z} \neyeAngles:  x: {eyeAngles_x} y: {eyeAngles_y} z: {eyeAngles_z}\n')
            
    def run(self):
        if self.Memory.yieldProcess(15):
            while True:
                self._()
                time.sleep(1)
