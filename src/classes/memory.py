import pymem
import time
from src.classes.offsets import Offsets
from src.classes.math import Vec3
from src.classes.entity import Entity

class Memory:

    def __init__(self):
        self.Handle = None
        self.CLIENT_DLL = None
        self.ENGINE_DLL = None
        self.OFFSETS = Offsets()

    def yieldProcess(self, limit: int) -> bool:
        print('[sigma-kit] searching for cs2...')
        
        for i in range(limit):
            for i in pymem.process.list_processes():
                if i.szExeFile.decode('utf-8') == "cs2.exe":  
                    self.Handle = pymem.Pymem(i.th32ProcessID)
                    self.CLIENT_DLL = pymem.process.module_from_name(self.Handle.process_handle, "client.dll").lpBaseOfDll
                    self.ENGINE_DLL = pymem.process.module_from_name(self.Handle.process_handle, "engine2.dll").lpBaseOfDll
                    print(f'[sigma-kit] found cs2.exe with pid {i.th32ProcessID}')
                    return True
            time.sleep(1)

        print('[sigma-kit] unable to find cs2.')
        exit()

    def readPointer(self, address: int) -> int:
        try:
            return self.Handle.read_ulonglong(address)
        except pymem.exception.MemoryReadError:
            return 0

    def readInt(self, address: int) -> int:
        try:
            return self.Handle.read_int(address)
        except pymem.exception.MemoryReadError:
            return 

    def readFloat(self, address: int) -> float:
        try:
            return self.Handle.read_float(address)
        except pymem.exception.MemoryReadError:
            return 0
 
    def readVec3(self, address: int) -> Vec3:
        try:
            return Vec3(self.Handle.read_float(address), self.Handle.read_float(address + 4), self.Handle.read_float(address + 8))
        except pymem.exception.MemoryReadError:
            return 0, 0, 0

    def readString(self, address: int, size: int) -> str:
        try:
            return self.Handle.read_string(address, size)
        except pymem.exception.MemoryReadError:
            return ""
 
    def readRaw(self, address: int, size: int) -> bytes:
        try:
            return self.Handle.read_bytes(address, size)
        except pymem.exception.MemoryReadError:
            return b''
        
    def getLocalPlayerPtr(self) -> int:
        return self.readPointer(self.CLIENT_DLL + self.OFFSETS.getOffset('dwLocalPlayerController'))

    def getLocalPlayerPawn(self) -> int:
        return self.readPointer(self.CLIENT_DLL + self.OFFSETS.getOffset('dwLocalPlayerPawn'))

    def getLocalPlayer(self) -> Entity:
        return Entity(self.getLocalPlayerPtr(), self.getLocalPlayerPawn())

    def getLocalViewAngles(self) -> tuple:
        return self.readVec3(self.CLIENT_DLL + self.OFFSETS.getOffset('dwViewAngles'))

    def getEntity(self, entityId: int) -> Entity:
        entityList = self.readPointer(self.CLIENT_DLL + self.OFFSETS.getOffset('dwEntityList'))

        if entityList == 0:
            print('failed to get entityList')
            return

        controllerPtr = self.readPointer(entityList + 0x8 * (entityId >> 9) + 0x10)
        if controllerPtr == 0:
            print('failed to get entryPtr')
            return

        pawnPtr = self.readPointer(controllerPtr + 120 * (entityId & 0x1FF))
        if pawnPtr == 0:
            print('failed to get controllerPtr')
            return

        return Entity(self, controllerPtr, pawnPtr)

    def getEntities(self) -> list:
        _entityList: list = []
        for i in range(1, 65):
            entityList = self.readPointer(self.CLIENT_DLL + self.OFFSETS.getOffset('dwEntityList'))
            if entityList == 0:
                continue

            entryPtr = self.readPointer(entityList + 8 * ((i & 0x7FFF) >> 9) + 16)
            if entryPtr == 0:
                continue

            controllerPtr = self.readPointer(entryPtr + 120 * (i & 0x1FF))
            if controllerPtr == 0:
                continue

            controllerPawnPtr = self.readPointer(controllerPtr + self.OFFSETS.getClientOffset('CCSPlayerController', 'm_hPlayerPawn'))
            if controllerPawnPtr == 0:
                continue

            listEntryPtr = self.readPointer(entityList + 0x8 * ((controllerPawnPtr & 0x7FFF) >> 9) + 0x10)
            if listEntryPtr == 0:
                continue

            pawnPtr = self.readPointer(listEntryPtr + 120 * (controllerPawnPtr & 0x1FF))
            if pawnPtr == 0:
                continue

            _entityList.append(Entity(self, controllerPtr, pawnPtr))

        return _entityList
