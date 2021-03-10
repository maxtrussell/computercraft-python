from collections import defaultdict
import math
import sys

in_minecraft = 'args' in globals()
if in_minecraft:
    from cc import fs, import_file, turtle
    nav = import_file('/lib/nav.py')
    navigator = nav.Navigator()
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
    turn_dir = nav.TURNS.RIGHT
    turn = navigator.turn

    def place(args):
        slice = args[0]
        block_defs = args[1]
        y = - navigator.location[0]
        x = navigator.location[1]

        if y % 2 == 0:
            symbol = slice[y][x]
        else:
            symbol = slice[y][::-1][x]

        if symbol in block_defs:
            inv.select_by_name(block_defs[symbol])
            turtle.placeDown()
    
    for i in range(len(slice)):
        place([slice, block_defs])
        navigator.force_dir(nav.DIRS.FORWARD, len(slice[i]) - 1, [place, [slice, block_defs]])

        if i != len(slice)-1:
            place([slice, block_defs])
            navigator.go_to([navigator.location[0] - 1, navigator.location[1], navigator.location[2]])
            navigator.turn(nav.TURNS.LEFT) if navigator.location[0] % 2 else navigator.turn(nav.TURNS.RIGHT)

    # reset for the next level
    nav.force_dir(nav.DIRS.UP)
    if len(slice) % 2 == 0:
        navigator.turn(nav.TURNS.RIGHT)
        navigator.force_dir(nav.DIRS.FORWARD, len(slice)-1)
        navigator.turn(nav.TURNS.RIGHT)
    else:
        navigator.turn(nav.TURNS.LEFT)
        navigator.force_dir(nav.DIRS.FORWARD, len(slice)-1)

        navigator.turn(nav.TURNS.LEFT)
        navigator.force_dir(nav.DIRS.FORWARD, len(slice[-1])-1)
        navigator.turn(nav.TURNS.LEFT)
        navigator.turn(nav.TURNS.LEFT)


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
    width = max([max([len(r) for r in s]) for s in schematic])
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
    navigator.go_to([0,0,0])
    navigator.turn_to(nav.CARDINALS.NORTH)
