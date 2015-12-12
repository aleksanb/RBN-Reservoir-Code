import logging
import json
import arrow
from ea.genotypes import SymbolVectorGenotype
import os.path
try:
    import numpypy as np
except:
    import numpy as np

logger = logging.getLogger()


def do_logging(adults, generation):
    logger.info('Generation: %s' % generation)
    logger.info('Current generation best individual: %s' % adults[-1])

    fitnesses = [x.fitness for x in adults]
    mean = np.mean(fitnesses)
    std = np.std(fitnesses)

    q1 = fitnesses[len(fitnesses) * 1 / 4 - 1]
    q2 = fitnesses[len(fitnesses) * 2 / 4 - 1]
    q3 = fitnesses[len(fitnesses) * 3 / 4 - 1]

    logging.info('Current generation fitness mean: %s' % mean)
    logging.info('Current generation fitness std: %s' % std)
    logging.info('Current generation quantiles: %s' % [q1, q2, q3])


def solve(problem, path='', state_file_path=''):
    state_file = 'state.dat'
    if path:
        state_file = path + state_file

    children = None
    adults = None
    generation = None
    just_loaded = False

    if state_file_path:
        if not os.path.isfile(state_file_path):
            logger.info(
                'No persistance data found, starting new persistance log in ' +
                state_file_path)
        else:
            try:
                with open(state_file_path, 'r') as f:
                    data = json.loads(f.readlines()[-1])
                    children = map(SymbolVectorGenotype.deserialize,
                                   data['children'])
                    adults = map(SymbolVectorGenotype.deserialize,
                                 data['adults'])
                    generation = data['generation']
                    just_loaded = True
            except Exception, e:
                logger.error(e)

    children = children or problem.initial_population()
    adults = adults or []
    generation = generation or 0

    while (adults[-1].fitness if adults else 0) <\
            problem.fitness_satisfaction_threshold and\
            generation < problem.maximum_generations:

        if not just_loaded:
            logger.debug('Persisting state...')
            did_persist = False
            try:
                with open(state_file, 'a') as f:
                    f.write('%s\n' % json.dumps({
                        'children': map(lambda x: x.serialize(), children),
                        'adults': map(lambda x: x.serialize(), adults),
                        'generation': generation,
                        'time': arrow.utcnow().isoformat(),
                    }))
                    did_persist = True
                    logger.debug('Persist complete.')
            except Exception, e:
                logger.error(e)
            if not did_persist:
                logger.error('Could not persist state!')
        else:
            just_loaded = False

        for child in children:
            child.fitness = problem.calculate_fitness(child)
        adults = problem.select_adults(adults, children,
                                       problem.adult_pool_size)
        adults.sort(key=lambda x: x.fitness)
        parents = [(problem.select_parent(adults),
                    problem.select_parent(adults))
                   for i in range(problem.children_pool_size)]
        children = [problem.crossover(parent_a, parent_b)
                    for parent_a, parent_b in parents]
        children = [problem.mutate(child) for child in children]
        children.sort(key=lambda x: x.fitness)

        generation += 1

        do_logging(adults, generation)

    logger.info('Simulation completed!')

    return generation, adults
