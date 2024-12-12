from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import requests
import os

app = Flask(__name__) # Flask object
app.secret_key = 'temporary_secret'

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

"""To access the google maps api with an output of json:
https://maps.googleapis.com/maps/api/directions/json?origin=Toronto&destination=Montreal&key=YOUR_API_KEY
"""
# Google Directions API:
google_api_url = 'https://maps.googleapis.com/maps/api'

# All Yelp Fusion API endpoints are under:
yelp_url = 'https://api.yelp.com/v3'

@app.route('/')
def root():
	return '<h1>Nothing Here, move along!</h1>'

@app.route("/autocomplete", methods=['GET'])
def autocomplete():
	""" This method is called from the script.js file 
	located in the static dir """

	# Get the text, lat, and long from script.js file frontent:
	text = request.args.get('text')
	latitude = request.args.get('latitude', type=float)
	longitude = request.args.get('longitude', type=float)

	headers = {'Authorization': f'Bearer {yelp_api_key}'}
	params = {
		"text": text,
		"latitude": latitude,
		"longitude": longitude
	}

	# Call the Yelp API with the api_key and parameters for a response:
	response = requests.get(f"{yelp_url}/autocomplete", headers=headers, params=params)
	return jsonify(response.json())
	# Pass the variables to the HTML template
	#return render_template('index.html', username=username, age=age, location=location)

@app.route('/business/<string:business_id>', methods=['GET'])
def business_reviews(business_id):
	url = f'{yelp_url}/businesses/{business_id}'
	headers = {
		'accept': 'application/json',
		'Authorization': f'Bearer {yelp_api_key}'
	}
	response = requests.get(url, headers=headers)
	business_details = response.json()

	print(business_details)
	
	lat = business_details['coordinates']['latitude']
	long = business_details['coordinates']['longitude']
	print(f'lat and long: ({lat}, {long})')

	
	address = ' '.join(business_details['location']['display_address']) # Joins the list elements into a string
	session['dest_address'] = address # Store data in a global session for access between routes.
	print('Address:', address)  
	############################################################
	## GEOCODING API USE:
	""" Resource: https://developers.google.com/maps/documentation/geocoding/requests-geocoding """
	############################################################
	# Using reverse geocoding Google API to et the place id of the business.
	# The reverse geocoding takes the business lat and long and returns the place_id.
	# The place_id is used in the google maps API to direct the user to their business
	# of choice:
	#geocode_url = f'{google_api_url}/geocode/json?latlng={lat},{long}&key={google_api_key}'
	geocode_url = f'{google_api_url}/geocode/json'
	params = {	
		'address': address,
		'key': google_api_key
	}
	geo_response = requests.get(geocode_url, params=params)
	place_id = geo_response.json()['results'][0]['place_id']
	print(place_id)
	session['dest_place_id'] = place_id
	############################################################
	## GOOGLE MAPS API USE:
	""" Resource: https://developers.google.com/maps/documentation/directions/get-directions """
	############################################################
	google_maps_url = f'{google_api_url}/directions/json'
	params = {
		'destination': f'place_id:{place_id}',
		'origin': f'{lat},{long}',
		'key': google_api_key
	}
	maps_response = requests.get(google_maps_url, params=params)	
	print(maps_response.json())
	############################################################
	DirectionsRequest = {
	  'origin': f'{lat},{long}', # Where we start
	  'destination': ' '.join(address), # Where we are going
	  'travelMode': 'DRIVING',
	  'provideRouteAlternatives': True
	}
	return render_template('maps.html', google_api_key=google_api_key)

""" The following API endpoint is used by the 
static/script.js file to access lat and long
variables to display the map for directions
to the user's desired business. """
@app.route('/fetch-data')
def fetch_data():
	print('session dest: ', session.get('dest_address'))
	data = {
		# Access the session variable needed for the js fetch method:
		'destination': session.get('dest_address')
	}
	return jsonify(data)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)
