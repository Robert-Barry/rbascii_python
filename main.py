#!/usr/bin/env python
#
# ASCII ART
# A program allowing users to upload ascii art for exhibiting
# on the web.
#
# AUTHOR: Robert Barry
# DATE CREATED: July 22, 2012
# DATE CHANGED: July 22, 2012
# WEB ADDRESS: http://rbascii.appspot.com/

import os
import webapp2

from google.appengine.ext import db

# HTML front page test 1
front_page = """
<html>
    <head>
	<title>/ascii/</title>
    </head>

    <body>
	<h1>/ascii/</h2>

	<form method="post">
	    <label>
	        <div>title</div>
		<input type="text" name="title" />
	    </label>
	    <label>
		<div>art</div>
		<textarea name="art"></textarea>
	    </label>
	</form>
    </body>
</html>
"""

# Main handler
class MainPage(webapp2.RequestHandler):
    def get(self):
	# Output text
	self.response.out.write(front_page)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)