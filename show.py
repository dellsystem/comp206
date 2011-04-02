#!/usr/bin/env python
import template, game

description = template.content("room1", dict())
planet = game.Planet()

# Get the rows of the price table
table_rows = [template.content("price_table_row", dict(item_name=row['commodity'].name)) for row in planet.market]
# Get the table using the rows
table = template.content("price_table", dict(rows = ''.join(table_rows)))
# Render the room template
template.render("room", dict(page_title="Room X", description=description, table=table))
