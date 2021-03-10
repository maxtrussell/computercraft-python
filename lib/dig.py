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

# add fuel source to VALUABLES
for k,v in fuel.FUEL.items():
        VALUABLES[k] = v

# start bottom front left
# do is list of a function and its arguments to execute after every movement
def quarry(width, depth, height, valuables=False, go_down=False, go_home=False, do=None):
        navigator = nav.Navigator()
        initial_location = navigator.get_location()
        initial_direction = navigator.get_direction()
        # get direction z
        zdir = nav.DIRS.DOWN if go_down else nav.DIRS.UP

        # pack do
        do = [do_wrapper, [[manage_inv, valuables][do[0],d[1]]]] if do else [do_wrapper, [[manage_inv, valuables]]]

        # axis one direction changes
        directions = [nav.TURNS.LEFT, nav.TURNS.RIGHT]
        direction_index = 1
        navigator.force_dir(nav.DIRS.FORWARD)
        for i in range(height):
                for j in range(width):
                        navigator.force_dir(nav.DIRS.FORWARD, depth - 1, do)
                        # reposition to dig second row
                        if j != (width - 1):
                                # choose direction
                                direction = directions[direction_index] 

                                # turn to next row
                                navigator.turn(direction)
                                navigator.force_dir(nav.DIRS.FORWARD, 1, do)
                                navigator.turn(direction)

                                # change direction
                                direction_index = (direction_index + 1) % 2
                                
j                # reset in next level
                if i != (height - 1):
                        manage_inv([valuables])
                        navigator.force_dir(zdir, 1, do)
                        navigator.turn(nav.TURNS.LEFT)
                        navigator.turn(nav.TURNS.LEFT)
        if go_home:
                navigator.go_to(initial_location)
                navigator.turn_to(initial_direction)

# drops all non valuable items and condenses inventory when full
def manage_inv(valuables):
        if valuables and inv.is_full():
                inv.drop_all_except(VALUABLES)
                inv.restack()

def do_wrapper(args):
        manage_inv = args[0][0]
        valuables = args[0][1]
        manage_inv(valuables)

        if len(args) > 1:
                do = args[1][0]
                do_args = args[1][1]
                do(do_args)

