#!/usr/bin/env python
import template, game, cgi

form = cgi.FieldStorage()

room_number = int(form.getfirst("room", 1))
room = game.Rooms[room_number-1]
planet = game.Planet()

# Get the planet's descriptiong from the file
description = template.content("room{0}".format(room_number), room)

# Get the rows of the price table
table_rows = [template.content("price_table_row", {'item_name': row['commodity'].name}) for row in planet.market]

# Get the table using the rows
table = template.content("price_table", dict(rows = ''.join(table_rows)))

# Get the map for use in the footer

def room_url(index):
    return 'show.py?room={0}'.format(index)

footer_rows = ""
for i,r in enumerate(game.Rooms):
    footer_rows += template.content("footer_row", {'room_name': r['name'], 
                                                   'image_url': "images/"+r['image']+".jpg", 
                                                   'room_url':  room_url(i + 1)})
# Render the room template
template.render("room", {'page_title': room['title'], 
                         'page_name': "room{0}".format(room_number), 
                         'description': description, 
                         'table': table, 
                         'footer_rows': footer_rows,
                         'left_url': room_url((room_number-2) % 5 + 1),
                         'right_url':room_url((room_number) % 5 + 1)})
