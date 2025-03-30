import time
from stripsProblem import STRIPS_domain, Strips, Planning_problem
from stripsForwardPlanner import Forward_STRIPS
from searchMPP import SearcherMPP

class Dinner:
    def __init__(self):
        self.boolean = [False, True]
        self.domain = STRIPS_domain(
            {
                'clean': self.boolean,
                'quiet': self.boolean,
                'garbage': self.boolean,
                'dinner': self.boolean,
                'present': self.boolean,
            },
            {
                Strips('cook', {'clean': True}, {'dinner': True}),
                Strips('wrap', {'quiet': True}, {'present': True}),
                Strips('carry', {'garbage': True}, {'garbage': False, 'clean': False}),
                Strips('dolly', {'garbage': True}, {'garbage': False, 'quiet': False}),
            }
        )

    @staticmethod
    def heuristic(state, goal):
        return sum(1 for key in goal if state.get(key) != goal[key])


problem1 = Planning_problem(
    Dinner().domain,
    {'clean': True, 'quiet': True, 'garbage': True, 'present': False, 'dinner': False},
    {'present': True, 'dinner': True, 'garbage': False, 'clean': True},
)

start_time = time.time()
SearcherMPP(Forward_STRIPS(problem1)).search()
end_time = time.time()
print(f"Time taken without heuristic: {end_time - start_time} seconds")

start_time = time.time()
SearcherMPP(Forward_STRIPS(problem1, heur=Dinner.heuristic)).search()
end_time = time.time()
print(f"Time taken with heuristic: {end_time - start_time} seconds")
