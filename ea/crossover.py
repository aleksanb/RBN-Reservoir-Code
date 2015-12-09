from tools import Mixin
from genotypes import SymbolVectorGenotype
import random


def split_crossover(p=1):
    def fn(parent_a, parent_b):
        child = SymbolVectorGenotype(parent_a.symbol_set_size, len(parent_a))
        if random.random() < p:
            split = random.randint(0, len(parent_a) - 1)
            for i, _ in enumerate(child):
                child[i] = parent_a[i] if i < split else parent_b[i]
        else:
            for i, _ in enumerate(parent_a):
                child[i] = parent_a[i]
            child.fitness = parent_a.fitness
        return child
    return Mixin('split_crossover', fn, kwargs={'p': p})


def genome_component_crossover(p=1):
    def fn(parent_a, parent_b):
        child = SymbolVectorGenotype(parent_a.symbol_set_size, len(parent_a))
        if random.random() < p:
            for i, _ in enumerate(child):
                child[i] = parent_a[i] if random.random() < 0.5\
                    else parent_b[i]
            return child
        else:
            for i, _ in enumerate(parent_a):
                child[i] = parent_a[i]
            child.fitness = parent_a.fitness
        return child
    return Mixin('genome_component_crossover', fn, kwargs={'p': p})
