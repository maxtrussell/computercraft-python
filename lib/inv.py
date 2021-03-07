from cc import turtle
# select a block with given name
def select_by_name(name):
	for i in range(16):
		item = turtle.getItemDetail(i + 1)
		if item is not None and item.name == name:
			turtle.select(i + 1)
			return true
	return false 

# select the first item in inv from dictionary
def select_from_dict(dict):
	for i in range(16):
		item = turtle.getItemDetail(i + 1)
		if item is not None and item.name in dict:
			turtle.select(i + 1)
			return true
	return false

# checks if every inventory slot has a block in it
# does not care if slots have space remaining
def is_full():
	for i in range(16):
		item = turtle.getItemDetail(i + 1)
		if item is None:
			return false
	return true

# drop all tiems from invenotry execpt those in provided table
def drop_all_except(keep):
	initial_slot = turtle.getSelectedSlot()
	for i in range(16):
		item = turtle.getItemDetail(i + 1)
		if item is not None and item.name not in keep:
			# found item not in keep
			turtle.select(i + 1)
			turtle.drop()
	turtle.select(initial_slot)

# deposites all of a certain block into a chest
# turtle must be facing the chest
def deposit_block(name):
	initial_slot = turtle.getSelectedSlot()
	while select_by_name(name):
		turtle.drop()
	turtle.select(initial_slot)

# condense turtle inventory
def restack():
	initial_slot = turtle.getSelectedSlot()
	inv = {}
	for i in range(16):
		item = turtle.getItemDetail(i + 1)
		if item is not None:
			if item is in inv:
				# stack with space already in inventory
				turtle.select(i + 1)
				turtle.transferTo(inv[item.name]['slot'])
				prev_space = turtle.getItemSpace(inv[item.name]['slot'])
				if prev_space > 0:
					# previous stack still has space remaining
					inv[item.name]['space'] = prev_space
				else if turtle.getItemCount(i + 1) > 0:
					# previous stack full, selected not empty
					inv[item.name] = {'space':turtle.getItemSpace(i + 1), 'slot':i + 1}
				else:
					# previous stack full, selected not empty
					inv[item.name] = null
			else if turtle.getItemSpace(i + 1) > 0:
				# add item to inv if not there and still has space
				inv[item.name] = {'space':turtle.getItemSpace(i + i), 'slot':i + 1}
	turtle.select(initial_slot)

def inv_dict():
	inv = {}
	for i in range(16):
		item = getItemDetail(i + 1)
		inv[i + 1] = item
	return inv