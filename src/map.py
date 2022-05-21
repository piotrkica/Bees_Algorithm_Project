from functools import reduce
from matplotlib import pyplot as plt
from src.generating import is_valid_antenna

from src.antenna import Antenna
from src.city import City
import numpy as np


class Map:
    def __init__(self, height, width, cities: [City], antennas):
        self.height = height
        self.width = width
        self.cities = cities
        self.antennas = antennas

    def calculate_cost(self, solution):
        def circles_intersection_area(circle_a, circle_b):
            x_a, y_a, r_a = circle_a
            x_b, y_b, r_b = circle_b
            distance = np.linalg.norm(np.array([x_a, y_a] - np.array([x_b, y_b])))
            if distance > r_a + r_b:
                return 0

            R = max(r_a, r_b)
            r = min(r_a, r_b)

            if R - r - distance > 0:
                return np.pi * r * r

            part1 = r * r * np.arccos((distance * distance + r * r - R * R) / (2 * distance * r))
            part2 = R * R * np.arccos((distance * distance + R * R - r * r) / (2 * distance * R))
            part3 = 0.5 * np.sqrt((-distance + r + R) * (distance + r - R) * (distance - r + R) * (distance + r + R))

            intersection_area = part1 + part2 - part3
            return intersection_area

        total_cost = 0
        for antenna_type, positions in solution.items():
            for pos in positions:
                radius = self.antennas[antenna_type][1]
                for city in self.cities:
                    total_cost += circles_intersection_area((*pos, radius), (city.x, city.y, city.radius))
        return total_cost

    def plot_cities(self, ax):
        city_circles = []
        for city in self.cities:
            city_circles.append(plt.Circle((city.x, city.y), city.radius, color='b'))
        for c in city_circles:
            ax.add_patch(c)

    def plot_solution(self, solution: [Antenna], ax):
        antennas_circles = []
        for antenna_type, positions in solution.items():
            _, antenna_range, _ = self.antennas[antenna_type]
            for pos in positions:
                antennas_circles.append(plt.Circle(pos, antenna_range, color='r'))
        for antenna_circle in antennas_circles:
            ax.add_patch(antenna_circle)

    def generate_random_solution(self):
        solution = {}
        for antenna_type, (antenna_count, antenna_range, antenna_bandwidth) in self.antennas.items():
            solution[antenna_type] = []
            for _ in range(antenna_count):
                random_coordinates = np.random.rand(2) * [self.width, self.height]
                while not is_valid_antenna(solution, (random_coordinates, antenna_range, antenna_bandwidth)):
                    random_coordinates = np.random.rand(2) * [self.width, self.height]
                solution[antenna_type].append(random_coordinates)
        return solution

    def sample_surrounding(self, solution, distance):
        antennas_count = reduce(lambda current_value, antenna_type: current_value + antenna_type[0],
                                self.antennas.values(), 0)

        def antena_idx_to_type(idx):
            for antenna_type, (count, _, _) in self.antennas.items():
                if idx < count:
                    return antenna_type, idx
                idx -= count

        sample = solution.copy()
        for key in sample:
            sample[key] = sample[key].copy()
        distances = np.sqrt(np.random.rand(antennas_count)) * distance
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
            new_pos = antenna_pos + [distance * np.cos(angle), distance * np.sin(angle)]
            sample[antenna_type][antenna_idx] = new_pos
        return sample
