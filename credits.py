#!/usr/bin/env python
# this rudimentary template engine does all the header/footer printing shit, to avoid duplication
import template

page_title = "Credits"

# Call the function for displaying the header - pass it the title
template.header(page_title)

# Call the function for showing the content - pass it the name of the html file
template.content('credits')

template.footer()
