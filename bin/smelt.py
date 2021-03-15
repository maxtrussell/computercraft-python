import math

from cc import import_file, os, turtle

inv = import_file('lib/inv.py')
nav = import_file('lib/nav.py')

ACCEPTED_FUEL = {'minecraft:coal', 'minecraft:charcoal'}

def smelt():
    # Account for inventory
    inventory = {x[b'name'].decode('utf-8') for x in inv.inv_dict().values() if x is not None}
    smeltables = inventory - ACCEPTED_FUEL
    fuel_qty = inv.count_items(ACCEPTED_FUEL)
    smelt_qty = inv.count_items(smeltables)

    required_fuel = math.ceil(smelt_qty / 8)
    furnaces_required = min(8, min(required_fuel, fuel_qty))

    # Find limiting reagent, fuel or smeltables
    if fuel_qty >= required_fuel:
        items_per_furnace = min(64, math.ceil(smelt_qty / furnaces_required))
    else:
        items_per_furnace = min(64, math.floor(fuel_qty * 8 / furnaces_required))

    # add smeltables to furnaces
    for i in range(8):
        callback = None
        if i < furnaces_required:
            callback = add_to_furnace(smeltables, items_per_furnace, turtle.dropDown)
        nav.dir(nav.DIRS.FORWARD, callback=callback)
    nav.dir(nav.DIRS.FORWARD)

    # Move below furnaces
    nav.turn(nav.TURNS.LEFT, n=2)
    nav.dir(nav.DIRS.DOWN, n=2)

    # add fuel to furnaces
    for i in range(8):
        callback = None
        if 8 - i <= furnaces_required:
            callback=add_to_furnace(ACCEPTED_FUEL, math.ceil(items_per_furnace / 8), turtle.dropUp)
        nav.dir(
            nav.DIRS.FORWARD,
            callback=callback,
        )
    nav.dir(nav.DIRS.FORWARD)

    # Wait for smelting to complete
    smelt_time = math.ceil(items_per_furnace * 10)
    print(f'Waiting {smelt_time} seconds...')
    os.sleep(smelt_time)

    # Collect smelted items
    nav.turn(nav.TURNS.LEFT, n=2)
    nav.dir(nav.DIRS.FORWARD, n=8, callback=turtle.suckUp)
    nav.dir(nav.DIRS.FORWARD)

    # Move above furnaces
    nav.turn(nav.TURNS.LEFT, n=2)
    nav.dir(nav.DIRS.UP, n=2)

    # Cannot collect extra fuel
    nav.dir(nav.DIRS.FORWARD, n=9)
    nav.turn(nav.TURNS.LEFT, n=2)

    # Drop products into chest
    inventory = {x[b'name'].decode('utf-8') for x in inv.inv_dict().values() if x is not None}
    for item in inventory - ACCEPTED_FUEL:
        inv.drop_item(item, turtle.dropDown)
    
def add_to_furnace(items, qty, drop_func):
    """ Wraps callback function with args """
    def wrapper():
        return inv.drop_some(items, qty, drop_func) if qty > 0 else None
    return wrapper


smelt()
