from cc import import_file, turtle

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

navigator = nav.Navigator()

# add fuel source to VALUABLES
for k,v in fuel.FUEL.items():
        VALUABLES[k] = v

# start bottom front left
def quarry(width, depth, height, valuables=False, go_down=False, go_home=False):
        # get direction z
        zdir = nav.DIRS.DOWN if go_down else nav.DIRS.UP

        # axis one direction changes
        directions = [nav.TURNS.LEFT, nav.TURNS.RIGHT]
        direction_index = 1
        navigator.force_dir(nav.DIRS.FORWARD)
        for i in range(height):
                for j in range(width):
                        for k in range(depth - 1):
                                manage_inv(valuables)
                                navigator.force_dir(nav.DIRS.FORWARD)

                        # finished diggin one row
                        # reposition to dig second row
                        if j != (width - 1):
                                # choose direction
                                direction = directions[direction_index] 

                                # turn to next row
                                navigator.turn(direction)
                                manage_inv(valuables)
                                navigator.force_dir(nav.DIRS.FORWARD)
                                navigator.turn(direction)

                                # change direction
                                direction_index = (direction_index + 1) % 2
                                
                # reset in next level
                if i != (height - 1):
                        manage_inv(valuables)
                        navigator.force_dir(zdir)
                        navigator.turn(nav.TURNS.LEFT)
                        navigator.turn(nav.TURNS.LEFT)
	if go_home:
		navigator.go_to([0,0,0])
		navigator.turn_to(nav.CARDINALS.NORTH)

# drops all non valuable items and condenses inventory when full
def manage_inv(valuables):
        if valuables and inv.is_full():
                inv.drop_all_except(VALUABLES)
                inv.restack()
