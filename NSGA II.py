import pygad
import drawByCV

import time
from tqdm import tqdm

NUMBER_OF_CIRCLE = drawByCV.NUMBER_OF_CIRCLE
NUMBER_OF_GENERATIONS = 300

pbar = tqdm(total=NUMBER_OF_GENERATIONS)

# function_inputs = []
# for i in range(NUMBER_OF_CIRCLE*2):
#     function_inputs.append(800*random.random())

def fitness_func(ga_instance, solution, solution_idx):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function calulates the sum of products between each input and its corresponding weight.
    return drawByCV.getFitness(solution)

fitness_function = fitness_func

num_generations = NUMBER_OF_GENERATIONS # Number of generations.
num_parents_mating = 7 # Number of solutions to be selected as parents in the mating pool.

init_range_low = 0
init_range_high = 800

# To prepare the initial population, there are 2 ways:
# 1) Prepare it yourself and pass it to the initial_population parameter. This way is useful when the user wants to start the genetic algorithm with a custom initial population.
# 2) Assign valid integer values to the sol_per_pop and num_genes parameters. If the initial_population parameter exists, then the sol_per_pop and num_genes parameters are useless.
sol_per_pop = 50 # Number of solutions in the population.
num_genes = NUMBER_OF_CIRCLE*2  # (x, y) * 50
gene_type = int

last_fitness = 0
startTime = time.time()
def callback_generation(ga_instance):
    global last_fitness
    global startTime

    best_solution = ga_instance.best_solution()    
    print("Generation = {generation}".format(generation=ga_instance.generations_completed))
    print("Fitness    = {fitness}".format(fitness=best_solution[1]))
    print("Change     = {change}".format(change=best_solution[1] - last_fitness))
    print("Time       = %.2f"%(time.time() - startTime))
    print(best_solution[0])
    startTime = time.time()
    last_fitness = best_solution[1]

    pbar.update()
    print("\n\n")

# Creating an instance of the GA class inside the ga module. Some parameters are initialized within the constructor.
ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating, 
                       fitness_func=fitness_function,
                       sol_per_pop=sol_per_pop, 
                       num_genes=num_genes,
                       gene_type=gene_type,

                       init_range_low=init_range_low,
                       init_range_high=init_range_high,

                       on_generation=callback_generation)

# Running the GA to optimize the parameters of the function.
ga_instance.run()

filename = 'genetic' # The filename to which the instance is saved. The name is without extension.
ga_instance.save(filename=filename)

pbar.close()
exit()

# After the generations complete, some plots are showed that summarize the how the outputs/fitenss values evolve over generations.
ga_instance.plot_fitness()

# Returning the details of the best solution.
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))

drawByCV.visualize(solution)

if ga_instance.best_solution_generation != -1:
    print("Best fitness value reached after {best_solution_generation} generations.".format(best_solution_generation=ga_instance.best_solution_generation))

# Saving the GA instance.
filename = 'genetic' # The filename to which the instance is saved. The name is without extension.
ga_instance.save(filename=filename)

# Loading the saved GA instance.
loaded_ga_instance = pygad.load(filename=filename)
loaded_ga_instance.plot_fitness()