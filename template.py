import cgi, cgitb, re
cgitb.enable() # for error messages

# Vendored version of string.Template from 2.7 for friggen gimpy ass Python 2.3 on the webserver
# Taken from http://svn.python.org/view/python/branches/release27-maint/Lib/string.py?view=markup
# from string import Template
class _TemplateMetaclass(type):
    pattern = r"""
    %(delim)s(?:
      (?P<escaped>%(delim)s) |   # Escape sequence of two delimiters
      (?P<named>%(id)s)      |   # delimiter and a Python identifier
      {(?P<braced>%(id)s)}   |   # delimiter and a braced identifier
      (?P<invalid>)              # Other ill-formed delimiter exprs
    )
    """

    def __init__(cls, name, bases, dct):
        super(_TemplateMetaclass, cls).__init__(name, bases, dct)
        if 'pattern' in dct:
            pattern = cls.pattern
        else:
            pattern = _TemplateMetaclass.pattern % {
                'delim' : re.escape(cls.delimiter),
                'id'    : cls.idpattern,
                }
        cls.pattern = re.compile(pattern, re.IGNORECASE | re.VERBOSE)


class Template:
    """A string class for supporting $-substitutions."""
    __metaclass__ = _TemplateMetaclass

    delimiter = '$'
    idpattern = r'[_a-z][_a-z0-9]*'

    def __init__(self, template):
        self.template = template

    # Search for $$, $identifier, ${identifier}, and any bare $'s

    def _invalid(self, mo):
        i = mo.start('invalid')
        lines = self.template[:i].splitlines(True)
        if not lines:
            colno = 1
            lineno = 1
        else:
            colno = i - len(''.join(lines[:-1]))
            lineno = len(lines)
        raise ValueError('Invalid placeholder in string: line %d, col %d' %
                         (lineno, colno))

    def substitute(self, *args, **kws):
        if len(args) > 1:
            raise TypeError('Too many positional arguments')
        if not args:
            mapping = kws
        elif kws:
            mapping = _multimap(kws, args[0])
        else:
            mapping = args[0]
        # Helper function for .sub()
        def convert(mo):
            # Check the most common path first.
            named = mo.group('named') or mo.group('braced')
            if named is not None:
                val = mapping[named]
                # We use this idiom instead of str() because the latter will
                # fail if val is a Unicode containing non-ASCII characters.
                return '%s' % (val,)
            if mo.group('escaped') is not None:
                return self.delimiter
            if mo.group('invalid') is not None:
                self._invalid(mo)
            raise ValueError('Unrecognized named group in pattern',
                             self.pattern)
        return self.pattern.sub(convert, self.template)

    def safe_substitute(self, *args, **kws):
        if len(args) > 1:
            raise TypeError('Too many positional arguments')
        if not args:
            mapping = kws
        elif kws:
            mapping = _multimap(kws, args[0])
        else:
            mapping = args[0]
        # Helper function for .sub()
        def convert(mo):
            named = mo.group('named')
            if named is not None:
                try:
                    # We use this idiom instead of str() because the latter
                    # will fail if val is a Unicode containing non-ASCII
                    return '%s' % (mapping[named],)
                except KeyError:
                    return self.delimiter + named
            braced = mo.group('braced')
            if braced is not None:
                try:
                    return '%s' % (mapping[braced],)
                except KeyError:
                    return self.delimiter + '{' + braced + '}'
            if mo.group('escaped') is not None:
                return self.delimiter
            if mo.group('invalid') is not None:
                return self.delimiter
            raise ValueError('Unrecognized named group in pattern',
                             self.pattern)
        return self.pattern.sub(convert, self.template)


# Here's where our code starts.
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
    
    if 'layout' not in data:
        # Set the default layout for the rendering
        data['layout'] = 'application'

    print content(data['layout'], data) # Render the body inside the application layout
    return True

def content(name, data):
    renderable = PartialRenderer()
    renderable.update(data)
    f = open('layout/' + name + '.html', 'r')
    template = Template(f.read())
    f.close()
    return template.substitute(renderable)
