// This file grabs the user's current location, the final business destination
// and then calls the Google Maps API to create a map and show the directions
// from the origin (user location) to the destination (business) and how long
// it will take to get there via car.

// Resource: https://developers.google.com/maps/documentation/javascript/directions?hl=en#TravelModes //
// Create the Google Maps API map to display the current user location
// and the final business destination with directions:
function initMap(origin, destination, directions) { // Export function to use in script.js.
	if (directions == true) { // Only display map and directions if user asks.
		// Create the map
		const map = new google.maps.Map(document.getElementById("map"), {
			center: origin,
			zoom: 10 
		});

		// Initialize Directions Service and Renderer objects:
		const directionsService = new google.maps.DirectionsService();
		const directionsRenderer = new google.maps.DirectionsRenderer();

		// Attach DirectionsRenderer to the map:
		directionsRenderer.setMap(map);

		// Create route request:
		const request = {
			origin: origin,
			destination: destination,
			travelMode: google.maps.TravelMode.DRIVING,
		};

		// Make the directions request:
		directionsService.route(request, (result, status) => {
			if (status === google.maps.DirectionsStatus.OK) {
				// Render route from request:
				directionsRenderer.setDirections(result);
				TimeToDest(result); // Call to display time in browser.
			} else {
				console.error(`Error: Request failed because: ${status}`);
			}
		});
	}
}
window.initMap = initMap; // Google Maps API requires global initMap access.

// Function takes in the result from the directionsService object
// and creates a div element in the HTML to display the time 
// until arrival at the final destination:
function TimeToDest(result) {
	// Get travel time from origin to destination:
	const route = result.routes[0];
	const leg = route.legs[0]; 
	const travelTime = leg.duration.text;

	console.log('Time to Destination:', travelTime);

	// Show travel time in the window:
	const travelTimeElement = document.createElement('div');
	travelTimeElement.innerHTML = `<h2>Time to Destination: ${travelTime}</h2>`;
	document.body.appendChild(travelTimeElement);
}
