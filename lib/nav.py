from enum import Enum, IntEnum
from cc import gps, import_file, turtle

fuel = import_file('/lib/fuel.py')

class GpsLocationException(Exception):
    pass

class DIRS(Enum):
    UP='UP'
    DOWN='DOWN'
    FORWARD='FORWARD'

    DIG='DIG'
    MOVE='MOVE'
    TURN='TURN'

class TURNS(Enum):
    LEFT='LEFT'
    RIGHT='RIGHT'

class AXIS(IntEnum):
    X=0
    Y=1
    Z=2

class CARDINALS(IntEnum):
    NORTH=0  # negative Z
    EAST=1   # postive X
    SOUTH=2  # positive Z
    WEST=3   # negative X

class OPS(Enum):
    MOVE=1
    DIG=2
    TURN=3

ACTIONS = {
    OPS.MOVE: {
        DIRS.UP:turtle.up,
        DIRS.DOWN:turtle.down,
        DIRS.FORWARD:turtle.forward,
    },
    OPS.DIG: {
        DIRS.UP:turtle.digUp,
        DIRS.DOWN:turtle.digDown,
        DIRS.FORWARD:turtle.dig,
    },
    OPS.TURN: {
        TURNS.LEFT:turtle.turnLeft,
        TURNS.RIGHT:turtle.turnRight,
    },
}

# destructively move n blocks
def force_dir(dir, n=1):
    for i in range(n):
        ACTIONS[OPS.DIG][dir]()

        while True:
            # keep trying until success
            # used to deal w/falling gravel etc.
            fuel.fuel()
            if ACTIONS[OPS.MOVE][dir]():
                break
            ACTIONS[OPS.DIG][dir]()

# move n blocks
def dir(dir, n=1):
    for i in range(n):
        fuel.fuel()
        if not ACTIONS[OPS.MOVE][dir]():
            return False
    return True

# turn a by a given direction
def turn(turn_dir):
    ACTIONS[OPS.TURN][turn_dir]()

def get_bearing():
    initial_pos = None
    for i in range(4):
        if turtle.inspect() is None:
            initial_pos = gps.locate()
            if initial_pos is None:
                raise GpsLocationException(
                    'Could not establish connection. Is a modem attached?'
                )
            fuel.fuel()
            turtle.forward()
            break
        turtle.turnRight()
    else:
        raise GpsLocationException(
            'Could not get bearing, are there any open blocks around the turtle?'
        )

    dx, _, dz = map(lambda x: x[0]-x[1], zip(gps.locate(), initial_pos))
    turtle.back()
    if abs(dx) > 0:
        return CARDINALS.EAST if dx > 0 else CARDINALS.WEST
    else:
        return CARDINALS.SOUTH if dz > 0 else CARDINALS.NORTH

class Navigator:
    def __init__(self, location=None, direction=CARDINALS.NORTH):
        self.location = location if location is not None else [0,0,0]
        self.direction=direction

    ### SETTERS
    # change location depending on given direction
    def set_location(self, dir):
        if dir == DIRS.UP:
            axis = 2
            direction = 1
        elif dir == DIRS.DOWN:
            axis = 2
            direction = -1
        else:
            axis = 0 if self.direction % 2 else 1
            direction = - 1 if self.direction > 1 else 1
        self.location[axis]+=direction

    # change direction given a turn direction
    def set_direction(self, turn_dir):
        turn_dir = -1 if turn_dir == TURNS.LEFT else 1
        self.direction = CARDINALS((self.direction + turn_dir) % 4)

    ## MOVERS
    # move in the given direction
    def dir(self, move_dir, n=1, callback=None):
        for i in range(n):
            if callback:
                callback[0](*callback[1:])
            if not dir(move_dir):
                return False
            self.set_location(move_dir)
        return True

    # force move
    def force_dir(self, move_dir, n=1, callback=None):
        for i in range(n):
            if callback:
                callback[0](*callback[1:])
            force_dir(move_dir)
            self.set_location(move_dir)

    ## TURNERS
    # turn RIGHT or LEFT
    def turn(self, turn_dir):
        turn(turn_dir)
        self.set_direction(turn_dir)

    # turn to cardinal
    def turn_to(self, target):
        right_turns = (target - self.direction) % 4
        left_turns = (self.direction - target) % 4
        turn_dir = TURNS.RIGHT if right_turns < left_turns else TURNS.LEFT
        for _ in range(min(right_turns, left_turns)):
            self.turn(turn_dir)

    ## PATHERS
    # move once in any direction
    def step(self, axis, direction, n=1, callback=None, force=False):
        move = self.force_dir if force else self.dir

        if axis == 2:
            move_dir = {1:DIRS.UP, -1:DIRS.DOWN}
            move(move_dir[direction], n, callback)
        else:
            if axis:
                target_cardinal = 0 if direction == 1 else 2
            else:
                target_cardinal = 1 if direction == 1 else 3

            initial_cardinal = self.direction
            self.turn_to(target_cardinal)
            move(DIRS.FORWARD, n, callback)
            self.turn_to(initial_cardinal)

    def pathing_brute(self, target, callback=None, preferred_axis=0):

        while(self.location != target):
            difference = [a-b for a,b in zip(target, self.location)]
            direction = [1 if x > 0 else -1 for x in difference]

            for i in range(3):
                axis = preferred_axis + i % 3
                if difference[axis]:
                    self.step(axis, direction[axis], abs(difference[axis]), callback, False)

    def go_to(self, target, callback=False):
        self.pathing_brute(target, callback)
