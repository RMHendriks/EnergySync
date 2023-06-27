from code.algorithms.algorithm import Algorithm
from code.algorithms.random import Random
from code.algorithms.greedy_shared import GreedyShared
from code.algorithms.greedy_beam_search import GreedyBeamSearch
from code.algorithms.evolution import Evolution
from code.classes.program import Program

if __name__ == "__main__":

    ITERATIONS = 1
    NEIGHBOURHOOD = "1"
    ALGORITHM: Algorithm = Evolution

    program = Program("1", ITERATIONS, ALGORITHM)
    program.run()
