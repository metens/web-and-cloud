from flask import Flask, redirect, request, url_for, render_template
import requests
import os
  
app = Flask(__name__)
  
@app.route('/')
def home_page():
	return "<html><body><h1>Hello World!</h1>Nothing to see here. Move along.</body></html>"

@app.route('/secret1')
def secret_page():
	return "<html><body><h1>Secret #1</h1>Welcome to the first secret</body></html>"

@app.route('/athlete')
def athlete_page():	
	# My API Application details found here: https://www.strava.com/settings/api
	"""Set the api variables:"""
	client_id=141734
	client_secret='701f50e4f6e9e72e2b5f5de379053b9b03a36596'

	url1 = f"http://www.strava.com/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read"

	#authorization_code='ff41a52ebf87e6b1e048306c6596bfb787e4fdd5'
	#grant_type='authorization_code'

	# Set the API endpoint
	url = "https://www.strava.com/oauth/token"

	# Prepare the payload (form data)
	"""
	data = {
	    'client_id': client_id,
	    'client_secret': client_secret,
	    'code': authorization_code,
	    'grant_type': grant_type
	}"""

	data = {'hello'}
	# Make the POST request
	#response = requests.post(url1, data=data)
	response = requests.post(url1, data=data)
	"""
	# Check if the request was successful
	if response.status_code == 200:
	    # Parse the JSON response
	    response_data = response.json()
	    print("Access Token:", response_data['access_token'])
	else:
	    print("Error:", response.status_code, response.text)
	"""	
	return "<html><body><h1>Athlete page:</h1></body></html>"
	#return response

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, debug=True)
