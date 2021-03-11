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
def quarry(width, depth, height, valuables=False, go_down=False, go_home=False, chest=None, do=None):
        navigator = nav.Navigator()
        initial_location = navigator.get_location()
        initial_direction = navigator.get_direction()
        # get direction z
        zdir = nav.DIRS.DOWN if go_down else nav.DIRS.UP

        # pack do
        keep = VALUABLES if valuables else None
        if chest:
                chest.append(navigator)
        quarry_dos = [manage_inv, keep, chest]
        do = [do_wrapper, [quarry_dos, [d[0], d[1]]]] if do else [do_wrapper, [quarry_dos]]

        # axis one direction changes
        directions = [nav.TURNS.LEFT, nav.TURNS.RIGHT]
        direction_index = 1

        navigator.force_dir(nav.DIRS.FORWARD, 1, do)
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
                                
                # reset in next level
                if i != (height - 1):
                        navigator.force_dir(zdir, 1, do)
                        navigator.turn(nav.TURNS.LEFT)
                        navigator.turn(nav.TURNS.LEFT)
        if go_home:
                navigator.go_to(initial_location)
                navigator.turn_to(initial_direction)

# drops all non valuable items and condenses inventory when full
def manage_inv(valuables, chest):
        if valuables and inv.is_full():
                inv.drop_all_except(VALUABLES)
                inv.restack()

        if chest and inv.is_full():
                current_location = navigator.get_location()
                current_direction = navigator.get_direction()

                chest_location = chest[0]
                chest_direction = chest[1]
                navigator = chest[2]

                # return to chest
                navigator.go_to(chest_coordinates)
                navigator.turn_to(chest_direction)
                # deposit all
                inv.drop_all_except({})

                # go back
                navigator.go_to(current_location)
                navigator.turn_to(current_direction)


def do_wrapper(args):
        manage_inv = args[0][0]
        valuables = args[0][1]
        chest = args[0][2]
        manage_inv(valuables, chest)

        if len(args) > 1:
                do = args[1][0]
                do_args = args[1][1]
                do(do_args)

