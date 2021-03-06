from matplotlib import pyplot as plt
from functools import reduce
from random import randint
import numpy as np

from src.city import City
from src.utils import circles_intersection_area


class Map:
    def __init__(self, height, width, cities: [City], antennas):
        self.height = height
        self.width = width
        self.cities = cities
        self.antennas = antennas

    def calculate_cost(self, solution):
        total_cost = 0
        for antenna_type, positions in solution.items():
            for pos in positions:
                radius = self.antennas[antenna_type][1]
                for city in self.cities:
                    if (pos[0], pos[1], radius) in city:
                        total_cost += int(3.14 * radius ** 2)
                    # total_cost += circles_intersection_area((*pos, radius), (city.x, city.y, city.radius))
        return total_cost

    def plot_solution(self, solution):
        _, ax = plt.subplots()
        ax.set_xlim(0, self.height)
        ax.set_ylim(0, self.width)

        for city in self.cities:
            city_circle = plt.Circle((city.x, city.y), city.radius, color='b')
            ax.add_patch(city_circle)

        for antenna_type, positions in solution.items():
            _, antenna_range = self.antennas[antenna_type]
            for pos in positions:
                antenna_circle = plt.Circle(pos, antenna_range, color='r')
                ax.add_patch(antenna_circle)

        plt.show()

    def generate_random_solution(self):
        def is_valid_antenna(solution, new_antenna, antenna_range):
            if antenna_range > new_antenna[0] or antenna_range > new_antenna[1]:
                return False
            if self.height - new_antenna[0] < antenna_range or self.width - new_antenna[1] < antenna_range:
                return False

            for antenna_type, antennas in solution.items():
                for antenna in antennas:
                    radius_sum = self.antennas[antenna_type][1] + antenna_range
                    if (antenna[0] - new_antenna[0]) ** 2 + (antenna[1] - new_antenna[1]) ** 2 < radius_sum ** 2:
                        return False

            return True

        solution = {}
        for antenna_type, (antenna_count, antenna_range) in self.antennas.items():
            solution[antenna_type] = []
            for _ in range(antenna_count):
                random_coordinates = [randint(0, self.height), randint(0, self.width)]
                while not is_valid_antenna(solution, random_coordinates, antenna_range):
                    random_coordinates = [randint(0, self.height), randint(0, self.width)]
                solution[antenna_type].append(random_coordinates)

        return solution

    def sample_surrounding(self, solution, distance):
        antennas_count = reduce(lambda current_value, antenna_type: current_value + antenna_type[0],
                                self.antennas.values(), 0)

        def antena_idx_to_type(idx):
            for antenna_type, (count, _) in self.antennas.items():
                if idx < count:
                    return antenna_type, idx
                idx -= count

        def is_intersecting(solution, antenna):
            new_pos, radius_a = antenna
            for antenna_type in solution:
                _, radius_b = self.antennas[antenna_type]
                for position in solution[antenna_type]:
                    if position == antenna_pos and radius_a == radius_b:
                        continue
                    if (position[0] - new_pos[0]) ** 2 + (position[1] - new_pos[1]) ** 2 < (radius_a + radius_b) ** 2:
                        return True
            return False
        
        sample = solution.copy()
        for key in sample:
            sample[key] = sample[key].copy()
        distances = np.random.rand(antennas_count) * distance
        distances.sort()
        current_distance = 0
        for idx, val in enumerate(distances):
            if idx == 0:
                current_distance = val
                continue
            distances[idx] -= current_distance
            current_distance += distances[idx]

        for index, distance in enumerate(distances):
            angle = np.random.rand() * np.pi * 2
            antenna_type, antenna_idx = antena_idx_to_type(index)
            antenna_pos = solution[antenna_type][antenna_idx]
            new_pos = [antenna_pos[0] + int(distance * np.cos(angle)), antenna_pos[1] + int(distance * np.sin(angle))]
            _, antenna_radius = self.antennas[antenna_type] 
            is_valid = False
            while not is_valid:
                is_valid = True
                if is_intersecting(sample, (new_pos, antenna_radius)):
                    is_valid = False
                    angle = np.random.rand() * np.pi * 2
                    distance = np.random.rand() * 2 * distance
                    new_pos = [antenna_pos[0] + int(distance * np.cos(angle)), antenna_pos[1] + int(distance * np.sin(angle))]
                    break
            sample[antenna_type][antenna_idx] = new_pos
        return sample
