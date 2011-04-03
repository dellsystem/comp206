#!/usr/bin/env python
import template, game

room_number = 2
room = game.Rooms[room_number-1]
planet = game.Planet()

# Get the planet's descriptiong from the file
description = template.content("room{0}".format(room_number), room)

# Get the rows of the price table
table_rows = [template.content("price_table_row", dict(item_name=row['commodity'].name)) for row in planet.market]

# Get the table using the rows
table = template.content("price_table", dict(rows = ''.join(table_rows)))

# Render the room template
template.render("room", dict(page_title=room['title'], page_name="room{0}".format(room_number), description=description, table=table))
