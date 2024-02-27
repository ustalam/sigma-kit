class Vec3:

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def unpack(self) -> tuple:
        return self.x, self.y, self.z
