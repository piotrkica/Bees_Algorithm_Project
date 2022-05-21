import matplotlib.pyplot as plt
from src.bees import bees_algorithm
from src.generating import *
from src.map import Map

if __name__ == "__main__":
    n_cities = 15
    map_size = (25000, 25000)

    antennas = {
        "short": (13, 75),
        "medium": (13, 225),
        "long": (13, 450),
    }

    cities = generate_random_cities(map_size, n_cities=n_cities)
    cities_map = Map(map_size[0], map_size[1], cities, antennas)

    solution = bees_algorithm(cities_map.generate_random_solution, cities_map.sample_surrounding,
                              cities_map.calculate_cost, max_iterations=100)
    _, ax = plt.subplots()
    ax.set_xlim(0, map_size[0])
    ax.set_ylim(0, map_size[1])
    cities_map.plot_cities(ax)
    cities_map.plot_solution(solution, ax)
    plt.show()
