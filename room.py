#!/usr/bin/env python
# Sample room page - won't actually be used
# Just for testing how room pages could be generated
# Could be incorporated into show/activity.py later
import template

# Define a dictionary for each room's name
rooms = {1: 'The moon', 2: 'Arrakis', 3: 'The Orion Nebula', 4: 'Shatner Space Station', 5: 'Memento Mori'}

# Make it room one unless specified otherwise
room_number = 1

page_title = rooms[1]
template.header(page_title)
template.content('room' + str(room_number))

# Map stuff ... only valid in the rooms page, but defined in template
# Pass it the room number, will make it opaque
template.map(room_number)
# Uses a different footer so we don't need the standard one
