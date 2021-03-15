from cc import turtle
# select a block with given name
def select_by_name(name):
    # item keys are byte strings
    name = name.encode('utf-8')

    curr_selected = turtle.getItemDetail()
    if curr_selected and curr_selected[b'name'] == name:
        # item already selected, short circuit
        # avoiding selects saves time
        return True
        
    for i in range(1,17):
        item = turtle.getItemDetail(i)
        if item is not None and item[b'name'] == name:
            turtle.select(i)
            return True
    return False

# select the first item in inv from dictionary
def select_from_dict(d):
    d = {k.encode('utf-8'): v for k,v in d.items()}
    for i in range(16):
        item = turtle.getItemDetail(i + 1)
        if item is not None and item[b'name'] in d:
            turtle.select(i + 1)
            return True
    return False

# checks if every inventory slot has a block in it
# does not care if slots have space remaining
def is_full():
    for i in range(16):
        item = turtle.getItemDetail(i + 1)
        if item is None:
            return False
    return True

# drop all iteems from invenotry execpt those in provided set
def drop_all_except(keep, down=False):
    keep = {x.encode('utf-8') for x in keep}
    initial_slot = turtle.getSelectedSlot()
    for i in range(16):
        item = turtle.getItemDetail(i + 1)
        if item is not None and item[b'name'] not in keep:
            # found item not in keep
            turtle.select(i + 1)
            if down:
                turtle.dropDown()
            else:
                turtle.drop()
    turtle.select(initial_slot)

def count_items(items):
    items = {x.encode('utf-8') for x in items}
    inventory = [turtle.getItemDetail(i) for i in range(1,17)]
    target_item = lambda x: x is not None and x[b'name'] in items
    return sum([i[b'count'] for i in inventory if target_item(i)])

# deposit all of a certain block into a chest
# turtle must be facing the chest
def drop_item(name, drop_func=turtle.drop):
    initial_slot = turtle.getSelectedSlot()
    while select_by_name(name):
        drop_func()
    turtle.select(initial_slot)

def drop_some(names, qty, drop_func=turtle.drop):
    names = {x.encode('utf-8') for x in names}
    initial_slot = turtle.getSelectedSlot()
    dropped = 0
    for i in range(1,17):
        if dropped >= qty:
            break
        item = turtle.getItemDetail(i)
        if item is not None and item[b'name'] in names:
            to_drop = min(qty - dropped, item[b'count'])
            turtle.select(i)
            drop_func(to_drop)
            dropped += to_drop
    turtle.select(initial_slot)
    
def drop_all(drop_func=turtle.drop):
    initial_slot = turtle.getSelectedSlot()
    for i in range(1,17):
        if turtle.getItemCount(i) != 0:
            turtle.select(i)
            drop_func()
    turtle.select(initial_slot)

# condense turtle inventory
def restack():
    initial_slot = turtle.getSelectedSlot()
    inv = {}
    for i in range(1, 17):
        item = turtle.getItemDetail(i)
        if item is not None:
            if item[b'name'] in inv:
                # stack with space already in inventory
                turtle.select(i)
                turtle.transferTo(inv[item[b'name']]['slot'])
                prev_space = turtle.getItemSpace(inv[item[b'name']]['slot'])
                if prev_space > 0:
                    # previous stack still has space remaining
                    inv[item[b'name']]['space'] = prev_space
                elif turtle.getItemCount(i) > 0:
                    # previous stack full, selected not empty
                    inv[item[b'name']] = {'space': turtle.getItemSpace(i), 'slot': i}
                else:
                    # previous stack full, selected not empty
                    del inv[item[b'name']]
            elif turtle.getItemSpace(i) > 0:
                # add item to inv if not there and still has space
                inv[item[b'name']] = {'space': turtle.getItemSpace(i), 'slot': i}
    turtle.select(initial_slot)

def inv_dict():
    return {i: turtle.getItemDetail(i) for i in range(1, 17)}
