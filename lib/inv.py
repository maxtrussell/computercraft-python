from cc import turtle
# select a block with given name
def select_by_name(name):
    # item keys are byte strings
    name = name.encode('utf-8')

    curr_selected = turtle.getItemDetail()
    if curr_selected and curr_selected[b'name'] == name:
        # item already selected, short circuit
        return
        
    for i in range(16):
        item = turtle.getItemDetail(i + 1)
        if item is not None and item[b'name'] == name:
            turtle.select(i + 1)
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

def count_item(name):
    byte_name = name.encode('utf-8')
    inventory = [turtle.getItemDetail(i) for i in range(1,17)]
    target_item = lambda x: x is not None and x[b'name'] == byte_name
    return sum([i[b'count'] for i in inventory if target_item(i)])

# deposit all of a certain block into a chest
# turtle must be facing the chest
def drop_item(name, down=False):
    initial_slot = turtle.getSelectedSlot()
    while select_by_name(name):
        if down:
            turtle.dropDown()
        else:
            turtle.drop()
    turtle.select(initial_slot)

def drop_some(name, qty, down=False):
    name = name.encode('utf-8')
    initial_slot = turtle.getSelectedSlot()
    dropped = 0
    for i in range(1,17):
        if dropped >= qty:
            break
        item = turtle.getItemDetail(i)
        if item is not None and item[b'name'] == name:
            to_drop = min(qty - dropped, item[b'count'])
            turtle.select(i)
            if down:
                turtle.dropDown(to_drop)
            else:
                turtle.drop(to_drop)
            dropped += to_drop
    turtle.select(initial_slot)
    

def drop_all(down=False):
    initial_slot = turtle.getSelectedSlot()
    for i in range(1,17):
        if turtle.getItemCount(i) != 0:
            turtle.select(i)
            if down:
                turtle.dropDown()
            else:
                turtle.drop()
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
    inv = {}
    for i in range(16):
        item = getItemDetail(i + 1)
        inv[i + 1] = item
    return inv
