import pygad

filename = 'genetic' # The filename to which the instance is saved. The name is without extension.
loaded_ga_instance = pygad.load(filename=filename)
loaded_ga_instance.plot_fitness()