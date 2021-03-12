from cc import import_file

nav = import_file('/lib/nav.py')

# test for navigator

# ignore arguments

turtle = nav.Navigator()

def test(msg = 'State:'):
    print(msg)
    print('Location: ', turtle.location)
    print('Direction: ', turtle.direction)
    print('-------------------------------\n')

test('Initial State:')

turtle.dir(nav.DIRS.FORWARD)
test('Expected State: [0,1,0], NORTH')
input()

turtle.dir(nav.DIRS.UP)
test('Expected State: [0,1,1], NORTH')
input()

turtle.dir(nav.DIRS.DOWN)
test('Expected State: [0,1,0], NORTH')
input()

turtle.turn(nav.TURNS.LEFT)
test('Expected State: [0,1,0], WEST')
input()

turtle.turn_to(nav.CARDINALS.SOUTH)
test('Expected State: [0,1,0], SOUTH')
input()

turtle.turn_to(nav.CARDINALS.NORTH)
test('Expected State: [0,1,0], NORTH')
input()

turtle.dir(nav.DIRS.FORWARD, 5)
test('Expected State: [0,6,0], NORTH')
input()

turtle.turn_to(nav.CARDINALS.EAST)
test('Expected State: [0,6,0], EAST')
input()

turtle.dir(nav.DIRS.FORWARD, 5)
test('Expected State: [5,6,0], EAST')
input()

print(turtle.go_to([0,0,0]))
