from cc import import_file

dig = import_file('/lib/dig.py')
nav = import_file('/lib/nav.py')

# Wrapper for dig
if len(args) < 3:
    print('Usage: quarry <width> <depth> <height> [valuables?] [down?] [go_home?] [chest: xcord,ycord,zcord direction')

width, depth, height = [int(x) for x in args[:3]]
valuables = bool(args[3]) if len(args) > 3 else False
go_down = bool(args[4]) if len(args) > 4 else False
go_home = bool(args[5]) if len(args) > 5 else False

if len(args) > 7:
    chest_location = args[6].split(',')
    chest_direction = nav.CARDINALS[args[7]]
    chest = [chest_location, chest_direction]
else:
    chest = None

dig.quarry(width, depth, height, valuables, go_down, go_home, chest)
