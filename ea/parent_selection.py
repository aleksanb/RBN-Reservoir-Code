from tools import Mixin
import random
try:
    import numpypy as np
except:
    import numpy as np


def fitness_proportionate_selection():
    def fn(population, fitnesses=None):
        fitnesses = fitnesses or\
            [individual.fitness for individual in population]
        total_fitness = sum(fitnesses)
        roll = random.uniform(0, total_fitness)
        counter = 0
        for fitness, individual in zip(fitnesses, population):
            counter += fitness
            if counter >= roll:
                return individual
    return Mixin('fitness_proportionate_selection', fn)


def sigma_scaling_selection():
    fps = fitness_proportionate_selection()

    def fn(population):
        fitnesses = [individual.fitness for individual in population]
        average_fitness = np.mean(fitnesses)
        standard_deviation = np.std(fitnesses)
        standard_deviation = max(0.0001, standard_deviation)
        scaled_fitnesses = [1 + (fitness - average_fitness) /
                            (2 * standard_deviation)
                            for fitness in fitnesses]
        return fps(population, fitnesses=scaled_fitnesses)
    return Mixin('sigma_scaling_selection', fn)


def tournament_selection(k=1, epsilon=0.05):

    def fn(population):
        tournament_participants = random.sample(population, k)
        if random.random() < epsilon:
            return random.choice(tournament_participants)
        else:
            return max(tournament_participants, key=lambda x: x.fitness)
    return Mixin('tournament_selection', fn, kwargs={'k': k,
                                                     'epsilon': epsilon})


def rank_selection():
    fps = fitness_proportionate_selection()

    def fn(population):
        sorted_population = sorted(population,
                                   key=lambda individual: individual.fitness)
        fitnesses = [individual.fitness for individual in population]
        min_fitness = min(fitnesses)
        max_fitness = max(fitnesses)
        N = len(population)
        scaled_fitnesses = [min_fitness + (max_fitness - min_fitness) * i /
                            (N - 1) for i in range(N)]
        return fps(sorted_population, fitnesses=scaled_fitnesses)
    return Mixin('rank_selection', fn)


def random_selection():
    def fn(population):
        return random.choice(population)
    return Mixin('random_selection', fn)
