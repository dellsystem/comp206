import cgi, cgitb, re
cgitb.enable() # for error messages
from string import Template

partialCheck = re.compile("^partial(.+)$")

class PartialRenderer(dict):
    def __getitem__(self, key):
        # Check for nonexistent items in the dict, and render them if they are partials
        if key not in self:
            name = partialCheck.search(key)
            # Render the doo dad
            if name:
                return content(name.group(1), self)

        return super(PartialRenderer, self).__getitem__(key) # If its not a partial call, do the standard stuff

def render(name, data):
    print "Content-type: text/html"
    print
    
    if 'body' not in data:
        # Render the body from a template
        data['body'] = content(name, data)    

    if 'page_name' not in data:
        # Assign the page name so we can use it as a css class    
        data['page_name'] = name

    print content("application", data) # Render the body inside the application layout
    return true

def content(name, data):
    renderable = PartialRenderer()
    renderable.update(data)
    f = open('layout/' + name + '.html', 'r')
    template = Template(f.read())
    f.close()
    return template.substitute(renderable)
