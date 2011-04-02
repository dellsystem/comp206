import random

class Commodity:
    def __init__(self, name, prices):
        self.name = name
        self.prices = prices

Commodities = map(lambda x: Commodity(x[0],x[1]), [["Ore",          range(10,20)],
                                                   ["Laser Swords", range(100,200)], 
                                                   ["Cheese",       range(2,4)], 
                                                   ["Melange",      range(1000,6000)], 
                                                   ["Whatever",     range(10,20)]])

class Planet:
    def __init__(self):
        self.market = map(lambda com: dict(commodity=com, price=random.choice(com.prices)), Commodities)

class Inventory:
    pass
    #def __init__(self):

    #def _read(self):

    #def _write(self):
