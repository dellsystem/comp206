# game.py - implementation of the commodity trading game including inventory reading and writing
import random, re
import cgi # Just for escaping, whatever

# Global function for validating points
# Pass it a string that you want to be the points
# Will return either an int representation of it, or 0 if not possible
# Means that you can't ever have negative or non-integer points
def validate_points(points):
    try:
        points = int(points)
    except ValueError:
        points = 0
    if points < 0:
        points = 0
    return points

# Global function for validating the price
# Has to be a non-negative integer
def validate_price(price):
    try:
        price = int(price)
    except ValueError:
        raise

    # Throw an invalid price error
    if price <= 0:
        raise ValueError
    else:
        return price

# Global function for validating quantities
# Has to be 0 or greater
def validate_quantity(quantity):
    try:
        quantity = int(quantity)
    except ValueError:
        raise

    if quantity < 0:
        raise ValueError
    else:
        return quantity

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
    # Initializes an InventoryItem from a line in a CSV
    def fromCSV(entry):
        values = entry.split(',')
        if not len(values) == 2:
            raise MalformedCSVError
        return InventoryItem(*values)
    fromCSV = staticmethod(fromCSV)

    def __init__(self, commodity_name, quantity):
        self.quantity = int(quantity)
        self.commodity_name = commodity_name
        commodities = filter( lambda x: x.name == commodity_name , Commodities)
        if commodities:
            self.commodity = commodities[0]
        else:
            if not re.search('Space Junk \((.+)\)', self.commodity_name):
                # First escape some shit
                commodity_name = cgi.escape(commodity_name)
                commodity_name = commodity_name.replace('"', '&quot;')
                self.commodity_name = "Space Junk (%s)" % commodity_name
            else:
                # Escape shit anyway ... baaaad exploit
                commodity_name = cgi.escape(commodity_name)
                commodity_name = commodity_name.replace('"', '&quot;')
                self.commodity_name = commodity_name
                # T_T my fault for not noticing this before

    # Renders out a representation of this item as a row for CSV
    def getCSV( self ):
        return '%s,%d\n' % (self.commodity_name, self.quantity)


# Inventory class which the PlanetInventory and UserInventory classes extend.
# Add items using addItem, change their quantity by using updateQuantity,
# and delete items by updating their quantity to be 0.
class Inventory:

    # Method to add a new item to the inventory. This is nessecary because we need to
    # track and update both the #items and #items_dict containers.
    def addItem(self, item):
        # Ensure items are unique
        if item.commodity_name in self.items_dict:
            self.updateQuantity(item.commodity_name, item.quantity)
        else:
            self.items.append(item)
            self.items_dict[item.commodity_name] = item

    def updateQuantity(self, item_name, quantity):
        # Ensure the Inventory has an InventoryItem representing this item.
        if item_name not in self.items_dict:
            self.addItem(InventoryItem(item_name, 0))

        item = self.items_dict[item_name]

        item.quantity += quantity
        if item.quantity <= 0:
            del self.items_dict[item_name]
            self.items = filter(lambda item: item.commodity_name != item_name, self.items)

    # Sets the user's inventory to empty
    def empty(self):
        self.items = []
        self.items_dict = {}

# Class which represents the collection of currently available items, and manages reading and writing this to disk
class PlanetInventory(Inventory):
    def __init__(self, room_number):
        self.filename = "database/inventory" + str(room_number) + ".csv"
        self.backup_file = "database/inventory" + str(room_number) + "_initial.csv"
        self.read() # Grab the inventory items upon creation

    # Function for reloading the inventory of a planet
    # Called when inventoryx.csv gets broken
    # The above should never happen, though
    # Also called when we force reset
    # This is done upon logging in
    # And we can reset individual planets by doing:
    # show.py?points=100&room=x&reset=this
    def reload_inventory(self):
        inv_file = open(self.filename, 'w')
        backup_file = open(self.backup_file, 'r')
        backup_inventory = backup_file.readlines()
        for entry in backup_inventory:
            inv_file.write(entry)
        inv_file.close()

        # Now reset the item inventory to 0 or we get problems
        self.items = []

        return

    # Reads and initializes the items in the inventory from CSV.
    def read(self):
        inv_file = open(self.filename, 'r')
        inventory = inv_file.readlines()
        inv_file.close()

        self.empty()
        for entry in inventory:
            entry.strip('\n')
            # We try to load the inventory from the file, and if we are unsuccessful
            # we revert to a known, solid backup.
            try:
                new_item = InventoryItem.fromCSV(entry)
                self.addItem(new_item)
            except MalformedCSVError:
                self.reload_inventory()
                self.read()
        return self.items

    # Writes out the items to CSV.
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

# Class which manages a User's inventory, marshalling to and back from a CGI POST form.
class UserInventory(Inventory):
    def __init__(self, form):
        # Validate user form
        if "points" not in form:
            raise MalformedGameFormError()
        else:
            self.points = validate_points(form.getfirst("points"))

        # Init tracking containers
        self.empty()

        # Add all the inventory items we can to this object
        inventory = {} # Use this to track potential duplicates
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

                self.addItem(item)

    # Get the CGI form elements which represent the user's inventory
    def render(self):
        s = '<input type="hidden" name="points" value="' + str(self.points) + '" />'
        j = 0
        for i, item in enumerate(self.items):
            j += 1
            s += '<input type="hidden" name="Inventory' + str(i+1) + '" value="' + str(item.quantity) + ' ' + item.commodity_name + '" />'
        for i in range(j, 5): # Build up the inventory to always be 5 items long for other sites which can't deal with less than 5
            s += '<input type="hidden" name="Inventory' + str(i+1) + '" value="" />'
        return s

# Class which represents an inventory full of items which may or may not be part of the commodities
class Planet:
    def __init__(self, user_inventory, form, room):
        self.inventory = PlanetInventory(room)
        self.user_inventory = user_inventory
        self.form = form
        self.setMarket()

    # Build a nice, easily traversed representation of the planet's and user's inventory in one nice
    # convenient dict of dicts.
    def setMarket(self):
        market = {}
        # The market has all the standard commodities by default.
        for com in Commodities:
            # Gets an inventory item using the submitted price if its given, and lets the
            # commodity pick one otherwise.
            market[com.name] = com.toInventoryDict()
            key = 'price_'+com.name
            if key in self.form:
                market[com.name]['price'] = self.form.getfirst(key)
            else:
                market[com.name]['price'] = random.choice(com.prices)

        # Loop through the items in the planet's inventory. If its a standard item, then
        # add the quantity to the existing item. If its non standard, add it to the list.
        # Notice that here, the quantity of the inventory item represents the quantity
        # the planet has to sell to the user, so we put it in the 'available_quantity' key.
        for item in self.inventory.items:
            if item.commodity_name in market:
                market[item.commodity_name]['available_quantity'] += item.quantity
            else:
                market[item.commodity_name] = {'name': item.commodity_name, 'quantity': 0, 'available_quantity': item.quantity}

        # Loop through the items in the user's inventory. If its a standard item, then
        # add the quantity to the existing item. If its non standard, add it to the list.
        # Notice that here, the quantity of the inventory item represents the quantity the
        # user has to sell, so we put it in the 'quantity' key.
        for item in self.user_inventory.items:
            if item.commodity_name in market:
                market[item.commodity_name]['quantity'] += item.quantity
            else:
                market[item.commodity_name] = {'name': item.commodity_name, 'quantity': item.quantity, 'available_quantity': 0}

        for key, item in market.iteritems():
            if 'price' not in item:
                market[key]['price'] = random.choice([1,2,3])

        # Return a list for easy processing
        self.market = [row for key, row in market.iteritems()]
        return self.market

    # Apply the buy/sell orders contained in the form. If they can be successfully applied, then this returns
    # the new number of points the user has. If they can't be applied for any reason, an array of string reasons
    # is returned, suitable for showing the user.
    def commit_purchase_order(self):
        errors = [] # List of strings describing issues (if any) with the form
        commits = [] # List of name, quantity dicts to be applied to the planet's inventory and the user's inventory if there are no errors

        if 'points' not in self.form:
            errors.append("Malformed form, please try submitting again!")
            return errors
        else:
            # Validate points, in case someone is messing around
            points = validate_points(self.form.getfirst('points'))

        for key in self.form:
            m = re.search("com_name_([0-9]+)", key)
            # Search all the form keys for things matching our set
            if not not m:
                num = m.group(1)

                # Qty, action, price group found. Check all values are present
                commodity_name = self.form.getfirst("com_name_"+num)
                quantity = self.form.getfirst("qty_"+num)
                action = self.form.getfirst("action_"+num)
                price = self.form.getfirst("price_"+num)

                # Check for the presence of fields
                if not commodity_name or not quantity or not action or not price:
                    errors.append("Malformed form, please try submitting again!")
                    break

                # Validate the price
                try:
                   price = validate_price(price)
                   # pass
                # If the price is invalid
                except ValueError:
                    errors.append("Stop trying to break my vases I promise you there are no rupees in them")
                    break

                # Validate the quantity
                try:
                   quantity = validate_quantity(quantity)
                except ValueError:
                    errors.append("Why can't you buy things in regular quantities like normal people? Jeez")
                    break

                # Make sure we're not being passed commas
                if commodity_name.find(',') is not -1:
                    errors.append('Malformed form (commas are not allowed in item names), please stop trying to break our site!') 

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
                        commits.append({'name':commodity_name, 'quantity': -1 * quantity})

                    elif action == "sell":
                        if not commodity_name in self.user_inventory.items_dict:
                            errors.append("You can't sell "+commodity_name+" because you don't have any! Tisk!")
                            continue

                        if quantity > self.user_inventory.items_dict[commodity_name].quantity:
                            errors.append("You can't sell more "+commodity_name+" than you have, sorry.")
                            continue

                        points += price * quantity
                        commits.append({'name': commodity_name, 'quantity': quantity})
                    else:
                        errors.append("Malformed form, please try submitting again!")
                        break

        # Check that the user has enough points to apply the commits
        if points < 0:
            errors.append("You don't have enough money for these transactions, sorry.")

        # Check if the user will end up with more than 5 items. For this, we need to "mock" apply all the
        # transactions to the inventory, and check the items count of the final result. This is unfortunately
        # inefficient, but we don't have a database with transaction support, so, sorry?

        # Get a dict of the itemname -> quantity of the user's inventory
        final_items = dict(map(lambda x: (x.commodity_name, x.quantity), self.user_inventory.items))

        # Apply the commits to this mock inventory
        for commit in commits:
            if commit['name'] in final_items:
                final_items[commit['name']] -= commit['quantity']
            else:
                final_items[commit['name']] = -1 * commit['quantity']

        # Check if the result (without empty inventory items) has more than 5 items
        if len(filter(lambda (k, v): v > 0, final_items.iteritems())) > 5:
            errors.append("You can only carry five items at a time! Sell some to free up your inventory.")

        if len(errors) > 0:
            return errors
        else:
            # No errors, commit all the quantity changes to the inventories
            for commit in commits:
                self.user_inventory.updateQuantity(commit['name'], -1 * commit['quantity'])
                self.inventory.updateQuantity(commit['name'], commit['quantity'])
                self.setMarket()

            return points

    def userAssetValue(self):
        return reduce(lambda acc, x: acc + (x['quantity'] * x['price']), self.market, 0)

# Constant listing all the rooms and their attributes
Rooms = [{'name': "The Moon", 'title': "The Moon", 'image':"moon_thumb", 'url':"~wliu65/206-5/"},
        {'name': "Arrakis", 'title': "Arrakis", 'image':"arrakis_thumb", 'url':"~hbrund/comp206-5/"},
        {'name': "Orion", 'title': "The Orion Nebula", 'image':"orion_thumb", 'url':"~csuder/ass5/"},
        {'name': "SSS", 'title': "Shatner Space Station", 'image':"sss_thumb", 'url':"~cleung24/comp206-5/"},
        {'name': "MM", 'title': "Memento Mori", 'image':"mm_thumb", 'url':"~ezarou/ass5/"}]

# Constant listing the default commodities available on every planet, and the range of prices each one might adopt
Commodities = map(lambda x: Commodity(x[0],x[1]), [["Ore",         range(10,20)],
    ["Laser Swords", range(100,200)],
    ["Green Cheese",       range(2,4)],
    ["Melange",      range(1000,2000)],
    ["Purple Cloud Candy",     range(10,30)],
    ["Water", range(5, 10)],
    ["Moon Dust", range(70, 90)],
    ["Faerie Dust", range(50, 80)],
    ["Serum of Life", range(500, 1000)],
    ["Manthrax", range(800, 900)]])
