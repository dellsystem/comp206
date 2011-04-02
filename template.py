import cgi
import cgitb
cgitb.enable() # for error messages

# Function for printing out the header of a page
def header(page_title):
    print "Content-type: text/html"
    print
    
    header_file = open('layout/header.html', 'r')
    # Replace {PAGE_TITLE} with the actual page title
    header_str = header_file.read()
    header_str = header_str.replace('{PAGE_TITLE}', page_title)
    header_file.close()

    print header_str

# Function for printing out the content of a page - pass it the html file name (without the .html extension)
def content(filename):
    content = open('layout/' + filename + '.html', 'r')
    for line in content:
        print line,

# Function for printing out the footer of a page
def footer():
    footer = open('layout/footer.html', 'r')
    # Nothing to replace ... just print it out with a loop
    for line in footer:
        print line,
