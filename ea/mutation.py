from tools import Mixin
import random


def per_genome_mutation(probability=0.01, mutate=None):
    def fn(genome):
        if random.random() < probability:
            component_to_mutate = random.randint(0, len(genome) - 1)
            if mutate:
                mutate(genome, component_to_mutate)
            else:
                genome.mutate(component_to_mutate)
        return genome
    return Mixin('per_genome_mutation', fn, {'probability': probability,
                                             'mutate': mutate})


def per_genome_component_mutation(probability=0.01, mutate=None):
    def fn(genome):
        for i, _ in enumerate(genome):
            if random.random() < probability:
                if mutate:
                    mutate(genome, i)
                else:
                    genome.mutate(i)
        return genome
    return Mixin('per_genome_component_mutation', fn, {
        'probability': probability,
        'mutate': mutate,
    })
