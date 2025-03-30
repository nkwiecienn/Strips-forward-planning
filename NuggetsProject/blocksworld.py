import time

from stripsProblem import STRIPS_domain, Strips, Planning_problem
from stripsForwardPlanner import Forward_STRIPS
from searchMPP import SearcherMPP

class BlocksWorld:
    def __init__(self):
        self.boolean = [False, True]
        self.blocks = ['A', 'B', 'C', 'D', 'E', 'F']
        self.states = self.generate_domain_dict()
        self.domain = STRIPS_domain(
            self.states,
            self.generate_actions_dict(),
        )

    def generate_domain_dict(self):
        domain = {}
        for i in ['A', 'B', 'C']:
            name = i + 'OnTable'
            domain[name] = self.boolean
            name = i + 'InHand'
            domain[name] = self.boolean
            for j in ['A', 'B', 'C']:
                if i != j:
                    name = i + 'On' + j
                    domain[name] = self.boolean

        return domain

    @staticmethod
    def generate_actions_dict():
        actions = []

        # Pickup (from Table)
        for i in ['A', 'B', 'C']:
            actions.append(Strips(
                'PickUp' + i,
                {i + 'OnTable': True, **{k + 'InHand': False for k in ['A', 'B', 'C']},
                 **{k + 'On' + i: False for k in ['A', 'B', 'C'] if k != i}},
                {i + 'OnTable': False, i + 'InHand': True}
            ))

        # Put down (on Table)
        for i in ['A', 'B', 'C']:
            actions.append(Strips(
                'PutDown' + i,
                {i + 'InHand': True},
                {i + 'OnTable': True, i + 'InHand': False}
            ))

        # Unstack (from another block)
        for i in ['A', 'B', 'C']:
            for j in ['A', 'B', 'C']:
                if i != j:
                    actions.append(Strips(
                        'Unstack' + i + j,
                        {i + 'On' + j: True, **{k + 'InHand': False for k in ['A', 'B', 'C']},
                         **{k + 'On' + i: False for k in ['A', 'B', 'C'] if k != i}},
                        {i + 'On' + j: False, i + 'InHand': True}
                    ))

        # Stack (on another block)
        for i in ['A', 'B', 'C']:
            for j in ['A', 'B', 'C']:
                if i != j:
                    actions.append(Strips(
                        'Stack' + i + j,
                        {i + 'InHand': True, **{k + 'On' + j: False for k in ['A', 'B', 'C'] if k != j}},
                        {i + 'On' + j: True, i + 'InHand': False}
                    ))

        return actions

    @staticmethod
    def heuristic(state, goal):
        cost = 0

        for key in goal:
            if state.get(key) != goal[key]:
                block, position = key.split('On')
                if state.get(block + 'InHand', False):
                    continue
                if state.get(position + 'On' + block, False):
                    cost += 2
                else:
                    cost += 1

        return cost


def set_initial_state(states, *args):
    initial_state = {key: False for key in states}
    for arg in args:
        initial_state[arg] = True
    return initial_state

def set_goal(*args):
    goal = {}
    for arg in args:
        goal[arg] = True
    return goal

# Problem:
# C
# A B

# Goal:
# A
# B
# C

problem = Planning_problem(
    BlocksWorld().domain,
    set_initial_state(BlocksWorld().states, 'COnA', 'AOnTable', 'BOnTable'),
    set_goal('AOnB', 'BOnC', 'COnTable')
)

SearcherMPP(Forward_STRIPS(problem)).search()

start_time = time.time()
SearcherMPP(Forward_STRIPS(problem)).search()
end_time = time.time()
print(f"Time taken without heuristic: {end_time - start_time} seconds")

start_time = time.time()
SearcherMPP(Forward_STRIPS(problem, heur=BlocksWorld.heuristic)).search()
end_time = time.time()
print(f"Time taken with heuristic: {end_time - start_time} seconds")