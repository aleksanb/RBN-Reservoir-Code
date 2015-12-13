from utils import deviation_stats, fst, lst, glob_load, get_working_dir
from rbn_reservoir_problem import genotype_to_phenotype

import log
import logging


def load_rbns_from_ea():
    working_dir = get_working_dir()
    ea_runs = map(fst, glob_load(working_dir + '*-evolved'))

    best_genomes = map(lst, ea_runs)
    rbns = [genotype_to_phenotype(genome, 100, 2)
            for genome in best_genomes]

    return best_genomes, rbns


def caluclate_stats(genomes, rbns):
    deviation_stats('Fitness', [g.fitness for g in best_genomes])
    deviation_stats('Input connectivity', [len(rbn.input_connections)
                                           for rbn in rbns])


if __name__ == '__main__':
    log.setup(logging.DEBUG)

    genomes, rbns = load_rbns_from_ea()

    deviation_stats('Fitness', [g.fitness for g in genomes])
    deviation_stats('Input connectivity', [len(rbn.input_connections)
                                           for rbn in rbns])
