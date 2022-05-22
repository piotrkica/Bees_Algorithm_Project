from src.bees import bees_algorithm
from src.generating import *
from src.map import Map
from src.utils import get_score
from matplotlib import pyplot as plt

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

    # solution, solution_area = bees_algorithm(cities_map.generate_random_solution, cities_map.sample_surrounding,
    #                                          cities_map.calculate_cost, max_iterations=100)
    # cities_map.plot_solution(solution)


    values = []
    iterations = list(range(10, 210, 10))
    for i in iterations:
        _, solution_area = bees_algorithm(cities_map.generate_random_solution, cities_map.sample_surrounding,
                                             cities_map.calculate_cost, max_iterations=i)
        values.append(solution_area)
    plt.plot(iterations, values)
    plt.title("Wartość funkcji celu od ilości iteracji")
    plt.show()


    print("Score: " + str(get_score(antennas, solution_area) * 100) + "%")
