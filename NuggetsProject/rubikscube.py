import time

from stripsProblem import STRIPS_domain, Strips, Planning_problem
from stripsForwardPlanner import Forward_STRIPS
from searchMPP import SearcherMPP

class RubiksCube:
    def __init__(self):
        self.values = [1, 2, 3, 4, 5, 6]
        self.positions = ['Position1', 'Position2', 'Position3', 'Position4', 'Position5', 'Position6']
        self.states = self.generate_domain_dict()
        self.domain = STRIPS_domain(
            self.states,
            self.generate_actions_dict(),
        )

    def generate_domain_dict(self):
        domain = {pos: [val] for pos, val in zip(self.positions, self.values)}
        return domain

    def generate_actions_dict(self):
        actions = []

        # (1 2 3 4) 5 6 --0--> (4 3 2 1) 5 6
        # 1 (2 3 4 5) 6 --1--> 1 (5 4 3 2) 6
        # 1 2 (3 4 5 6) --2--> 1 2 (6 5 4 3)

        for val1 in self.values:
            for val2 in self.values:
                for val3 in self.values:
                    for val4 in self.values:
                        if len({val1, val2, val3, val4}) == 4:
                            name = str(0) + 'turn' + str(val1) + str(val2) + str(val3) + str(val4)
                            actions.append(Strips(
                                name,
                                {'Position1': val1, 'Position2': val2, 'Position3': val3, 'Position4': val4},
                                {'Position1': val4, 'Position2': val3, 'Position3': val2, 'Position4': val1},
                            ))
                            name = str(1) + 'turn' + str(val1) + str(val2) + str(val3) + str(val4)
                            actions.append(Strips(
                                name,
                                {'Position2': val1, 'Position3': val2, 'Position4': val3, 'Position5': val4},
                                {'Position2': val4, 'Position3': val3, 'Position4': val2, 'Position5': val1},
                            ))
                            name = str(2) + 'turn' + str(val1) + str(val2) + str(val3) + str(val4)
                            actions.append(Strips(
                                name,
                                {'Position3': val1, 'Position4': val2, 'Position5': val3, 'Position6': val4},
                                {'Position3': val4, 'Position4': val3, 'Position5': val2, 'Position6': val1},
                            ))

        return actions

    @staticmethod
    def heuristic(state, goal):
        cost = 0
        for pos in state:
            if state[pos] != goal[pos]:
                cost += 1
        return cost

    def set_initial_state(self, *args):
        initial_state = {}

        for i in range(6):
            initial_state[self.positions[i]] = args[i]

        return  initial_state

    def set_goal(self, *args):
        goal = {}

        for i in range(6):
            goal[self.positions[i]] = args[i]

        return goal
