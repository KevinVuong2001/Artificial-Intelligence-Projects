# Kevin Vuong
# 8-Queens Problem with Genetic Algorithm

import random
import time

class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.calculate_fitness()
        self.selection_probability = 0

    def calculate_fitness(self): # Calculating the fitness with number of non-attacking pairs of queens
        clashes = 0 # Minimum
        n = len(self.chromosome)
        for i in range(n):
            for j in range(i + 1, n):
                # If the queens are in the same row
                if self.chromosome[i] == self.chromosome[j]:
                    clashes += 1
                # If the queens are in diagonal
                elif abs(self.chromosome[i] - self.chromosome[j]) == abs(i - j):
                    clashes += 1
        return 28 - clashes  # Max fitness is 28 (8 choose 2) - total number of clashes

def initial_population(population_size):
    population = []
    for _ in range(population_size):
        # Generate population
        chromosome = [random.randint(0, 7) for _ in range(8)]  # Including Duplicates
        population.append(Individual(chromosome))
    return population

def calculate_select_probabilities(population):
    total_fitness = 0
    for individual in population:
        total_fitness += individual.fitness
    for individual in population:
        # Calculate the probability with their fitness / total fitness of all population
        individual.selection_probability = individual.fitness / total_fitness

def select_parents(population):
    selection_probabilities = [individual.selection_probability for individual in population]
    parent1 = random.choices(population, weights=selection_probabilities, k=1)[0]
    parent2 = random.choices(population, weights=selection_probabilities, k=1)[0]
    return parent1, parent2

def crossover(parent1, parent2):
    crossover_point = random.randint(1, 7) # Generate a random crossover point
    child_chromosome = parent1.chromosome[:crossover_point] + parent2.chromosome[crossover_point:] # New child
    return Individual(child_chromosome)

def mutate(child, mutation_pct):
    if random.random() < mutation_pct: # Trigger mutation
        gene_to_mutate = random.randint(0, 7) # Randomly select an index to mutate
        new_gene = random.randint(0, 7) # Randomly choose a value
        child.chromosome[gene_to_mutate] = new_gene # Mutation applied with a random value
        child.fitness = child.calculate_fitness()  # Recalculate fitness after mutation

def generate_children(population, num_children, mutation_pct):
    children = []
    for _ in range(num_children):
        parent1, parent2 = select_parents(population)
        child = crossover(parent1, parent2) # Performing crossover
        mutate(child, mutation_pct) # Applied Mutation if it meets with the percentage
        children.append(child) # Update the list of children
    return children

def genetic_algorithm(population_size, num_iterations, mutation_pct):
    population = initial_population(population_size)
    start_time = time.time()
    generations = 0

    # Main purpose for this for plot data
    avg_fitness_history = []
    best_fitness_history = []

    # Log initial population
    print(f"Initial Population (Generation {generations}):")
    for ind in random.sample(population, min(6, len(population))):
        print(ind.chromosome, "Fitness:", ind.fitness)
    print("----------")

    for _ in range(num_iterations):
        calculate_select_probabilities(population) 
        children = generate_children(population, population_size, mutation_pct) # Generate the children
        population += children # Include children to population
        population.sort(key=lambda x: x.fitness, reverse=True) # Sort it based on fitness score
        population = population[:population_size]  # Keep population size constant

        generations += 1 # Updating the generation count

        # Calculate average and best fitness
        avg_fitness = sum(individual.fitness for individual in population) / population_size
        best_fitness = max(ind.fitness for ind in population)

        avg_fitness_history.append(avg_fitness) # Update the average fitness history
        best_fitness_history.append(best_fitness) # Update the best fitness history

        # Print fitness details for the current generation
        print(f"Generation {generations}: Avg Fitness: {avg_fitness}, Best Fitness: {best_fitness}")

        # If a perfect solution is found
        if best_fitness == 28:
            print("Perfect solution is found!")
            break

        # If average fitness is high enough
        if avg_fitness > 27:  # High average fitness indicates most solutions are close to optimal
            break

    end_time = time.time()
    best_solution = max(population, key=lambda x: x.fitness) # Get the best solution
    execution_time = end_time - start_time

    # Log final population
    print(f"Final Population (Generation {generations}):")
    for ind in random.sample(population, min(6, len(population))):
        print(ind.chromosome, "Fitness:", ind.fitness)
    print("----------")

    return best_solution, generations, execution_time, avg_fitness_history, best_fitness_history

if __name__ == '__main__':
    print("Welcome to the 8-Queens Problem")

    # User input for parameters
    population_size = int(input("Enter population size: "))
    num_iterations = int(input("Enter number of iterations: "))
    mutation_pct = float(input("Enter mutation percentage (e.g., 0.1 for 10%): "))

    # Running the genetic algorithm
    best_solution, generations, execution_time, avg_fitness_history, best_fitness_history = genetic_algorithm(population_size, num_iterations, mutation_pct)

    # Output the results
    print("Best solution found:", best_solution.chromosome)
    print("Best solution fitness:", best_solution.fitness)
    print("Number of generations:", generations)
    print("Execution time (seconds):", execution_time)
