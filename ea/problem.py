from ea.genotypes import SymbolVectorGenotype


class Problem(object):

    genotype_symbol_set_size = 2

    def initial_population(self):
        return [SymbolVectorGenotype(self.genotype_symbol_set_size,
                                     self.problem_size)
                for j in range(self.children_pool_size)]
