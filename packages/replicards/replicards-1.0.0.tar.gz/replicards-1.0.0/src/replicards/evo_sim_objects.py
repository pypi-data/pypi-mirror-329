"""


"""

import copy
import random
import numpy as np
import matplotlib.pyplot as plt


class Organism:
    
    def __init__(self, name, fitness):
        self.name = name
        self.fitness = fitness
        
    def reproduce(self):
        num_of_offspring = np.random.poisson(self.fitness)
        offspring = []
        for i in range(num_of_offspring):
            offspring.append(copy.deepcopy(self))
        return offspring


class Population:
    
    def __init__(self, org_list):
        
        # All the organisms in the population
        self.organisms = org_list
        
        # Population size (number of organisms)
        self.size = len(org_list)
        
        # Initialize generation number
        self.gen = 0
        
        # Lineages
        self.names = list(set([org.name for org in self.organisms]))
        self.names.sort()
        
        # Initialize counts dictionary
        self.counts = dict({})
        org_names = self.get_current_org_names()
        for name in self.names:
            self.counts[name] = [org_names.count(name)]
        
        # Fixation: whether or not one lineage reached fixation
        self.fixation = (len(set(org_names)) == 1)
    
    def _update_counts(self):
        org_names = self.get_current_org_names()
        for name in self.names:
            self.counts[name].append(org_names.count(name))
        self.gen += 1
        if len(set(org_names)) == 1:
            self.fixation = True
    
    def get_current_org_names(self):
        ''' List of the names of all organism currently in the population. '''
        return [org.name for org in self.organisms]
    
    def get_latest_counts(self):
        latest = dict({})
        for name in self.names:
            latest[name] = self.counts[name][-1]
        return latest
    
    def plot_evolution(self):
        for name in self.names:            
            plt.plot(self.counts[name], label=name)
        plt.xticks(list(range(self.gen + 1)))
        plt.legend()
        plt.grid()
        plt.show()
    
    def update(self, org_list):
        self.organisms = org_list
        self._update_counts()


def create(org_name, fitness, n):
    ''' Creates `n` organisms with name `org_name` and specified `fitness`. '''
    return [Organism(org_name, fitness) for i in range(n)]

