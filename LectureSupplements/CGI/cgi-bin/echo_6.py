#!/usr/bin/env python
import cgi
import cgitb

cgitb.enable()

data = cgi.FieldStorage()
name = data.getvalue("name", "Anonymous")
friends = data.getlist("friends")

print """
<html>
<head>
   <title>Info Echo</title>
</head>
<body>
<h1>Welcome %s</h1>
</body>
</html>""" % (name,)
