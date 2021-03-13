from collections import defaultdict
import math
import sys
from cc import import_file, fs

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

def build_slice(slice, block_defs, navigator):
    selected = 0
    turn = navigator.turn
    initial_location = navigator.get_location()
    initial_direction = navigator.get_direction()

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
        place([slice, block_defs])

        if i != len(slice)-1:
            navigator.go_to([navigator.location[0] - 1, navigator.location[1], navigator.location[2]])
            navigator.turn(nav.TURNS.LEFT) if navigator.location[0] % 2 else navigator.turn(nav.TURNS.RIGHT)
    place([slice, block_defs])
    navigator.go_to(initial_location)
    navigator.turn_to(initial_direction)
    navigator.force_dir(nav.DIRS.UP)

def run_schematic(path_to_schematic, analyze=False, navigator=None):
    navigator = navigator if navigator else nav.Navigator()
    schematic, block_defs = parse_schematic(path_to_schematic, fs.open)
    if analyze:
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
    elif:
        for slice in schematic:
            build_slice(slice, block_defs, navigator)
	