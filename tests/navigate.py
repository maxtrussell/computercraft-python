from cc import import_file, fs

nav = import_file('/lib/nav.py')
schematic_driver = import_file('/lib/schematic.py')
dig = import_file('/lib/dig.py')

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

turtle.dir(nav.DIRS.UP)
test('Expected State: [0,1,1], NORTH')

turtle.dir(nav.DIRS.DOWN)
test('Expected State: [0,1,0], NORTH')

turtle.turn(nav.TURNS.LEFT)
test('Expected State: [0,1,0], WEST')

turtle.turn_to(nav.CARDINALS.SOUTH)
test('Expected State: [0,1,0], SOUTH')

turtle.turn_to(nav.CARDINALS.NORTH)
test('Expected State: [0,1,0], NORTH')

turtle.dir(nav.DIRS.FORWARD, 5)
test('Expected State: [0,6,0], NORTH')

turtle.turn_to(nav.CARDINALS.EAST)
test('Expected State: [0,6,0], EAST')

turtle.dir(nav.DIRS.FORWARD, 5)
test('Expected State: [5,6,0], EAST')

turtle.go_to([0,0,0])
turtle.turn_to(nav.CARDINALS.NORTH)
