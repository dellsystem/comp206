import random

Rooms = [{'name': "The Moon", 'title': "The Moon", 'image':"moon_thumb", 'url':"~wliu65/206/"},
         {'name': "Arrakis", 'title': "Arrakis", 'image':"arrakis_thumb", 'url':"~hbrund/206/"},
         {'name': "Orion", 'title': "The Orion Nebula", 'image':"orion_thumb", 'url':"~csuder/206/"},
         {'name': "SSS", 'title': "Shatner Space Station", 'image':"sss_thumb", 'url':"~cleung24/206/"},
         {'name': "MM", 'title': "Memento Mori", 'image':"mm_thumb", 'url':"~ezarou/206/"},
        ]

# Class which represents the metaclass of the available items for purchase
# Responsible for managing the global particulars of one entry, such as the price generation
class Commodity:
    def __init__(self, name, prices):
        self.name = name
        self.prices = prices

    def toInventoryItem(self):
        return InventoryItem(self.name, 0, random.choice(self.prices)) 

Commodities = map(lambda x: Commodity(x[0],x[1]), [["Ore",          range(10,20)],
                                                   ["Laser Swords", range(100,200)], 
                                                   ["Cheese",       range(2,4)], 
                                                   ["Melange",      range(1000,6000)], 
                                                   ["Whatever",     range(10,20)]])


# Class which represents the possession of some commodity by the user. A row in the inventory, if you will.
class InventoryItem:
    def __init__(self, commodity_name, quantity, price):
        self.quantity = int(quantity)
        self.price = int(price)
        self.commodity_name = commodity_name
        commodities = filter( lambda x: x.name == commodity_name , Commodities)
        if commodities:
            self.commodity = commodities[0]
        else:
            self.commodity_name = "Space Junk (%s)" % commodity_name
    
    def updateQnty( self, qnty_change ):
        self.quantity += qnty_change
        
    def getCSV( self ):
        csv = '%s,%d,\n' % (self.commodity_name, self.quantity)
        return csv      

# Class which represents the collection of currently owned items, and manages reading and writing this to disk
class Inventory:
    def __init__(self, filename="database/inventory.csv"):
        self.filename = filename
        self.read()

    def read(self):
        inv_file = open(self.filename, 'r')
        inventory = inv_file.readlines()
        inv_file.close()

        self.items = [] 
        for entry in inventory:
            entry.strip('\n')
            values = entry.split(',')
            new_item = InventoryItem(*values)
            self.items.append(new_item)

        return self.items

    def write(self):
        inv_file = open(self.filename, 'w')
    
        for item in self.items:
            line = item.getCSV()
            inv_file.write(line)
                        
        inv_file.close()
        return self.items

# Class which represnets an inventory full of items which may or may not be part of the commodities
class Planet:

    def __init__(self):
        self._market = {}
        for com in Commodities:
            self._market[com.name] = com.toInventoryItem()

        self.inventory = Inventory()
        for item in self.inventory.items:
            if item.commodity_name in self._market:
                self._market[item.commodity_name]['quantity'] += item.quantity
            else:
                self._market[item.commodity_name] = item

    def market(self):
        return [{'name': x.commodity_name, 'quantity':x.quantity, 'price':x.price, 'available_quantity': 200} for k, x in self._market.iteritems()]
