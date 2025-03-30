import time
from stripsProblem import STRIPS_domain, Strips, Planning_problem
from stripsForwardPlanner import Forward_STRIPS
from searchMPP import SearcherMPP
from blocksworld import BlocksWorld

class Solver:
    @staticmethod
    def solve_without_heuristic(domain, initial_state, goal):
        problem = Planning_problem(domain.domain, initial_state, goal)
        start_time = time.time()
        SearcherMPP(Forward_STRIPS(problem)).search()
        end_time = time.time()
        print('---------------------------------------------------------------------------------------------')
        print(f"Time taken without heuristic: {end_time - start_time} seconds")
        print('---------------------------------------------------------------------------------------------')

    @staticmethod
    def solve_with_heuristic(domain, initial_state, goal):
        problem = Planning_problem(domain.domain, initial_state, goal)
        start_time = time.time()
        SearcherMPP(Forward_STRIPS(problem, heur=domain.heuristic)).search()
        end_time = time.time()
        print('---------------------------------------------------------------------------------------------')
        print(f"Time taken with heuristic: {end_time - start_time} seconds")
        print('---------------------------------------------------------------------------------------------')

    @staticmethod
    def solve_with_subgoal(domain, initial_state, subgoal1, subgoal2, goal, heuristic=False):
        start_time = time.time()

        subproblem1 = Planning_problem(
            domain.domain,
            initial_state,
            subgoal1,
        )

        subsolution1 = SearcherMPP(Forward_STRIPS(subproblem1)).search().end().assignment

        subproblem2 = Planning_problem(
            domain.domain,
            subsolution1,
            subgoal2,
        )

        subsolution2 = SearcherMPP(Forward_STRIPS(subproblem2)).search().end().assignment

        finalproblem = Planning_problem(
            domain.domain,
            subsolution2,
            goal
        )

        if heuristic:
            SearcherMPP(Forward_STRIPS(finalproblem, heur=domain.heuristic)).search()
        else:
            SearcherMPP(Forward_STRIPS(finalproblem)).search()

        end_time = time.time()

        if heuristic:
            print('---------------------------------------------------------------------------------------------')
            print(f"Time taken with heuristic and subgoals: {end_time - start_time} seconds")
            print('---------------------------------------------------------------------------------------------')
        else:
            print('---------------------------------------------------------------------------------------------')
            print(f"Time taken without heuristic but with subgoals: {end_time - start_time} seconds")
            print('---------------------------------------------------------------------------------------------')