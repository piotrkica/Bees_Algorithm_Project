from matplotlib import pyplot as plt

from src.antenna import Antenna
from src.city import City


class Map:
    def __init__(self, height, width, cities: [City]):
        self.height = height
        self.width = width
        self.cities = cities

    def calculate_cost(self, antennas: [Antenna]):
        total_cost = 0
        for antenna in antennas:
            for city in self.cities:  # todo optimize search somehow, although we can restrict n_cities to be small
                if antenna in city:
                    total_cost += 3.14 * antenna.radius ** 2
                    break

        return total_cost

    def plot_solution(self, solution: [Antenna]):  # , ax):

        antennas_circles = []
        for antenna_type, positions in solution.items():
            _, antenna_range, _ = solution[antenna_type]
            for pos in positions:
                antennas_circles.append(plt.Circle(pos, antenna_range, color='r'))
        for antenna_circle in antennas_circles:
            ax.add_patch(antenna_circle)