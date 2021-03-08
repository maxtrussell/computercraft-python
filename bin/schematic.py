from collections import defaultdict
import math
import sys

in_minecraft = 'args' in globals()
if in_minecraft:
    from cc import fs, import_file, turtle
    nav = import_file('/lib/nav.py')
    inv = import_file('/lib/inv.py')

def parse_schematic(path, open_func):
    """ Returns 3D array of schematic """
    schematic = []
    curr_slice = []
    block_defs = {}
    in_def_blocks = False
    in_slice = False
    with open_func(path, 'r') as f:
        for line in f:
            if line.startswith('#DEF_BLOCKS'):
                in_def_blocks = True
            elif line.startswith('#END_DEF_BLOCKS'):
                in_def_blocks = False
            elif line.startswith('#START'):
                in_slice = True
            elif line.startswith('#END'):
                times = 1
                if 'x' in line:
                    times = int(line.split('x')[1])
                schematic.extend([curr_slice] * times)
                curr_slice = []
                in_slice = False
            elif in_def_blocks:
                k,v = line.split('=')
                block_defs[k.strip()] = v.strip()
            elif in_slice:
                curr_slice.append(list(line.strip()))
    return schematic, block_defs

def build_slice(slice, block_defs):
    selected = 0
    turn_dir = turtle.turnRight

    for i in range(len(slice)):
        for j in range(len(slice[i])):
            if j != 0:
                nav.force_dir(nav.DIRS.FORWARD)
            symbol = slice[i][j]
            if symbol in block_defs:
                inv.select_by_name(block_defs[symbol])
                turtle.placeDown()

        if i != len(slice)-1:
            # turn to next row
            turn_dir()
            nav.force_dir(nav.DIRS.FORWARD)
            turn_dir()

            # flip the turn direction
            turn_dir = turtle.turnRight if turn_dir is turtle.turnLeft else turtle.turnLeft

    # reset for the next level
    nav.force_dir(nav.DIRS.UP)
    if len(slice) % 2 == 0:
        turtle.turnRight()
        nav.force_dir(nav.DIRS.FORWARD, len(slice)-1)
        turtle.turnRight()
    else:
        turtle.turnLeft()
        nav.force_dir(nav.DIRS.FORWARD, len(slice)-1)

        turtle.turnLeft()
        nav.force_dir(nav.DIRS.FORWARD, len(slice[-1])-1)
        turtle.turnLeft()
        turtle.turnLeft()


# make args global accessible from within or outside of MC
args = args if in_minecraft else sys.argv[1:]

if len(args) == 0:
    print('Usage: schematic <path to schematic file> [--analyze]')

schematic, block_defs = parse_schematic(f'schematics/{args[0]}', fs.open if in_minecraft else open)
if '--analyze' in args:
    char_counts = defaultdict(lambda: 0)
    def count_col(col):
        char_counts[col] += 1
    [[[count_col(col) for col in row if col != '.'] for row in slice] for slice in schematic]

    depth = max([len(s) for s in schematic])
    width = max([len(r) for r in [s for s in schematic]])
    height = len(schematic)
    fuel = width*depth*height + height*(width+depth)
    print(f'Height: {height}')
    print(f'Footprint: {width}x{depth}')
    print(f'Est Fuel: {fuel} ({math.ceil(fuel/80)} coal)')
    print('Block counts:')
    for k,v in sorted(dict(char_counts).items()):
        print(f'- {block_defs[k]}: {v} ({v // 64} stacks + {v % 64})')
elif in_minecraft:
    # obviously you can only build from within minecraft
    for slice in schematic:
        build_slice(slice, block_defs)
