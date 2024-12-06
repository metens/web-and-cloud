from flask import Flask, request
import requests
import os

app = Flask(__name__) # Flask object

""" Google Maps Platform Resources:
https://developers.google.com/maps/documentation/directions/get-api-key
https://developers.google.com/maps/documentation/directions/get-directions
"""

""" Yelp Resources:
https://docs.developer.yelp.com/docs/fusion-intro
https://docs.developer.yelp.com/reference/v3_business_search
"""

# API Key from environment variables $GOOGLE_API_KEY and $YELP_API_KEY to keep keys secret:
google_api_key = os.getenv("GOOGLE_API_KEY")
yelp_api_key = os.getenv("YELP_API_KEY")

"""To access the google maps api with an output of json:
https://maps.googleapis.com/maps/api/directions/json?origin=Toronto&destination=Montreal&key=YOUR_API_KEY
"""
# Google Directions API:
google_api_url = "https://maps.googleapis.com/maps/api"

# All Yelp Fusion API endpoints are under:
yelp_url = "https://api.yelp.com/v3"

@app.route('/')
def home_page():
	#headers = { "Authorization": f"Bearer {google_api_key}" }
	headers = { "Authorization": f"Bearer {yelp_api_key}" }

	latitude = 45.486599
	longitude = -122.7982922 
	text = "salt"
	# Using latitiude and longitude for destination and origin locations:
	#url = f"{google_api_url}/directions/json?destination=45.486599,-122.795609&origin=45.512230,-122.658722&key={google_api_key}"
	url = f"{yelp_url}/autocomplete?text={text}&latitude={latitude}&longitude={longitude}"
	
	response = requests.get(url, headers=headers)
	print("RESPONSE STATUS:", response.status_code)
	if response.status_code == 200:
		print("RESPONSE:", response.text)
	return response.json()

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)
