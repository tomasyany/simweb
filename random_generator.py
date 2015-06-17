from numpy import random

class RandomTime(object):
    # This class is used to generate random numbers following a defined distribution
    def __init__(self,distribution, parameters):
        self.dist = distribution
        self.params = parameters

    def getInstance(self):
        dist = self.dist
        p = self.params
        if dist == 'exponential':
            return random.exponential(p[0])
        elif dist == 'normal':
            return random.normal(p[0],p[1])
        elif dist == 'uniform':
            return random.uniform(p[0],p[1])
        elif dist == 'poisson':
            return random.poisson(p[0])
        elif dist == 'binomial':
            return random.binomial(p[0],p[1])
        elif dist == 'geometric':
            return random.geometric(p[0])
        elif dist == 'weibull':
            return random.weibull(p[0])
        elif dist == 'gamma':
            return random.gamma(p[0],p[1])
        elif dist == 'beta':
            return random.beta(p[0],p[1])
        elif dist == 'lognormal':
            return random.lognormal(p[0],p[1])