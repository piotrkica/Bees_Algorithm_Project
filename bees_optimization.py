class Antenna:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius


class City:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def __contains__(self, antenna: Antenna):
        return (antenna.x - self.x) ** 2 + (antenna.y - self.y) ** 2 < self.radius ** 2


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

    def plot_solution(self, antennas: [Antenna]):
        pass
        # todo copy plotting from notebook


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


if __name__ == "main":
    # TODO add function to generate initial solution from notebook
    height = 100
    width = 100
    cities = ["TODO"]
    cities_map = Map(height, width, cities)
    initial_solutions = ["TODO antennas"]

    optimizer = BeesOptimization(cities_map)
    best_solution, best_solution_cost = optimizer.find_best_solution(100, initial_solutions)

    print("Best solution cost: ", best_solution_cost)
    print("Best solution: ", best_solution)
    cities_map.plot_solution(best_solution)
