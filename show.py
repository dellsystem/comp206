#!/usr/bin/env python
# show.py - Renders a room and the price table to stdout
# Usage: Send the room number as a post variable (named room)
import template, game, cgi, os

try:
    # Figure out the room number and grab the room info
    form = cgi.FieldStorage()
    try:
        room_number = int(form.getfirst("room", 1)) # Default of the first room
        # Make sure room is between 1 and 5, inclusive
        if room_number < 1 or room_number > 5:
            room_number = 1 # defaults to the moon
    # If we get passed an invalid room number
    except ValueError:
        room_number = 1
    room = game.Rooms[room_number-1]
    
    # If we need to reload each planet's inventory
    # Should only occur when someone is logging in for the first time
    # Or if we need to force reset for some reason
    reset = form.getfirst("reset", 0)
    if reset == "all":
        # Reload every planet's inventory
        for i in range(5):
            planet_inventory = game.PlanetInventory(i+1)
            planet_inventory.reload_inventory()
    elif reset is not 0:
        # We have to reset one of the planet's inventories ... which?
        try:
           pass 
        except ValueError:
            # Trying an illegal operation T_T """
            pass

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

    # Get the stats for the user's inventory
    asset_value = planet.userAssetValue()
    net_worth = asset_value + user_inventory.points

    # Render all the stuff: the user's inventory, the price table, the planet's description, and the footer map.
    # Render the user's inventory once, its put in a while bunch of places
    points_form = user_inventory.render()

    # Get the rows of the price table, so we can then pass it to the table
    table_rows = []
    for i, row in enumerate(planet.market):
        d = dict(num=i, **row)
        if d['quantity'] == 0:
            d['buy_selected'] = 'selected="selected"'
            d['sell_selected'] = ''
        else:
            d['buy_selected'] = ''
            d['sell_selected'] = 'selected="selected"'

        for key in ['available_quantity', 'quantity']:
            if d[key] > 0:
                d[key] = "<b>%d</b>" % d[key]
            else:
                d[key] = "<span class=\"boring\">%d</span>" % d[key]


        table_rows.append(template.content("price_table_row", d))

    # Get the table using the rows
    table = template.content("price_table", {'rows':''.join(table_rows),
                                             'points_form': points_form,
                                             'room_id': room_number,
                                             'points': user_inventory.points,
                                             'asset_value': asset_value,
                                             'net_worth': net_worth})

    # Get the map for use in the footer
    def room_url(index):
        if index == 0:
            return 'http://cs.mcgill.ca/~llehne/ass5/cgi-bin/show.py'
        elif index == 6:
            return 'http://cs.mcgill.ca/~ztrifi/myPage.html'
        else:
            # Uses the list Rooms in game.py
            # Gets the URL for each room
            # So we can each host our own room, lol
            if os.path.exists("./development_mode"):
              return 'show.py'
            else:
              return 'http://cs.mcgill.ca/' + game.Rooms[index-1]['url'] + 'show.py'

    footer_rows = ""
    for i,r in enumerate(game.Rooms):
        footer_rows += template.content("footer_row", {'room_name': r['name'],
                                                       'room_url': room_url(i),
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
                             'asset_value': asset_value,
                             'net_worth': net_worth,
                             'footer_rows': footer_rows,
                             'left_url': room_url(room_number-1),
                             'left_room': room_number-1,
                             'right_url': room_url(room_number+1),
                             'right_room': room_number+1,
                             'points_form': points_form})

except game.MalformedGameFormError:
    # Go back to the login page teehee
    template.render("login", dict(page_title="Login", layout="logged_out"))
