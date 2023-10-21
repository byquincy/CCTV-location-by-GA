import pygad
import drawByCV

from tqdm import tqdm
import csv

NUMBER_OF_CIRCLE = drawByCV.NUMBER_OF_CIRCLE
NUMBER_OF_GENERATIONS = 1000
fSolutions = None
fFitnesses = None
wrSolutions = None
wrFitnesses = None

pbar = tqdm(total=NUMBER_OF_GENERATIONS)

def fitness_func(ga_instance, solution, solution_idx):
    return drawByCV.getFitness(solution)

fitness_function = fitness_func

num_generations = NUMBER_OF_GENERATIONS # Number of generations.
num_parents_mating = 10 # Number of solutions to be selected as parents in the mating pool.

init_range_low = 0
init_range_high = 800


sol_per_pop = 50 # Number of solutions in the population.
num_genes = NUMBER_OF_CIRCLE*2  # (x, y) * 50
gene_type = int

# last_fitness = 0
def callback_generation(ga_instance):
    # global last_fitness

    best_solution = ga_instance.best_solution()    
    # print("Generation = {generation}".format(generation=ga_instance.generations_completed))
    # print("Fitness    = {fitness}".format(fitness=best_solution[1]))
    # print("Change     = {change}".format(change=best_solution[1] - last_fitness))

    # print(list(best_solution[0]))
    # last_fitness = best_solution[best_solution[1]]

    wrSolutions.writerow(best_solution[0])
    wrFitnesses.writerow([best_solution[1]])
    pbar.update()

def setFilePath(filePath):
    global fSolutions
    global fFitnesses
    global wrSolutions
    global wrFitnesses

    fSolutions = open('Solutions.csv', 'w', encoding='utf-8', newline='')
    fFitnesses = open("Fitnesses.csv", 'w', encoding='utf-8', newline='')
    wrSolutions = csv.writer(fSolutions)
    wrFitnesses = csv.writer(fFitnesses)

def start():
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

    pbar.close()
    fSolutions.close()
    fFitnesses.close()

# After the generations complete, some plots are showed that summarize the how the outputs/fitenss values evolve over generations.
# ga_instance.plot_fitness()