from blocksworld import BlocksWorld
from rubikscube import RubiksCube
from shakeyworld import ShakeyWorld
from hanoi import Hanoi
from solver import Solver

print('---------------------------------------------------------------------------------------')
print('-----------------------------BLOCKS WORLD----------------------------------------------')
print('---------------------------------------------------------------------------------------')

blocks = BlocksWorld(6)

initial_state = blocks.set_initial_state(
    'COnD',
    'DOnA',
    'AOnTable',
    'EOnB',
    'BOnTable',
    'FOnTable'
)

# C
# D E
# A B F

goal = blocks.set_goal(
    'FOnTable',
    'EOnF',
    'DOnE',
    'COnD',
    'BOnC',
    'AOnB'
)

# A
# B
# C
# D
# E
# F

Solver.solve_without_heuristic(blocks, initial_state, goal)
Solver.solve_with_heuristic(blocks, initial_state, goal)

subgoal1 = blocks.set_goal(
    'FOnTable',
    'EOnF',
    'COnB',
)

subgoal2 = blocks.set_goal(
    'DOnE',
    'COnD',
)

Solver.solve_with_subgoal(blocks, initial_state, subgoal1, subgoal2, goal, False)
Solver.solve_with_subgoal(blocks, initial_state, subgoal1, subgoal2, goal, True)

print('-----------------------------RUBIKS CUBE----------------------------------------------')
print('---------------------------------------------------------------------------------------')

cube = RubiksCube()
initial_state = cube.set_initial_state(4, 5, 2, 3, 1, 6)
goal = cube.set_goal(1, 2, 3, 4, 5, 6)

Solver.solve_without_heuristic(cube, initial_state, goal)
Solver.solve_with_heuristic(cube, initial_state, goal)

subgoal1 = cube.set_goal(1, 6, 2, 3, 4, 5)
subgoal2 = cube.set_goal(1, 4, 5, 6, 2, 3)

Solver.solve_with_subgoal(cube, initial_state, subgoal1, subgoal2, goal, False)
Solver.solve_with_subgoal(cube, initial_state, subgoal1, subgoal2, goal, True)

print('-----------------------------SHAKEY WORLD----------------------------------------------')
print('---------------------------------------------------------------------------------------')

shakey = ShakeyWorld()

initial_state = shakey.set_initial_state(
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
# |  Robot         |   |                |   |                |
# |  Ball1         |   |  Ball2         |   |  Ball3         |
# |  Box1          |   |  Box2          |   |  Box3          |
# |  Light: OFF    |   |  Light: ON     |   |  Light: ON     |
# +----------------+   +----------------+   +----------------+
#         ||                    ||                    ||
#    Adjacent to B         Adjacent to A,C       Adjacent to B

goal = shakey.set_goal(
    'Ball1InRoomB',
    'Box1InRoomB',
    'RobotInRoomC',
    'RobotCarryingBall2'
)

# +----------------+   +----------------+   +----------------+
# |     RoomA      |   |     RoomB      |   |     RoomC      |
# |                |   |                |   |                |
# |                |   |                |   | Robot          |
# |                |   |  Ball1         |   | Ball 2 in hand |
# |                |   |  Box1          |   |                |
# |                |   |                |   |                |
# +----------------+   +----------------+   +----------------+

Solver.solve_without_heuristic(shakey, initial_state, goal)
Solver.solve_with_heuristic(shakey, initial_state, goal)

subgoal1 = shakey.set_goal(
    'RobotInRoomA',
    'RobotCarryingBall1',
    'LightOnRoomA'
)

subgoal2 = shakey.set_goal(
    'RobotInRoomB',
    'Box1InRoomB',
    'RobotCarryingBall2'
)

Solver.solve_with_subgoal(shakey, initial_state, subgoal1, subgoal2, goal, False)
Solver.solve_with_subgoal(shakey, initial_state, subgoal1, subgoal2, goal, True)

print('-----------------------------HANOI TOWER 4 (20+ STEPS)---------------------------------')
print('---------------------------------------------------------------------------------------')

hanoi4 = Hanoi(4)
initial_state = hanoi4.set_initial_state()
goal = hanoi4.set_goal()

Solver.solve_without_heuristic(hanoi4, initial_state, goal)

subgoal1 = hanoi4.set_subgoal(
    'AOnD',
    'DOnTower1',
    'COnTower2',
    'BOnTower3'
)

subgoal2 = hanoi4.set_subgoal(
    'AOnD',
    'BOnTower1',
    'COnTower2',
    'DOnTower3'
)

Solver.solve_with_subgoal(hanoi4, initial_state, subgoal1, subgoal2, goal, False)

print('-----------------------------HANOI TOWER 5 (20+ STEPS)---------------------------------')
print('---------------------------------------------------------------------------------------')

hanoi5 = Hanoi(5)
initial_state = hanoi5.set_initial_state()
goal = hanoi5.set_goal()

Solver.solve_without_heuristic(hanoi5, initial_state, goal)

subgoal1 = hanoi5.set_subgoal(
    'AOnB',
    'BOnC',
    'COnD',
    'DOnTower2',
    'EOnTower1'
)

subgoal2 = hanoi5.set_subgoal(
    'AOnB',
    'BOnC',
    'COnTower1',
    'DOnTower2',
    'EOnTower3'
)

Solver.solve_with_subgoal(hanoi5, initial_state, subgoal1, subgoal2, goal, False)