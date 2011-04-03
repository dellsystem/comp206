#!/usr/bin/env python
# this rudimentary template engine does all the header/footer printing shit, to avoid duplication
import template
template.render("home", dict(page_title="Welcome", page_name="welcome", layout="logged_out"))
