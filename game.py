import random

Rooms = [{'name': "The Moon", 'title': "The Moon", 'image':"moon_thumb", 'url':"~wliu65/206/"},
         {'name': "Arrakis", 'title': "Arrakis", 'image':"dune_thumb", 'url':"~hbrund/206/"},
         {'name': "Orion", 'title': "The Orion Nebula", 'image':"orion_thumb", 'url':"~csuder/206/"},
         {'name': "SSS", 'title': "Shatner Space Station", 'image':"sss_thumb", 'url':"~cleung24/206/"},
         {'name': "MM", 'title': "Memento Mori", 'image':"memento_thumb", 'url':"~ezarou/206/"},
        ]

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
