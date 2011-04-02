#!/usr/bin/env python
# For experimenting with layouts (calling the html files in the layout dir)
import cgi
# for error messages
import cgitb
cgitb.enable()

print "Content-type: text/html"
print

page_title = "Sandbox"

# Open the header template file, print it to the screen
header = open('layout/header.html', 'r')
# First replace {PAGE_TITLE} with the actual page title
header_str = header.read()
header_str = header_str.replace('{PAGE_TITLE}', page_title)
header.close()

print header_str

print "test - contents of page go here blah blah"

footer = open('layout/footer.html', 'r')
# Nothing to replace ... just print it out with a loop
for line in footer:
    print line,

