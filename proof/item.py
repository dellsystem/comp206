#!/usr/bin/python

from random import randint

# Takes parameters as strings and casts them to integers
# Bad practice but slightly computationally faster

class Item:

	# Constructs new Item with parameters in same order as inventory.csv		
	def __init__( self, name, avg, var, quantity, cur_price ):
		self.name = name
		self.avg = int(avg)
		self.var = int(var)
		self.quantity = int(quantity)
		self.cur_price = int(cur_price)
	
	# Modifies the quantity of the inventory item by some amount

	def updateQnty( self, qnty_change ):
		self.quantity += qnty_change
		
	# Randomly generates a new price for the item
	# between average price +/- var

	def newPrice( self ):
		lower = self.avg - self.var
		upper = self.avg + self.var
		self.cur_price = randint(lower, upper)
	
	# Returns the data in Item in a single string
	# formatted for CSV

	def getCSV( self ):
		csv = '%s,%d,%d,%d,%d\n' % (self.name, self.avg, self.var, self.quantity, self.cur_price)
		return csv		
