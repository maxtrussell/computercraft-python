from cc import import_file
nav = import_file('/lib/nav.py')
fuel = import_file('/lib/fuel.py')
inv = import_file('/lib/inv.py')

VALUABLES = {
	'minecraft:iron_ore':True,
	'minecraft:gold_ore':True,
	'minecraft:diamond':True,
	'minecraft:emerald':True,
	'minecraft:lapis_lazuli':True,
}

# add fuel source to VALUABLES
for k,v in fuel.items():
	VALUABLES[k] = v

# start bottom front left
def quarry(width, depth, height, valuables=False, go_down=False):
	# get direction z
	if go_down:
		move_z = turtle.down
	else:
		move_z = turtle.up
        # axis one direction changes
        directions = [turtle.left, turtle.right]
        directionIndex = 1
        turtle.forward()
        for i in range(height):
                for j in range(width):
                        for k in range(depth - 1):
                                manage_inv(VALUABLES)
				nav.force_dir(nav.DIRS.FORWARD)

                        # finished diggin one row
                        # reposition to dig second row
                        if j != (width - 1):
                                # choose direction
                                changeDirection = directions[directionIndex] 

                                # turn to next row
                                changeDirection()
                                manage_inv(VALUABLES)
				nav.force_dir(nav.DIRS.FORWARD)
                                changeDirection()

                                # change direction
                                directionIndex = (directionIndex + 1) % 2
                
                # reset in next level
                if i != (height - 1):
			manage_inv(VALUABLES)
			move_z()
			turtle.left()
                        turtle.left()

# drops all non valuable items and condenses inventory when full
def manage_inv(valuables):
	if valuables and inv.is_full():
		inv.drop_all_except(VALUABLES)
		inv.restack()
