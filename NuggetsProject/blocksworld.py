import time
from stripsProblem import STRIPS_domain, Strips, Planning_problem
from stripsForwardPlanner import Forward_STRIPS
from searchMPP import SearcherMPP

class BlocksWorld:
    def __init__(self, num_of_blocks=3):
        self.boolean = [False, True]
        self.blocks = self.generate_blocks_list(num_of_blocks)
        self.states = self.generate_domain_dict()
        self.domain = STRIPS_domain(
            self.states,
            self.generate_actions_dict(),
        )

    @staticmethod
    def generate_blocks_list(num_of_blocks=3):
        return [chr(i) for i in range(65, 65 + num_of_blocks)]


    def generate_domain_dict(self):
        domain = {}
        for i in self.blocks:
            name = i + 'OnTable'
            domain[name] = self.boolean
            name = i + 'InHand'
            domain[name] = self.boolean
            for j in self.blocks:
                if i != j:
                    name = i + 'On' + j
                    domain[name] = self.boolean

        return domain

    def generate_actions_dict(self):
        actions = []

        # Pickup (from Table)
        for i in self.blocks:
            actions.append(Strips(
                'PickUp' + i,
                {i + 'OnTable': True, **{k + 'InHand': False for k in self.blocks},
                 **{k + 'On' + i: False for k in self.blocks if k != i}},
                {i + 'OnTable': False, i + 'InHand': True}
            ))

        # Put down (on Table)
        for i in self.blocks:
            actions.append(Strips(
                'PutDown' + i,
                {i + 'InHand': True},
                {i + 'OnTable': True, i + 'InHand': False}
            ))

        # Unstack (from another block)
        for i in self.blocks:
            for j in self.blocks:
                if i != j:
                    actions.append(Strips(
                        'Unstack' + i + j,
                        {i + 'On' + j: True, **{k + 'InHand': False for k in self.blocks},
                         **{k + 'On' + i: False for k in self.blocks if k != i}},
                        {i + 'On' + j: False, i + 'InHand': True}
                    ))

        # Stack (on another block)
        for i in self.blocks:
            for j in self.blocks:
                if i != j:
                    actions.append(Strips(
                        'Stack' + i + j,
                        {i + 'InHand': True, **{k + 'On' + j: False for k in self.blocks if k != j}},
                        {i + 'On' + j: True, i + 'InHand': False}
                    ))

        return actions

    def heuristic(self, state, goal):
        cost = 0

        for key in goal:
            if state.get(key) != goal[key]:
                if 'On' in key:
                    top, bottom = key.split('On')
                    for block in self.blocks:
                        if block != top and state[block + 'On' + top]:
                            cost += 1
                            break
                    cost += 1

        return cost


    def set_initial_state(self, *args):
        initial_state = {key: False for key in self.states}
        for arg in args:
            initial_state[arg] = True
        return initial_state

    @staticmethod
    def set_goal(*args):
        goal = {}
        for arg in args:
            goal[arg] = True
        return goal
