import random
import matplotlib.pyplot as plt
import numpy as np

# Параметри задачі про рюкзак
capacity = 250
num_items = 100
items = [(random.randint(2, 20), random.randint(1, 10)) for _ in range(num_items)]

# Параметри генетичного алгоритму
population_size = 100
crossover_point = 50
mutation_probability = 0.05
local_improvement_probability = 0.2
iterations = 1000
local_improvement_iterations = 10


def fitness(individual):
    total_value = sum(item[0] for i, item in enumerate(items) if individual[i] == 1)
    total_weight = sum(item[1] for i, item in enumerate(items) if individual[i] == 1)
    return total_value if total_weight <= capacity else 0


def crossover(parent1, parent2):
    point = random.randint(0, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def mutate(individual):
    index = random.randint(0, len(individual) - 1)
    individual[index] = 1 - individual[index]


def local_improvement(individual):
    for _ in range(local_improvement_iterations):
        if random.random() < local_improvement_probability:
            mutate(individual)


def genetic_algorithm():
    population = [
        [random.randint(0, 1) for _ in range(num_items)] for _ in range(population_size)
    ]
    best_fitness_history = []

    for generation in range(iterations):
        population.sort(key=lambda ind: -fitness(ind))
        best_individual = population[0]
        best_fitness_history.append(fitness(best_individual))

        new_population = []

        for _ in range(population_size // 2):
            parent1, parent2 = random.choices(population[:10], k=2)
            child1, child2 = crossover(parent1, parent2)

            if random.random() < mutation_probability:
                mutate(child1)
            if random.random() < mutation_probability:
                mutate(child2)

            local_improvement(child1)
            local_improvement(child2)

            new_population.extend([child1, child2])

        population = new_population

    return best_individual, best_fitness_history


best_solution, fitness_history = genetic_algorithm()


def main():
    best_solution, fitness_history = genetic_algorithm()

    # Графік залежності якості розв'язку від числа ітерацій
    iterations = len(fitness_history)
    iterations_range = np.arange(20, iterations + 1, 20)

    plt.plot(iterations_range, fitness_history[: len(iterations_range)], marker="o")
    plt.xlabel("Number of Iterations")
    plt.ylabel("Fitness")
    plt.title("Genetic Algorithm for Knapsack Problem")
    plt.show()

    print("Best Solution:", best_solution)
    print("Best Fitness:", fitness(best_solution))


if __name__ == "__main__":
    main()
