#!/usr/bin/env python
#
# ASCII ART
# A program allowing users to upload ascii art for exhibiting
# on the web.
#
# AUTHOR: Robert Barry
# DATE CREATED: July 22, 2012
# DATE CHANGED: August 21, 2012
# WEB ADDRESS: http://rbascii.appspot.com/

import os
import urllib2
import webapp2
import logging

from xml.dom import minidom

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


	    form {
		float: left;
	    }

	    .map {
		margin-left: 10px;
		margin-top: 20px;
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
		clear: left;
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

	%(map)s

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

IP_URL = "http://api.hostip.info/?ip="
GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"

def get_coords(ip):
    url = IP_URL + ip
    content = None
    try:
	content = urllib2.urlopen(url).read()
    except URLError:
	return

    if content:
	d = minidom.parseString(content)
	coords = d.getElementsByTagName("gml:coordinates")
	if coords and coords[0].childNodes[0].nodeValue:
	    lon, lat = coords[0].childNodes[0].nodeValue.split(',')
	    return db.GeoPt(lat, lon)

def gmaps_img(points):
    markers = "&".join("markers=%s,%s" % (p.lat, p.lon) for p in points)
    return GMAPS_URL + markers

# Create the database
class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    coords = db.GeoPtProperty()

CACHE = {}
def top_arts():
    key = 'top'
    
    if key in CACHE:
	arts = CACHE[key]
    else:
        logging.error("DB QUERY")
        # make the query
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC LIMIT 10")

        # Prevent the running of multiple queries
        arts = list(arts)
	CACHE[key] = arts
    
    return arts


# Main handler
class MainPage(webapp2.RequestHandler):
    # render the front page with art from the database
    def render_front(self, title="", art="", error=""):
	
	arts = top_arts()

	# Find which arts have coordinates set
	points = []
	for a in arts:
	    if a.coords:
		points.append(a.coords)

	# If we have any arts coords, make an image url
	# display the image url
	img_url = None
	map = ""
	if points:
	    img_url = gmaps_img(points)
	    map = '<img src="%s" class="map" />' % img_url


	art_images = "" # creates inner html for art
	# loop through each entity in database and write to page
	for each_art in arts:
	    art_images = art_images + (art_db % {'art_title': each_art.title, 'art_body': each_art.art })
	    
	self.response.out.write(front_page % {'title': title, 'art': art, 'error': error, 'art_images': art_images, 'map': map } )

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
	    # Lookup the user's coordinates from their IP
	    coords = get_coords(self.request.remote_addr)
	    # If we have coordinates, add them to the Art
	    if coords:
		a.coords = coords

	    a.put()
	    CACHE.clear()

	    # render the page with the art
	    self.redirect("/")
	else:
	    error = "we need both a title and some artwork!"
	    self.render_front(title, art, error)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)