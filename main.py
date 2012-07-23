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

	<style>
	    body {
		font-family: sans-serif;
		width: 800px;
		margin: 0 auto;
		padding: 10px;
	    }

	    .error {
		color: red;
	    }

	    label {
		display: block;
		font-size: 20px;
	    }

	    input[type=text] {
		width: 400px;
		font-size: 20px;
		padding: 2px;
	    }

	    textarea {
		width: 400px;
		height: 200px;
		font-size: 17px;
		font-family: monospace;
	    }

	    input[type=submit] {
		font-size: 24px;
	    }

	    hr {
		margin: 20px auto;
	    }

	    .art + .art {
		margin-top: 20px;
	    }

	    .art-title {
		font-weight: bold;
	        font-size: 20px;
	    }

	    .art-body {
		margin: 0;
		font-size: 17px;
	    }
	</style>
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

	<hr />

	%(art_images)s
	
    </body>
</html>
"""

art_db = """
	<div class="art">
	    <div class="art-title">%(art_title)s</div>
	    <pre class="art-body">%(art_body)s</pre>
	</div>
"""

# Create the database
class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

# Main handler
class MainPage(webapp2.RequestHandler):
    # render the front page with art from the database
    def render_front(self, title="", art="", error=""):
	# make the query
	arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
	art_images = "" # creates inner html for art
	# loop through each entity in database and write to page
	for each_art in arts:
	    art_images = art_images + (art_db % {'art_title': each_art.title, 'art_body': each_art.art })
	    
	self.response.out.write(front_page % {'title': title, 'art': art, 'error': error, 'art_images': art_images } )

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
	    # add the title and art to the database
	    a = Art(title = title, art = art)
	    a.put()
	    # render the page with the art
	    self.redirect("/")
	else:
	    error = "we need both a title and some artwork!"
	    self.render_front(title, art, error)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)