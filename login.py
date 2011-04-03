#!/usr/bin/env python
# this rudimentary template engine does all the header/footer printing shit, to avoid duplication
import template
template.render("login", dict(page_title="Login", layout="logged_out"))
