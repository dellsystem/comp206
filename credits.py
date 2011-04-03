#!/usr/bin/env python
# this rudimentary template engine does all the header/footer printing shit, to avoid duplication
import template
template.render("credits", dict(page_title="Credits", layout="logged_out"))
