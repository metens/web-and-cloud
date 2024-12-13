""" 
This is the Flask Python App backend code. This file has the root route ('/'),
the autocomplete route ('/autocomplete'), and the business route ('/business/business_id').
The root route displays the index.html file wich shoes a search bar in the front end.
The autocomplete route is what calls the YELP API to autocomplete businesses that the
user types in. It then redirects that business's place_id into the business route to
be accessed by the GOOGLE API to show the directions from the user's current location.
"""

from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import requests
import os

app = Flask(__name__) # Flask object.
app.secret_key = os.getenv('SECRET') # Used for global session variables.

""" Google Maps Platform Resources:
https://developers.google.com/maps/documentation/directions/get-api-key
https://developers.google.com/maps/documentation/directions/get-directions
"""

""" Yelp Resources:
https://docs.developer.yelp.com/docs/fusion-intro
https://docs.developer.yelp.com/reference/v3_business_search
"""

# API Key from environment variables $GOOGLE_API_KEY and $YELP_API_KEY to keep keys secret:
google_api_key = os.getenv('GOOGLE_API_KEY')
yelp_api_key = os.getenv('YELP_API_KEY')

""" To access the google maps api with an output of json:
https://maps.googleapis.com/maps/api/directions/json?origin=Toronto&destination=Montreal&key=YOUR_API_KEY
"""

# Google Directions API:
google_api_url = 'https://maps.googleapis.com/maps/api'

# All Yelp Fusion API endpoints are under:
yelp_url = 'https://api.yelp.com/v3'

# Root route that displays the frontend for the user to interact:
@app.route('/')
def root():
	return render_template('index.html', google_api_key=google_api_key)

# Autocomplete route accesses YELP's API to autocomplete search for business:
@app.route("/autocomplete", methods=['GET'])
def autocomplete():
	# Get the text, lat, and long from script.js file frontent:
	text = request.args.get('text')
	# Set the lat and long session variables for global backend access:
	latitude = request.args.get('latitude', type=float); session['lat'] = latitude;
	longitude = request.args.get('longitude', type=float); session['long'] = longitude;

	# Headers and params to access YELP's API:
	headers = {'Authorization': f'Bearer {yelp_api_key}'}
	params = {
		"text": text,
		"latitude": latitude,
		"longitude": longitude
	}

	# Call the Yelp API with the api_key and parameters for a response:
	response = requests.get(f"{yelp_url}/autocomplete", headers=headers, params=params)
	
	return jsonify(response.json())

# Access the business details and use them to display info to the user and directions:
@app.route('/business/<string:business_id>', methods=['GET'])
def business(business_id):
	session.clear(); # Reset all session variables to avoid cacheing one business.

	# Call Yelp API for the business details:
	url = f'{yelp_url}/businesses/{business_id}'
	headers = {
		'accept': 'application/json',
		'Authorization': f'Bearer {yelp_api_key}'
	}
	response = requests.get(url, headers=headers)
	business_details = response.json()
	
	# Get important business details and set as global variables for easy access:
	session['name'] = business_details['name']
	session['img'] = business_details['image_url']
	session['url'] = business_details['url']
	session['is_open'] = business_details['hours'][0]['is_open_now']
	session['rating'] = business_details['rating']
	session['phone'] = business_details['phone']
	
	lat = business_details['coordinates']['latitude']
	long = business_details['coordinates']['longitude']
	
	address = ' '.join(business_details['location']['display_address']) # Joins the list elements into a string
	session['dest_address'] = address # Store data in a global session for access between routes.

	############################################################
	## GEOCODING API USE:
	""" Resource: https://developers.google.com/maps/documentation/geocoding/requests-geocoding """
	############################################################
	# Using reverse geocoding Google API to get the place id of the business.
	# The reverse geocoding takes the business lat and long and returns the place_id.
	# The place_id is used in the google maps API to direct the user to their business
	# of choice:
	geocode_url = f'{google_api_url}/geocode/json'
	params = {	
		'address': address,
		'key': google_api_key
	}
	headers = {
		'accept': 'application/json',
		'Authorization': f'Bearer {google_api_key}'
	}
	geo_response = requests.get(geocode_url, headers=headers, params=params)
	place_id = geo_response.json()['results'][0]['place_id']
	
	session['dest_place_id'] = place_id

	############################################################
	## GOOGLE MAPS API USE:
	""" Resource: https://developers.google.com/maps/documentation/directions/get-directions """
	############################################################
	# Using the place_id extracted from the Geocoding API, we can now get a more precise destination:
	google_maps_url = f'{google_api_url}/directions/json'
	params = {
		'destination': f'place_id:{place_id}',
		'origin': f'{lat},{long}',
		'key': google_api_key
	}
	maps_response = requests.get(google_maps_url, headers=headers, params=params)	

	""" The following is used by the 
	static/script.js file to access lat and long
	variables to display the map for directions
	to the user's desired business. """
	data = {
		'name': session.get('name'),
		'img': session.get('img'),
		'url': session.get('url'),
		'is_open': session.get('is_open'),
		'rating': session.get('rating'),
		'phone': session.get('phone'),
		'destination': session.get('dest_address'),
	}
	return jsonify(data)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)
