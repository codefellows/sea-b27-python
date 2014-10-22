#!/usr/bin/env python
import cgi

data = FieldStorage()
name = data.getvalue("name", "Anonymous")
friends = data.getlist("friends")

