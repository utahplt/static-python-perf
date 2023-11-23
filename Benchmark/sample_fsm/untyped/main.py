import time

from Utilities import relative_average
from Other import build_random_population

def run():
    simulation_to_lines(evolve(build_random_population(100), 10, 2, 1))
    return

def evolve(p, c, s, r):
    """
    Computes the list of average payoffs over the evolution of population
    p for c cycles of match_ups with r rounds per match and at birth/death
    rate of s
    :param p: Population
    :param c: Natural
    :param s: Natural
    :param r: Natural
    :return: [Float]
    """
    payoffs = []
    for i in range(c):
        p2 = p.match_up(r)
        pp = p2.payoffs()
        p3 = p2.regenerate(s)
        payoffs = payoffs + [relative_average(pp, r)]
        p = p3

    return payoffs

def simulation_to_lines(data):
    """
    Turn average payoffs into a list of Cartesian points
    :param data: [Payoffs]
    :return: None
    """
    result = []
    counter = 0
    for payoff in data:
        result = result + [(counter, payoff)]
        counter+=1
    return result

    #print(str(result))
start_time = time.time()

for i in range(100):
    run()

end_time = time.time()
runtime = end_time - start_time
print(runtime)