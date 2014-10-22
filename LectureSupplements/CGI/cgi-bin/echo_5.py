#!/usr/bin/env python
import cgi
import cgitb

cgitb.enable()

data = cgi.FieldStorage()
name = data.getvalue("name", "Anonymous")
friends = data.getlist("friends")

