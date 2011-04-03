#!/usr/bin/python

from random import randint

# Takes parameters as strings and casts them to integers
# Bad practice but slightly computationally faster

class Item:
	def __init__( self, name, avg, var, quantity, cur_price ):
		self.name = name
		self.avg = int(avg)
		self.var = int(var)
		self.quantity = int(quantity)
		self.cur_price = int(cur_price)
	
	def updateQnty( self, qnty_change ):
		self.quantity += qnty_change
		
	def newPrice( self ):
		lower = self.avg - self.var
		upper = self.avg + self.var
		self.cur_price = randint(lower, upper)
	
	def getCSV( self ):
		csv = '%s,%d,%d,%d,%d\n' % (self.name, self.avg, self.var, self.quantity, self.cur_price)
		return csv		
