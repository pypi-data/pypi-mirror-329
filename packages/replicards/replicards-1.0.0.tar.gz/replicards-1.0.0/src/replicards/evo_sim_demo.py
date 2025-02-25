"""


"""

import random
from evo_sim_objects import Population, create


# Initialize population
pop = Population(create('A', 5, 8) +
                 create('B', 4, 8) +
                 create('C', 3, 8))

# Population size
N = pop.size

# Keep evolving until fixation is reached
while not pop.fixation:
    
    # Reproduction based on fitness
    pop_offspring = []
    for org in pop.organisms:
        pop_offspring += org.reproduce()
    parents_and_offspring = pop.organisms + pop_offspring
    
    # Maintain population size constant at N, the environment's carrying capacity
    new_pop = random.sample(parents_and_offspring, N)
    
    # Update the population
    pop.update(new_pop)

# Plot results of the evolutionary simulation
pop.plot_evolution()













