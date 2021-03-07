from cc import import_file

dig = import_file('/lib/dig.py')

# Wrapper for dig
if len(args) < 3:
    print('Usage: quarry <width> <depth> <height> [valuables?] [down?]')

width, depth, height = args[:3]
valuables = bool(args[3]) if len(args) > 3 else False
go_down = bool(args[4]) if len(args) > 4 else False

dig.quarry(width, depth, height, valuables, go_down)
