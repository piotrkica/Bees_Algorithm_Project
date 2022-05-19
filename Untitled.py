
from functools import reduce
from matplotlib import pyplot as plt
from random import randint, shuffle
import numpy as np

MAP_SIZE = (25000, 25000)
SOLUTIONS_COUNT = 50
CITIES_COUNT = 15

antennas = {
    "short": (13, 75, 100), # (count, range, bandwidth)
    "medium": (13, 225, 100),
    "long": (13, 450, 100),
}

def is_valid_antenna(solution, new_antenna):
    return True

def generate_random_solution():
    solution = {}
    for antenna_type, (antenna_count, antenna_range, antenna_bandwidth) in antennas.items():
        solution[antenna_type] = []
        for _ in range(antenna_count):
            random_coordinates = np.random.rand(2) * MAP_SIZE
            while not is_valid_antenna(solution, (random_coordinates, antenna_range, antenna_bandwidth)):
                random_coordinates = np.random.rand(2) * MAP_SIZE
            solution[antenna_type].append(random_coordinates)
    return solution

def is_valid_city(cities, new_city):
    if new_city[2] > new_city[0] or new_city[2] > new_city[1]:
        return False
    if MAP_SIZE[0] - new_city[0] < new_city[2] or MAP_SIZE[1] - new_city[1] < new_city[2]:
        return False
        
    for city in cities:
        radius_sum = city[2] + new_city[2] + 200
        distance = np.linalg.norm((city[0] - new_city[0], city[1] - new_city[1]))
        if radius_sum > distance:
            return False
    return True

def generate_random_cities():
    # (x, y, radius, bandwidth){{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}
    gen_city = lambda: (randint(0, MAP_SIZE[0]), randint(0, MAP_SIZE[1]), randint(500, 2000), randint(50, 150))
    cities = [] 
    for i in range(CITIES_COUNT):
        random_city = gen_city()
        while not is_valid_city(cities, random_city):
            random_city = gen_city()
        cities.append(random_city)
    return cities

def metric(solution_a, solution_b):
    result = 0
    for antena_a, antena_b in zip(solution_a, solution_b):
        result += np.linalg.norm(np.array(antena_a) - np.array(antena_b))
    return result

def circles_intersection_area(circle_a, circle_b):
    x_a, y_a, r_a = circle_a
    x_b, y_b, r_b = circle_b
    distance = np.linalg.norm(np.array([x_a, y_a] - np.array([x_b, y_b])))
    if distance > r_a + r_b:
        return 0
    
    R = max(r_a, r_b)
    r = min(r_a, r_b)
    part1 = r * r * np.arccos((distance * distance + r * r - R * R) / (2 * distance * r))
    part2 = R * R * np.arccos((distance * distance + R * R - r * r) / (2 * distance * R))
    part3 = 0.5 * np.sqrt((-distance + r + R) * (distance + r-R) * (distance-r + R) * (distance + r + R))

    intersection_area = part1  +  part2 - part3
    return intersection_area

def goal_function(solution):
    result = 0
    for antenna_type, positions in solution.items():
        for pos in positions:
            radius = antennas[antenna_type][1]
            for city_x, city_y, city_r, bandwidth in cities:
                result += bandwidth * circles_intersection_area((*pos, radius), (city_x, city_y, city_r))

def bees_algorithm(scouts_count, goal_function):
    scouts = generate_random_solution()
    

def sample_surrounding(solution):
    antennas_count = reduce(lambda current_value, antenna_type: current_value + antenna_type[0], antennas.values(), 0)
    def antena_idx_to_type(idx):
        for antenna_type, (count, _, _) in antennas.items():
            if idx < count:
                return antenna_type, idx
            idx -= count
            
    sample = solution.copy()
    for key in sample:
        sample[key] = sample[key].copy()
    random_order = list(range(antennas_count))
    shuffle(random_order)
    distance = 100000
    for index in random_order:
        move_distance = np.sqrt(np.random.rand()) * distance
        distance -= move_distance
        angle = np.random.rand() * np.pi * 2
        antenna_type, antenna_idx = antena_idx_to_type(index)
        antenna_pos = solution[antenna_type][antenna_idx]
        new_pos = antenna_pos + [move_distance * np.cos(angle), move_distance * np.sin(angle)]
        sample[antenna_type][antenna_idx] = new_pos
    return sample
            
def sample_surrounding2(solution):
    antennas_count = reduce(lambda current_value, antenna_type: current_value + antenna_type[0], antennas.values(), 0)
    def antena_idx_to_type(idx):
        for antenna_type, (count, _, _) in antennas.items():
            if idx < count:
                return antenna_type, idx
            idx -= count
    sample = solution.copy()
    for key in sample:
        sample[key] = sample[key].copy()
    distance = 100000
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
def plot_solution(solution, ax, color='r'):
    antennas_circles = []
    for antenna_type, positions in solution.items():
        _, antenna_range, _ = antennas[antenna_type]
        for pos in positions:
            antennas_circles.append(plt.Circle(pos, antenna_range, color=color))
    for antenna_circle in antennas_circles:
        ax.add_patch(antenna_circle)

def main():
    initial_solutions = [generate_random_solution() for _ in range(SOLUTIONS_COUNT)]
    cities = generate_random_cities()
    city_circles = [plt.Circle((c[0], c[1]), c[2], color='b') for c in cities]
    antennas_circles = []
    _, ax = plt.subplots()
    ax.set_xlim([0, MAP_SIZE[0]])
    ax.set_ylim([0, MAP_SIZE[1]])
    # for c in city_circles:
    #     ax.add_patch(c)
    sample = sample_surrounding(initial_solutions[0])
    plot_solution(initial_solutions[0], ax) 
    plot_solution(sample, ax, color='g')
    _, ax2 = plt.subplots()
    sample2 = sample_surrounding2(initial_solutions[0])
    plot_solution(initial_solutions[0], ax2)
    plot_solution(sample2, ax2, color='g')
    ax2.set_xlim([0, MAP_SIZE[0]])
    ax2.set_ylim([0, MAP_SIZE[1]])
    plt.show()
main() 