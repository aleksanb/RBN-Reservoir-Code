from tools import Mixin
import random


def full_generational_replacement():
    def fn(adults, children, adult_pool_size):
        new_adults = children
        return new_adults
    return Mixin('full_generational_replacement', fn)


def over_production():
    def fn(adults, children, adult_pool_size):
        new_adults = random.sample(children, adult_pool_size)
        return new_adults
    return Mixin('over_production', fn)


def generational_mixing():
    def fn(adults, children, adult_pool_size):
        new_adults = random.sample(children + adults, adult_pool_size)
        return new_adults
    return Mixin('generational_mixing', fn)
