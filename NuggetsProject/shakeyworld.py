import time

from stripsProblem import STRIPS_domain, Strips, Planning_problem
from stripsForwardPlanner import Forward_STRIPS
from searchMPP import SearcherMPP

class ShakeyWorld:
    def __init__(self):
        self.boolean = [False, True]
        self.rooms = ['RoomA', 'RoomB', 'RoomC']
        self.balls = ['Ball1', 'Ball2', 'Ball3']
        self.boxes = ['Box1', 'Box2', 'Box3']
        self.states = self.generate_domain_dict()
        self.domain = STRIPS_domain(
            self.states,
            self.generate_actions_dict(),
        )

    def generate_domain_dict(self):
        domain = {}

        # Robot/balls/boxes can be in one of three rooms
        for room in self.rooms:
            name = 'RobotIn' + room
            domain[name] = self.boolean
            for box in self.boxes:
                name = box + 'In' + room
                domain[name] = self.boolean
            for ball in self.balls:
                name = ball + 'In' + room
                domain[name] = self.boolean

            # Adjacent rooms
            for room2 in self.rooms:
                if room2 != room:
                    name = room + 'Adj' + room2
                    domain[name] = self.boolean
                    name = room2 + 'Adj' + room
                    domain[name] = self.boolean

            # Lights can be on or off
            name = 'LightOn' + room
            domain[name] = self.boolean

        # Robot can have an empty hand or not
        domain['HandEmpty'] = self.boolean

        # Robot can carry a ball

        for ball in self.balls:
            name = 'RobotCarrying' + ball
            domain[name] = self.boolean

        return domain


    def generate_actions_dict(self):
        actions = []

        # Pick up a ball - hand empty and robot and ball in the same room
        for ball in self.balls:
            for room in self.rooms:
                actions.append(Strips(
                    'PickUp' + ball + 'From' + room,
                    {'HandEmpty': True, ball + 'In' + room: True, 'RobotIn' + room: True},
                    {'HandEmpty': False, 'RobotCarrying' + ball: True, ball + 'In' + room: False},
                ))

        # Put down a ball - robot carrying ball and puts the ball down where it is
        for ball in self.balls:
            for room in self.rooms:
                actions.append(Strips(
                    'PutDown' + ball + 'In' + room,
                    {'RobotCarrying' + ball: True, 'RobotIn' + room: True},
                    {'HandEmpty': True, 'RobotCarrying' + ball: False, ball + 'In' + room: True},
                ))

        # Push box - rooms have to be adjacent, robot and box are in the same place and light has to be on
        for box in self.boxes:
            for room1 in self.rooms:
                for room2 in self.rooms:
                    if room2 != room1:
                        actions.append(Strips(
                            'Push' + box + 'From' + room1 + 'To' + room2,
                            {room1 + 'Adj' + room2: True, 'RobotIn' + room1: True, box + 'In' + room1: True, 'LightOn' + room1: True},
                            {'RobotIn' + room1: False, 'RobotIn' + room2: True, box + 'In' + room1: False, box + 'In' + room2: True},
                        ))

        # Move rooms - rooms have to be adjacent, robot is in first room and the light is on
        for room1 in self.rooms:
            for room2 in self.rooms:
                if room2 != room1:
                    actions.append(Strips(
                        'MoveFrom' + room1 + 'To' + room2,
                        {room1 + 'Adj' + room2: True, 'RobotIn' + room1: True, 'LightOn' + room1: True},
                        {'RobotIn' + room1: False, 'RobotIn' + room2: True},
                    ))


        # Turn on - light has to be off and robot is in the room and has empty hand
        for room in self.rooms:
            actions.append(Strips(
                'TurnLightOn' + room,
                {'LightOn' + room: False, 'RobotIn' + room: True, 'HandEmpty': True},
                {'LightOn' + room: True},
            ))

        return actions

    @staticmethod
    def heuristic(state, goal):
        def distance(pos1, pos2):
            room_positions = {'RoomA': 0, 'RoomB': 1, 'RoomC': 2}
            return abs(room_positions[pos1] - room_positions[pos2])

        cost = 0

        for key in goal:
            if state.get(key) != goal[key]:
                if 'In' in key or 'RobotIn' in key:
                    item, goal_room = key.split('In')
                    for room in state:
                        if state[room] and room.startswith(f'{item}In'):
                            current_room = room.replace(f'{item}In', '')
                            cost += distance(current_room, goal_room)
                            break

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


# +----------------+   +----------------+   +----------------+
# |     RoomA      |   |     RoomB      |   |     RoomC      |
# |                |   |                |   |                |
# |  Robot         |   |                |   |                |
# |  Ball1         |   |  Ball2         |   |  Ball3         |
# |  Box1          |   |  Box2          |   |  Box3          |
# |  Light: OFF    |   |  Light: ON     |   |  Light: ON     |
# +----------------+   +----------------+   +----------------+
#         ||                    ||                    ||
#    Adjacent to B         Adjacent to A,C       Adjacent to B

initial_state = ShakeyWorld().set_initial_state(
    'RobotInRoomA',
    'HandEmpty',
    'Ball1InRoomA',
    'Ball2InRoomB',
    'Ball3InRoomC',
    'Box1InRoomA',
    'Box2InRoomB',
    'Box3InRoomC',
    'RoomAAdjRoomB', 'RoomBAdjRoomA',
    'RoomBAdjRoomC', 'RoomCAdjRoomB',
    'LightOnRoomB',
    'LightOnRoomC'
)

# +----------------+   +----------------+   +----------------+
# |     RoomA      |   |     RoomB      |   |     RoomC      |
# |                |   |                |   |                |
# |                |   |                |   | Robot          |
# |                |   |  Ball1         |   | Ball 2 in hand |
# |                |   |  Box1          |   |                |
# |                |   |                |   |                |
# +----------------+   +----------------+   +----------------+

goal1 = ShakeyWorld().set_goal(
    'Ball1InRoomB',
    'Box1InRoomB',
    'RobotInRoomC',
    'RobotCarryingBall2'
)

problem1 = Planning_problem(
    ShakeyWorld().domain,
    initial_state,
    goal1
)

print("--------------------------------------TASKS 1------------------------------------------------------------")

start_time = time.time()
SearcherMPP(Forward_STRIPS(problem1)).search()
end_time = time.time()
print(f"Time taken without heuristic: {end_time - start_time} seconds")

start_time = time.time()
SearcherMPP(Forward_STRIPS(problem1, heur=ShakeyWorld.heuristic)).search()
end_time = time.time()
print(f"Time taken with heuristic: {end_time - start_time} seconds")

print("--------------------------------------TASKS 2------------------------------------------------------------")

start_time = time.time()

subgoal1 = ShakeyWorld().set_goal(
    'RobotInRoomA',
    'RobotCarryingBall1',
    'LightOnRoomA'
)

subgoal2 = ShakeyWorld().set_goal(
    'RobotInRoomB',
    'Box1InRoomB',
    'RobotCarryingBall2'
)

subproblem1 = Planning_problem(
    ShakeyWorld().domain,
    initial_state,
    subgoal1,
)

subsolution1 = SearcherMPP(Forward_STRIPS(subproblem1)).search().end().assignment

subproblem2 = Planning_problem(
    ShakeyWorld().domain,
    subsolution1,
    subgoal2
)

subsolution2 = SearcherMPP(Forward_STRIPS(subproblem2)).search().end().assignment

finalproblem = Planning_problem(
    ShakeyWorld().domain,
    subsolution2,
    goal1
)

finalsolution = SearcherMPP(Forward_STRIPS(finalproblem)).search()

end_time = time.time()
print(f"Time taken without heuristic but with subgoals: {end_time - start_time} seconds")

start_time = time.time()

subgoal1 = ShakeyWorld().set_goal(
    'RobotInRoomA',
    'RobotCarryingBall1',
    'LightOnRoomA'
)

subgoal2 = ShakeyWorld().set_goal(
    'RobotInRoomB',
    'Box1InRoomB',
    'RobotCarryingBall2'
)

subproblem1 = Planning_problem(
    ShakeyWorld().domain,
    initial_state,
    subgoal1,
)

subsolution1 = SearcherMPP(Forward_STRIPS(subproblem1, heur=ShakeyWorld.heuristic)).search().end().assignment

subproblem2 = Planning_problem(
    ShakeyWorld().domain,
    subsolution1,
    subgoal2
)

subsolution2 = SearcherMPP(Forward_STRIPS(subproblem2, heur=ShakeyWorld.heuristic)).search().end().assignment

finalproblem = Planning_problem(
    ShakeyWorld().domain,
    subsolution2,
    goal1
)

SearcherMPP(Forward_STRIPS(finalproblem, heur=ShakeyWorld.heuristic)).search()

end_time = time.time()
print(f"Time taken with heuristic and subgoals: {end_time - start_time} seconds")