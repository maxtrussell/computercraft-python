"""
1. Harvest wheat
2. Hoe + Plant seeds
3. Hibernate
"""

from cc import import_file, os, turtle

inv = import_file('/lib/inv.py')
nav = import_file('/lib/nav.py')

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
    inv.drop_all_except({'minecraft:coal', crop.seed}, down=True)
    inv.select_by_name('minecraft:coal')
    coal_qty = turtle.getItemCount()
    if coal_qty < 64:
        turtle.turnLeft()
        turtle.suck(64 - coal_qty)
        turtle.turnRight()
    seed_qty = inv.count_item(crop.seed)
    if seed_qty > 80:
        # 80 is the capacity of the farm
        inv.drop_some(crop.seed, seed_qty-80, down=True)

CROPS = [
    Crop('wheat', 'wheat', 'wheat_seeds', 7),
    Crop('carrots', 'carrot', 'carrot', 7),
    Crop('potatoes', 'potato', 'potato', 7),
    Crop('beetroots', 'beetroot', 'beetroot_seeds', 3),
]

if len(args) == 0:
    print('Usage: farm <crop>')
else:
    # Timer is reset on reboot, so always start with a farming pass
    active_crop = [c for c in CROPS if c.product == f'minecraft:{args[0]}'][0]
    print(f'Farming {active_crop.product}...')
    manage_inventory(active_crop)
    farm(active_crop)
    manage_inventory(active_crop)
    while True:
        os.sleep(30 * 60)  # sleep 30 minutes between runs
        farm(active_crop)
        manage_inventory(active_crop)
