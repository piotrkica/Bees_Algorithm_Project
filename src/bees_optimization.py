import matplotlib.pyplot as plt
from src.bees import bees_algorithm
from src.generating import *
from src.map import Map
from src.antenna import Antenna


class BeesOptimization:
    def __init__(self, cities_map: Map):
        self.map = cities_map

    def find_new_solution(self, solution):
        new_solution = []  # todo

        return new_solution

    def find_best_solution(self, max_iterations, best_solution: [Antenna]):
        best_solution_cost = self.map.calculate_cost(best_solution)
        for i in range(max_iterations):
            new_solution = self.find_new_solution(best_solution)
            new_solution_cost = self.map.calculate_cost(new_solution)

            if new_solution_cost > best_solution_cost:
                best_solution_cost = new_solution_cost
                best_solution = new_solution

        return best_solution, best_solution_cost


if __name__ == "__main__":
    n_cities = 15
    map_size = (25000, 25000)

    antennas = {
        "short": (13, 75, 100), # (count, range, bandwidth)
        "medium": (13, 225, 100),
        "long": (13, 450, 100),
    }

    cities = generate_random_cities(map_size, n_cities=n_cities)
    cities_map = Map(map_size[0], map_size[1], cities, antennas)

    solution = bees_algorithm(cities_map.generate_random_solution, cities_map.sample_surrounding, cities_map.calculate_cost, max_iterations=100)
    _, ax = plt.subplots()
    ax.set_xlim(0, map_size[0])
    ax.set_ylim(0, map_size[1])
    cities_map.plot_cities(ax)
    cities_map.plot_solution(solution, ax)
    plt.show()