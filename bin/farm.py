"""
1. Harvest wheat
2. Hoe + Plant seeds
3. Hibernate
"""

from cc import gps, import_file, os, turtle

inv = import_file('/lib/inv.py')
nav = import_file('/lib/nav.py')
net = import_file('/lib/net.py')

class Crop:
    def __init__(self, crop, product, seed, growth_age):
        id_str = 'minecraft:{}'
        self.crop = id_str.format(crop).encode('utf-8')
        self.product = id_str.format(product)
        self.seed = id_str.format(seed)
        self.growth_age = growth_age

def farm(crop: Crop):
    turn_dir = turtle.turnRight
    nav.force_dir(nav.DIRS.FORWARD)
    for i in range(9):
        for j in range(9):
            if j != 0:
                nav.force_dir(nav.DIRS.FORWARD)

            target = turtle.inspectDown()
            if not target or (target[b'name'] == crop.crop and target[b'state'][b'age'] == crop.growth_age):
                turtle.digDown()  # harvests and tills

            # plant
            inv.select_by_name(crop.seed)
            turtle.placeDown()

        if i != 8:
            turn_dir()
            nav.force_dir(nav.DIRS.FORWARD)
            turn_dir()
            turn_dir = turtle.turnRight if turn_dir is turtle.turnLeft else turtle.turnLeft

    # return to start
    turtle.turnLeft()
    nav.force_dir(nav.DIRS.FORWARD, 8)
    turtle.turnLeft()
    nav.force_dir(nav.DIRS.FORWARD, 9)
    [turtle.turnLeft() for i in range(2)]

def manage_inventory(crop):
    accepted_fuel = {'minecraft:coal', 'minecraft:charcoal'}
    inv.drop_all_except(accepted_fuel | {crop.seed}, turtle.dropDown)
    coal_qty = inv.count_items(accepted_fuel)
    if coal_qty < 64:
        turtle.turnLeft()
        turtle.suck(64 - coal_qty)
        turtle.turnRight()
        try:
            if inv.count_items(accepted_fuel) < 64:
                # The fuel chest has run out, alert main server
                net.request('main-server:FUEL/low', await_response=False)
            else:
                # The turtle has sufficient fuel. alert main server
                net.request('main-server:FUEL/ok', await_response=False)
        except Exception as e:
            print(f'ERROR: {str(e)}')

    seed_qty = inv.count_items({crop.seed})
    if seed_qty > 80:
        # 80 is the capacity of the farm
        inv.drop_some({crop.seed}, seed_qty-80, turtle.dropDown)
    inv.restack()

def initialize(initial_pos, initial_bearing):
    navigator = nav.Navigator([int(x) for x in gps.locate()], nav.get_bearing())
    navigator.go_to(initial_pos)
    navigator.turn_to(initial_bearing)

CROPS = [
    Crop('wheat', 'wheat', 'wheat_seeds', 7),
    Crop('carrots', 'carrot', 'carrot', 7),
    Crop('potatoes', 'potato', 'potato', 7),
    Crop('beetroots', 'beetroot', 'beetroot_seeds', 3),
]

if len(args) != 5:
    print('Usage: farm <crop> <x> <y> <z> <bearing>')
else:
    # Timer is reset on reboot, so always start with a farming pass
    active_crop = [c for c in CROPS if c.product == f'minecraft:{args[0]}'][0]
    print(f'Farming {active_crop.product}...')

    initial_pos = [int(x) for x in args[1:4]]
    initial_bearing = nav.CARDINALS(int(args[4]))
    initialize(initial_pos, initial_bearing)

    manage_inventory(active_crop)
    farm(active_crop)
    manage_inventory(active_crop)
    while True:
        os.sleep(30 * 60)  # sleep 30 minutes between runs
        farm(active_crop)
        manage_inventory(active_crop)
