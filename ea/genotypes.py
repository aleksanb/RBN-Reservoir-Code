import random


class SymbolVectorGenotype():

    def __init__(self, symbol_set_size, length, symbols=None, fitness=None):
        self.symbol_set_size = symbol_set_size
        self.symbols = symbols or [random.randrange(symbol_set_size)
                                   for i in range(length)]
        self.fitness = fitness

    def mutate(self, i):
        self.symbols[i] = random.randrange(self.symbol_set_size)
        self.fitness = None

    def __getitem__(self, i):
        return self.symbols[i]

    def __setitem__(self, i, item):
        self.symbols[i] = item

    def __len__(self):
        return len(self.symbols)

    def __repr__(self):
        return ' '.join(map(str, self.symbols)) + ':' + str(self.fitness)

    def __int__(self):
        print "Method not well behaved for symbol size > 10"
        return reduce(lambda x, y: (x << 1) | y, self.symbols)

    def serialize(self):
        return {
            'symbol_set_size': self.symbol_set_size,
            'symbols': self.symbols,
            'fitness': self.fitness,
        }

    @classmethod
    def deserialize(cls, data):
        return cls(data['symbol_set_size'],
                   len(data['symbols']),
                   symbols=data['symbols'],
                   fitness=data['fitness'])
