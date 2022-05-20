from src.antenna import Antenna


class City:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def __contains__(self, antenna: Antenna):
        return (antenna.x - self.x) ** 2 + (antenna.y - self.y) ** 2 < self.radius ** 2

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.radius})"

    def fits_on_map(self, map_size):
        if self.radius > self.x or self.radius > self.y:
            return False
        if map_size[0] - self.x < self.radius or map_size[1] - self.y < self.radius:
            return False

        return True