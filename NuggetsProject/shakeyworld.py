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

initial_state = set_initial_state(
    ShakeyWorld().states,
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

goal = set_goal(
    'Ball1InRoomB',
    'Box1InRoomB',
    'RobotInRoomC',
    'RobotCarryingBall2'
)

problem = Planning_problem(
    ShakeyWorld().domain,
    initial_state,
    goal
)

SearcherMPP(Forward_STRIPS(problem)).search()
