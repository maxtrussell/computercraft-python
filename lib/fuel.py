from cc import import_file, turtle
inv = import_file('/lib/inv.py')

# TODO: add blaze rods, bamboo, kelp, etc.
FUEL = {
	'minecraft:coal': 80,
	'minecraft:charcoal': 80,
	'minecraft:oak_planks': 15,
}

# refuel a turtle if necessary
# returns false if out of fuel
def fuel(threshold=80):
	initial_slot = turtle.getSelectedSlot()
	while turtle.getFuelLevel() < threshold:
		# select fuel
		if not inv.select_from_dict(FUEL):
			return false
		turtle.refuel(1)

	turtle.select(initial_slot)
	return true
