from enum import Enum, IntEnum
from cc import import_file, turtle

nav = import_file('/lib/nav.py')

class AXIS(IntEnum):
    X=1
    Y=2
    Z=3

class CARDINALS(Enum):
    NORTH='NORTH'
    EAST='EAST'
    SOUTH='SOUTH'
    WEST='WEST'

# maps a movement direction to an axis
DIRS_TO_AXIS = {
    nav.DIRS.UP:AXIS.Z,
    nav.DIRS.DOWN:AXIS.Z,
    nav.DIRS.FORWARD: {
        # axis depends on the cardinal direction the turtle is currently facing
        CARDINALS.NORTH:AXIS.Y,
        CARDINALS.EAST:AXIS.X,
        CARDINALS.SOUTH:AXIS.Y,
        CARDINALS.WEST:AXIS.X,
    },
}

# Maps current cardinal direction and a turn to a new cardinal direction
TURN_TO_DIR = {
        CARDINALS.NORTH: {
                nav.TURNS.LEFT:CARDINALS.WEST,
                nav.TURNS.RIGHT:CARDINALS.EAST,
        },
        CARDINALS.EAST: {
                nav.TURNS.LEFT:CARDINALS.NORTH,
                nav.TURNS.RIGHT:CARDINALS.SOUTH,
        },
        CARDINALS.SOUTH: {
                nav.TURNS.LEFT:CARDINALS.EAST,
                nav.TURNS.RIGHT:CARDINALS.WEST,
        },
        CARDINALS.WEST: {
                nav.TURNS.LEFT:CARDINALS.SOUTH,
                nav.TURNS.RIGHT:CARDINALS.NORTH,
        },
}


class Navigator:
    def __init__(self, location=[0,0,0], direction=CARDINALS.NORTH):
        self.location = location
        self.direction = direction

    # change location depending on given movement direction
    def set_location(self, dir):
        axis = DIRS_TO_AXIS[dir]
        if axis is dict:
            # movement direction is forward, axis depends on current cardinal direction
            axis = axis[self.direction]
        self.location[axis]+=1

    # change direction given a turn direction i.e. LEFT, RIGHT
    def set_direction(self, turn_dir):
        self.direction = TURN_TO_DIR[self.direction][turn_dir]

    # move in the given movement direction
    def dir(self, dir, n=1):
        for i in range(n):
            if not nav.dir(dir)
                return False
            self.set_location(dir)

    # turn RIGHT or LEFT
    def turn(self turn_dir):
        nav.turn(turn_dir)
        self.set_direction(turn_dir)

    def turn_to(self, cardinal):
        if self.direction == cardinal:
            return
        if DIRS_TO_AXIS[nav.DIRS.FORWARD][self.direction] == DIRS_TO_AXIS[nav.DIRS.FORWARD][cardinal]:
            # change axis to be different then desired axis
            self.turn(nav.TURNS.LEFT)
        # turn to face desired cardinal location
        self.turn(nav.TURNS.LEFT) if TURN_TO_DIR[self.direction][nav.TURNS.LEFT] == cardinal else self.turn(nav.TURNS.RIGHT)
