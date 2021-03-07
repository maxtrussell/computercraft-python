from enum import Enum
from cc import import_file,turtle
fuel = import_file('/lib/refuel.py')

class DIRS(Enum):
	UP='UP',
	DOWN='DOWN',
	FORWARD='FORWARD',

class OPS(Enum):
	DIG='DIG',
	MOVE='MOVE',

ACTIONS = {
	Operation.MOVE: {
		'UP':turtle.up,
		'DOWN':turtle.down,
		'FORWARD':turtle.forward,
	},
	Operation.DIG: {
		'UP':turtle.digUp,
		'DOWN':turtle.digDown,
		'FORWARD':turtle.dig,
	}
}

# destructively more n blocks
def force_dir(dir, n=1):
	for i in range(n):
		ACTIONS[Operation.DIG][dir]()

		while True:
			# keep trying until success
			# used to deal w/falling gravel etc.
			fuel.refuel()
			if ACTIONS[OPS.MOVE][dir]():
				break
			ACTIONS[OPS.DIG][dir]()
