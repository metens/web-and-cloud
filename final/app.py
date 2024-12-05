from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__) # Flask object

""" Google Maps Platform Resources:
https://developers.google.com/maps/documentation/directions/get-api-key
https://developers.google.com/maps/documentation/directions/get-directions
"""

# API Key from environment variable $API_KEY to keep api_key secret:
google_api_key = os.getenv("GOOGLE_API_KEY")
#yelp_api_key = os.getenv("YELP_API_KEY")

# All Yelp Fusion API endpoints are under:
#yelp_url = "https://api.yelp.com/v3"

"""To access the google maps api with an output of json:
https://maps.googleapis.com/maps/api/directions/json?origin=Toronto&destination=Montreal&key=YOUR_API_KEY
"""
# Google Directions API:
google_api_url = "https://maps.googleapis.com/maps/api"

@app.route('/')
def home_page():
	headers = { "Authorization": f"Bearer {google_api_key}" }

	# Using latitiude and longitude for destination and origin locations:
	url = f"{google_api_url}/directions/json?destination=45.486599,-122.795609&origin=45.512230,-122.658722&key={google_api_key}"
	
	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		print(response.status_code)
		print(response.text)
		return response.json()
	else: 
		print(response.status_code)
		return response.json()

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)
