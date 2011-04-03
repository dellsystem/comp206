#!/usr/bin/python

import item

def get_inventory( filename ):
	inv_file = open(filename, 'r')
	inventory = inv_file.readlines()
	inv_file.close()

	item_list = []	
	for entry in inventory:
		entry.strip('\n')
		values = entry.split(',')
		new_item = item.Item(values[0], values[1], values[2], values[3], values[4])
		item_list.append(new_item)

	return item_list

def write_inventory( filename, item_list ):
	inv_file = open(filename, 'w')
	
	for item in item_list:
		line = item.getCSV()
		inv_file.write(line)
					
	inv_file.close()			
