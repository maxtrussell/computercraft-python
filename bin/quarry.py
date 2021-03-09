from cc import import_file

dig = import_file('/lib/dig.py')

# Wrapper for dig
if len(args) < 3:
    print('Usage: quarry <width> <depth> <height> [valuables?] [down?] [go home?]')

width, depth, height = [int(x) for x in args[:3]]
valuables = bool(args[3]) if len(args) > 3 else False
go_down = bool(args[4]) if len(args) > 4 else False
go_home = bool(args[5]) if len(args) > 5 else False

dig.quarry(width, depth, height, valuables, go_down, go_home)
