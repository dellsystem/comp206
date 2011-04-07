#!/usr/bin/env python
# show.py - Renders a room and the price table to stdout
# Usage: Visit /show.py?room=# where # is the room number being shown
import template, game, cgi

try:
    # Figure out the room number and grab the room info
    form = cgi.FieldStorage()
    # Note: "room" is a POST variable, not GET anymore
    room_number = int(form.getfirst("room", 1)) # Default of the first room
    room = game.Rooms[room_number-1]

    # Get the user's inventory.
    # IF THE USER HAS GOTTEN HERE BY LEGITIMATE MEANS
    # Only logged in if there's a points input field
    # This will be true if we're coming from another game/room/login
    # Will raise an exception if the required info isn't present, and
    # send the user back to the login page (see below)
    user_inventory = game.UserInventory(form)

    # Planet class does all the backend stuff.
    planet = game.Planet(user_inventory, form, room_number)

    errors_or_new_points = planet.commit_purchase_order()
    if isinstance(errors_or_new_points, list):
      # There were errors processing the buy form. Redisplay form with errors.
      error_text = '<div class="errors pulsed_red">' + "<br/>".join(errors_or_new_points) + "</div>"
    else:
      # The inventory commited the transaction without errors. Write it to disk.
      user_inventory.points = errors_or_new_points
      planet.inventory.write()
      error_text = ""

    # Render all the stuff: the user's inventory, the price table, the planet's description, and the footer map.

    # Render the user's inventory once, its put in a while bunch of places
    points_form = user_inventory.render()

    # Get the rows of the price table, so we can then pass it to the table
    table_rows = [template.content("price_table_row", dict(num=i, **row)) for i, row in enumerate(planet.market())]
    # Get the table using the rows
    table = template.content("price_table", {'rows':''.join(table_rows), 'points_form': points_form})

    # Get the map for use in the footer
    def room_url(index):
        if index == 0:
            return 'http://www.cs.mcgill.ca/~llehne/room-page/room-page.html'
        elif index == 6:
            return 'http://cs.mcgill.ca/~ztrifi/myPage.html'
        else:
            return 'show.py'

    footer_rows = ""
    for i,r in enumerate(game.Rooms):
        footer_rows += template.content("footer_row", {'room_name': r['name'],
                                                       'image_url': "images/"+r['image']+".jpg",
                                                       'room_url':  room_url(i + 1),
                                                       'room_id': i+1, 
                                                       'points_form': points_form})

    # Get the planet's description from the file
    description = template.content("room%d" % room_number, room)

    # Render the room template
    template.render("room", {'page_title': room['title'],
                             'page_name': "room%d" % room_number,
                             'description': description,
                             'table': table,
                             'errors': error_text,
                             'points': user_inventory.points,
                             'footer_rows': footer_rows,
                             'left_url': room_url(room_number-1),
                             'left_room': room_number-1,
                             'right_url': room_url(room_number+1),
                             'right_room': room_number+1,
                             'points_form': points_form})

except game.MalformedGameFormError:
    # Go back to the login page teehee
    template.render("login", dict(page_title="Login", layout="logged_out"))
