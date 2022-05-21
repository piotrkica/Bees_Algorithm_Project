class Neighbourhood:
    MAX_NO_IMPROVEMENT_ITERATIONS = 10
    best_solution = None

    def __init__(self, generate_solution, generate_sample, goal_function, radius) -> None:
        self.generate_solution = generate_solution
        self.scout = generate_solution()
        self.foragers = []
        self.generate_sample = generate_sample
        self.goal_function = goal_function
        self.current_radius = radius
        self.initial_radius = radius
        self.iterations_count = 0

    def recruit_foragers(self, count):
        for _ in range(count):
            forager = self.generate_sample(self.scout, self.current_radius)
            self.foragers.append(forager)

    def local_search(self):
        best = max(self.foragers, key=self.goal_function)
        if self.goal_function(best) > self.goal_function(self.scout):
            self.scout = best
            if Neighbourhood.best_solution is None or self.goal_function(self.scout) > self.goal_function(Neighbourhood.best_solution):
                Neighbourhood.best_solution = self.scout
        else:
            self.current_radius *= 0.7
            self.iterations_count += 1
            if self.iterations_count == self.MAX_NO_IMPROVEMENT_ITERATIONS:
                if Neighbourhood.best_solution is None or self.goal_function(self.scout) > self.goal_function(self.best_solution):
                    Neighbourhood.best_solution = self.scout
                self.global_search()
        self.foragers = []

    def global_search(self):
        self.scout = self.generate_solution()
        self.current_radius = self.initial_radius 

def bees_algorithm(
    generate_solution,
    sample_surrounding,
    goal_function,
    scouts_count=45,
    promising_sites_count=6,
    elite_sites_count=4,
    max_iterations=300,
    neighbourhood_radius=100000
):
    iterations_count = 0
    neighbourhoods = [Neighbourhood(generate_solution, sample_surrounding, goal_function, neighbourhood_radius) for _ in range(scouts_count)]
    while iterations_count < max_iterations:
        neighbourhoods.sort(key=lambda n: goal_function(n.scout), reverse=True)
        for i in range(elite_sites_count):
            neighbourhoods[i].recruit_foragers(20)            
        for i in range(promising_sites_count):
            neighbourhoods[elite_sites_count + i].recruit_foragers(8) 
        for i in range(elite_sites_count + promising_sites_count):
            neighbourhoods[i].local_search()
        for i in range(elite_sites_count + promising_sites_count, len(neighbourhoods)):
            neighbourhoods[i].global_search()
        iterations_count += 1
    return Neighbourhood.best_solution
