#!/usr/bin/env python
# show.py - Renders a room and the price table to stdout
# Usage: Visit /show.py?room=# where # is the room number being shown
import template, game, cgi

# Figure out the room number and grab the room info
form = cgi.FieldStorage()
room_number = int(form.getfirst("room", 1)) # Default of the first room
room = game.Rooms[room_number-1]

# Planet class does all the backend stuff.
planet = game.Planet()

# Get the planet's description from the file
description = template.content("room%d" % room_number, room)

# Get the rows of the price table
table_rows = [template.content("price_table_row", row) for row in planet.market()]

# Get the table using the rows
table = template.content("price_table", dict(rows = ''.join(table_rows)))

# Get the map for use in the footer
def room_url(index):
    if index == 0:
        return 'http://www.cs.mcgill.ca/~llehne/room-page/room-page.html'
    elif index == 6:
        return 'http://cs.mcgill.ca/~ztrifi/myPage.html'
    else:
        return 'show.py?room=%d' % index

footer_rows = ""
for i,r in enumerate(game.Rooms):
    footer_rows += template.content("footer_row", {'room_name': r['name'], 
                                                   'image_url': "images/"+r['image']+".jpg", 
                                                   'room_url':  room_url(i + 1),
                                                   'room_id': i+1})
# IF THE USER HAS GOTTEN HERE BY LEGITIMATE MEANS
# working on this
if form.has_key("LOL"):
    # Render the room template
    template.render("room", {'page_title': room['title'] + form["LOL"].value, 
                             'page_name': "room%d" % room_number, 
                             'description': description, 
                             'table': table, 
                             'footer_rows': footer_rows,
                             'left_url': room_url(room_number-1),
                             'right_url':room_url(room_number+1)})
else:
    # Go back to the login page teehee
    template.render("login", dict(page_title="Login", layout="logged_out"))
