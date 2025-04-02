import time
from stripsProblem import STRIPS_domain, Strips, Planning_problem
from stripsForwardPlanner import Forward_STRIPS
from searchMPP import SearcherMPP

class Hanoi:
    def __init__(self, num_of_blocks=3):
        self.boolean = [False, True]
        self.num_of_blocks = num_of_blocks
        self.blocks = self.generate_blocks_list(self.num_of_blocks)
        self.towers = ['Tower1', 'Tower2', 'Tower3']
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
            for tower in self.towers:
                name = i + 'On' + tower
                domain[name] = self.boolean
            name = i + 'InHand'
            domain[name] = self.boolean
            for j in self.blocks:
                if i < j:
                    name = i + 'On' + j
                    domain[name] = self.boolean

        return domain

    def generate_actions_dict(self):
        actions = []

        # Pickup (from Tower)
        for i in self.blocks:
            for tower in self.towers:
                actions.append(Strips(
                    'PickUp' + i + tower    ,
                    {i + 'On' + tower: True, **{k + 'InHand': False for k in self.blocks},
                 **{k + 'On' + i: False for k in self.blocks if k < i}},
                    {i + 'On' + tower: False, i + 'InHand': True}
                ))

        # Put down (on Tower)
        for i in self.blocks:
            for tower in self.towers:
                actions.append(Strips(
                    'PutDown' + i + tower,
                    {i + 'InHand': True, **{k + 'On' + tower: False for k in self.blocks}},
                    {i + 'On' + tower: True, i + 'InHand': False}
                ))

        # Unstack (from another block)
        for i in self.blocks:
            for j in self.blocks:
                if i < j:
                    actions.append(Strips(
                        'Unstack' + i + j,
                        {i + 'On' + j: True, **{k + 'InHand': False for k in self.blocks},
                        **{k + 'On' + i: False for k in self.blocks if k < i}},
                        {i + 'On' + j: False, i + 'InHand': True}
                    ))

        # Stack (on another block)
        for i in self.blocks:
            for j in self.blocks:
                if i < j:
                    actions.append(Strips(
                        'Stack' + i + j,
                        {i + 'InHand': True, **{k + 'On' + j: False for k in self.blocks if k < j}},
                        {i + 'On' + j: True, i + 'InHand': False}
                    ))

        return actions

    def set_initial_state(self):
        initial_state = {key: False for key in self.states}
        for i in range(self.num_of_blocks - 1):
            initial_state[self.blocks[i] + 'On' + self.blocks[i+1]] = True
        initial_state[self.blocks[-1] + 'OnTower1'] = True

        return initial_state

    def set_goal(self):
        goal = {}
        for i in range(self.num_of_blocks - 1):
            goal[self.blocks[i] + 'On' + self.blocks[i + 1]] = True
        goal[self.blocks[-1] + 'OnTower3'] = True

        return goal

    @staticmethod
    def set_subgoal(*args):
        goal = {}
        for arg in args:
            goal[arg] = True
        return goal
