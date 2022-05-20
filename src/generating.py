from random import randint
import numpy as np

from src.city import City


def is_valid_antenna(solution, new_antenna):  # TODO
    return True


def generate_random_solution(map_size, antennas: []):  # TODO convert to classes
    solution = {}
    for antenna_type, (antenna_count, antenna_range, antenna_bandwidth) in antennas.items():
        solution[antenna_type] = []
        for _ in range(antenna_count):
            random_coordinates = np.random.rand(2) * map_size
            while not is_valid_antenna(solution, (random_coordinates, antenna_range, antenna_bandwidth)):
                random_coordinates = np.random.rand(2) * map_size
            solution[antenna_type].append(random_coordinates)
    return solution


def generate_random_cities(map_size, n_cities) -> [City]:
    def gen_city():
        return City(x=randint(0, map_size[0]),
                    y=randint(0, map_size[1]),
                    radius=randint(500, 2000))

    def is_valid_city(new_city, min_dist=200):
        if not new_city.fits_on_map(map_size):
            return False

        for city in cities:
            radius_sum = city.radius + new_city.radius + min_dist
            distance = np.linalg.norm((city.x - new_city.x, city.y - new_city.y))
            if distance < radius_sum:
                return False

        return True

    cities = []
    for i in range(n_cities):
        city = gen_city()
        while not is_valid_city(city):
            city = gen_city()
        cities.append(city)

    return cities
