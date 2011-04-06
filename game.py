# game.py - implementation of the commodity trading game including inventory reading and writing
import random, re

# Class which represents the metaclass of the available items for purchase
# Responsible for managing the global particulars of one entry, such as the price generation
class Commodity:
    def __init__(self, name, prices):
        self.name = name
        self.prices = prices

    # Used for initializing a Planet's market (see Planet)
    def toInventoryDict(self):
        return {'name': self.name, 'quantity': 0, 'available_quantity': 0}

class MalformedCSVError(Exception):
    pass

# Class which represents the possession of some commodity by the planet. A row in the inventory, if you will.
# Holds the name of the commodity, the quantity possesed by the planet, and the price at this instant.
class InventoryItem:
    def __init__(self, commodity_name, quantity):
        self.quantity = int(quantity)
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

    def fromCSV(entry):
        values = entry.split(',')
        if not len(values) == 2:
            raise MalformedCSVError
        return InventoryItem(*values)
    fromCSV = staticmethod(fromCSV)

# Class which represents the collection of currently available items, and manages reading and writing this to disk
class PlanetInventory:
    def __init__(self, room_number):
        self.filename = "database/inventory" + str(room_number) + ".csv"
        self.read() # Grab the inventory items upon creation

    def read(self):
        inv_file = open(self.filename, 'r')
        inventory = inv_file.readlines()
        inv_file.close()

        self.items = []
        self.items_dict = {}
        for entry in inventory:
            entry.strip('\n')
            new_item = InventoryItem.fromCSV(entry)
            self.items.append(new_item)
            self.items_dict[new_item.commodity_name] = new_item
        return self.items

    def write(self):
        inv_file = open(self.filename, 'w')
        for item in self.items:
            line = item.getCSV()
            inv_file.write(line)

        inv_file.close()
        return self.items

# Raised when the form tag describing a user's inventory isn't correctly formatted
class MalformedGameFormError(Exception):
    pass

class UserInventory:
    def __init__(self, form):
        self.items = []
        self.items_dict = {}
        if "points" not in form:
            raise MalformedGameFormError()
        else:
            self.points = form["points"].value

        # Add all the inventory items we can to this object
        for key in form:
            if re.search('Inventory(\d+)', key):
                value = form[key].value
                m = re.search('^(\d+) (.+)$', value)
                if m:
                    # Matches our iventory spec, yahoo! Use the quantity.
                    item = InventoryItem(m.group(2), m.group(1))
                else:
                    # Does not match our inventory spec. Take a tiny quantity.
                    item = InventoryItem(value, 1)
                self.items.append(item)
                self.items_dict[item.commodity_name] = item

    def render(self):
        s = '<input type="hidden" name="points" value="' + str(self.points) + '" />'
        for i, item in enumerate(self.items):
            s += '<input type="hidden" name="Inventory' + str(i+1) + '" value="' + str(item.quantity) + '" />'
        return s

# Class which represnets an inventory full of items which may or may not be part of the commodities
class Planet:
    def __init__(self, user_inventory, form, room):
        self.market = {}
        self.inventory = PlanetInventory(room)
        self.user_inventory = user_inventory
        self.form = form
        # The market has all the standard commodities by default.
        for com in Commodities:
            # Gets an inventory item using the submitted price if its given, and lets the
            # commodity pick one otherwise.
            self.market[com.name] = com.toInventoryDict()
            key = 'price_'+com.name
            if key in form:
                self.market[com.name]['price'] = self.form.getfirst(key)
            else:
                self.market[com.name]['price'] = random.choice(com.prices)

        # Loop through the items in the planet's inventory. If its a standard item, then
        # add the quantity to the existing item. If its non standard, add it to the list.
        # Notice that here, the quantity of the inventory item represents the quantity
        # the planet has to sell to the user, so we put it in the 'available_quantity' key.
        for item in self.inventory.items:
            if item.commodity_name in self.market:
                self.market[item.commodity_name]['available_quantity'] += item.quantity
            else:
                self.market[item.commodity_name] = {'name': item.commodity_name, 'quantity': 0, 'available_quantity': item.quantity}

        # Loop through the items in the user's inventory. If its a standard item, then
        # add the quantity to the existing item. If its non standard, add it to the list.
        # Notice that here, the quantity of the inventory item represents the quantity the
        # user has to sell, so we put it in the 'quantity' key.
        for item in self.user_inventory.items:
            if item.commodity_name in self.market:
                self.market[item.commodity_name]['quantity'] += item.quantity
            else:
                self.market[item.commodity_name] = {'name': item.commodity_name, 'quantity': item.quantity, 'available_quantity': 0}

        for key, item in self.market.iteritems():
            if 'price' not in item:
                self.market[key]['price'] = random.choice([1,2,3])

        self.market = [row for key, row in self.market.iteritems()]

    def purchase_order(self):
        return True

    def purchase_order_errors(self):
        errors = []

        if 'points' not in self.form:
            return ["Malformed form, please try submitting again!"]
        else:
            points = int(self.form.getfirst('points'))
        
        for key in self.form:
            m = re.search("com_name_([0-9]+)", key)
            if not not m:
                num = m.group(1)
                # Qty, action, price group found. Check all values are present
                commodity_name = self.form.getfirst("com_name_"+num)
                quantity = self.form.getfirst("qty_"+num)
                action = self.form.getfirst("action_"+num)
                price = self.form.getfirst("price_"+num)
                
                if not commodity_name or not quantity or not action or not price:
                    errors.append("Malformed form, please try submitting again!")
                    break
                
                price = int(price)
                quantity = int(quantity)
                if quantity > 0:
                    # Validate buy action
                    if action == "buy":
                        if not commodity_name in self.inventory.items_dict:
                            errors.append("You can't buy "+commodity_name+" from this planet, it doesn't have any!")
                            continue
                        if quantity > self.inventory.items_dict[commodity_name].quantity:
                            errors.append("You can't buy more "+commodity_name+" than is available, sorry.")
                            continue

                        points -= price * quantity

                    elif action == "sell":
                        if not commodity_name in self.user_inventory.items_dict:
                            errors.append("You can't sell "+commodity_name+" because you don't have any! Tisk!")
                            continue
                        if quantity > self.user_inventory.items_dict[commodity_name]:
                            errors.append("You can't sell more "+commodity_name+"than you have. Tisk!")
                            continue

                        points += price * quantity
                    else:
                        errors.append("Malformed form, please try submitting again!")
                        break

        if points < 0:
            errors.append("You don't have enough money for these transactions, sorry.")

        return errors
# Constant listing all the rooms and their attributes
Rooms = [{'name': "The Moon", 'title': "The Moon", 'image':"moon_thumb", 'url':"~wliu65/206-5/"},
        {'name': "Arrakis", 'title': "Arrakis", 'image':"arrakis_thumb", 'url':"~hbrund/206/"},
        {'name': "Orion", 'title': "The Orion Nebula", 'image':"orion_thumb", 'url':"~csuder/206/"},
        {'name': "SSS", 'title': "Shatner Space Station", 'image':"sss_thumb", 'url':"~cleung24/206/"},
        {'name': "MM", 'title': "Memento Mori", 'image':"mm_thumb", 'url':"~ezarou/206/"}]

# Constant listing the default commodities available on every planet, and the range of prices each one might adopt
Commodities = map(lambda x: Commodity(x[0],x[1]), [["Ore",         range(10,20)],
    ["Laser Swords", range(100,200)],
    ["Cheese",       range(2,4)],
    ["Melange",      range(1000,6000)],
    ["Whatever",     range(10,20)]])
