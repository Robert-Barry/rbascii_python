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
		<input type="text" name="title" value="%(title)s" />
	    </label>
	    <label>
		<div>art</div>
		<textarea name="art">%(art)s</textarea>
	    </label>

	    <div class="error">%(error)s</div>

	    <input type="submit" name="submit" value="Submit" />
	</form>
    </body>
</html>
"""

# Main handler
class MainPage(webapp2.RequestHandler):
    # render the front page
    def render_front(self, title="", art="", error=""):
	self.response.out.write(front_page % {'title': title, 'art':art, 'error': error} )

    # handle get requests
    def get(self):
	# Output text
	self.render_front()

    # handle post requests
    def post(self):
	# get variables
	title = self.request.get("title")
	art = self.request.get("art")
	
	# simple error handling for the variables
	if title and art:
	    self.response.out.write("thanks!")
	else:
	    error = "we need both a title and some artwork!"
	    self.render_front(title, art, error)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)