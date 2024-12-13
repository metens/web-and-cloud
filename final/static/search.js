// This file handles the YELP API frontend to display the 
// business information searched for by the user. The javascript
// code here interacts with the backend through fetch calls with 
// the python session variables and flask methods:

let latitude, longitude; // User latitude and longitude.
let origin; // User's origin (location).
let directions = false; // Hide map and directions unless user asks.
let locationReady = false;

// Useful business info to display:
let img, url, is_open, rating, phone, destination = false;

// Select the search bar, results div elements, and map:
const searchBar = document.getElementById("search-bar");
const resultsDiv = document.getElementById("results");
const detailsDiv = document.getElementById("details");
const mapContainer = document.getElementById("map");

// Since attaining the geolocation of the user is asynchronous,
// we need to make a promise that they will be defined before
// we use them in the code:
function getLocation() {
	return new Promise((resolve, reject) => {
		if (navigator.geolocation) {
			navigator.geolocation.getCurrentPosition((position) => {
				latitude = position.coords.latitude; longitude = position.coords.longitude;
				// Resolve the promise with the coordinates:
				resolve({ latitude, longitude });
				locationReady = true;
			}, (error) => {
				// Reject if there's an error with geolocation:
				reject('Geolocation error: ' + error.message);
			}
		);} else {
			reject('Geolocation not supported');
		}
	});
}

// Handle latitude/longitude outside the callback:
getLocation().then((coords) => {
	// Safely use latitude and longitude here:
	origin = { lat: coords.latitude, lng: coords.longitude };
	console.log('Origin:', origin);

	if (latitude && longitude) {
		// Event listener for input in the search bar:
		searchBar.addEventListener("input", () => {
			const query = searchBar.value.trim(); // Clean up input to remove unnecessary spaces.
			// When more than 1 character is inserted, begin to autocomplete:
			if (query.length > 1 && locationReady) { 
				resultsDiv.innerHTML = "<div class='loading'>Loading suggestions...</div>";
				fetchSuggestions(query);
			} else if (!locationReady) {
				showError("Location not available. Please allow location access.");
			} else {
				resultsDiv.innerHTML = ""; // Clear results if input is too short or empty
			}
		});
	}
}).catch((error) => {
    console.error(error);  // Handle the error if geolocation fails
});

// Fetch suggestions from the Flask backend:
function fetchSuggestions(query) {
	fetch(`/autocomplete?text=${query}&latitude=${latitude}&longitude=${longitude}`)
	.then(response => response.json())
	.then(renderSuggestions)
	.catch(error => showError("Error fetching autocomplete: " + error.message));
}

function renderSuggestions(data) {
	resultsDiv.innerHTML = ""; // Clear previous results.
	let resultFound = false;

	if (data['businesses']) {
		data['businesses'].forEach(item => {
			const div = document.createElement("div");
			div.className = "suggestion";
			div.textContent = `Business: ${item.name}`;

			// Add click event to fetch/display business details:
			div.addEventListener("click", () => {
				// Fetch details of the clicked business:
				fetch(`/business/${item.id}`).then(response => { return response.json(); }).then(details => {
					// Clear resultsDiv and display the business details:
					destination = details.destination; // Set destination before createing map...
					resultsDiv.innerHTML = `
						<div class="business-details">
							<h2>${details.name}</h2>
							<img src="${details.img || ''}" alt="Business Image" style="max-width: 100%;">
							<p><strong>Rating:</strong> ${details.rating}</p>
							<p><strong>Open Now:</strong> ${details.is_open ? 'Yes' : 'No'}</p>
							<p><strong>Phone:</strong> ${details.phone}</p>
							<a href="${details.url}" target="_blank">Visit Website</a>
						</div>
						<button id="map-button">Directions</button>
						<button id="back-button">Back to Suggestions</button>
					`;

					// Add a map button to display the map and directions from current location:
					document.getElementById("map-button").addEventListener("click", () => {
						document.getElementById("map").style.display = "block"; // Show map.
						initMap(origin, destination, true); // Calls GOOGLE API.
					});

					// Add a back button to return to the suggestions:
					document.getElementById("back-button").addEventListener("click", () => {
						document.getElementById("map").style.display = "none"; // Hide map.
						// Find the travel time element and remove it each time we go back:
						const travelTimeElement = document.getElementById('travel-time');
						if (travelTimeElement) {
							travelTimeElement.remove();
						}
						renderSuggestions(data); // Re-render suggestions.
					});
				}).catch(error => {
					console.error('Error:', error);
				});
			});

			resultsDiv.appendChild(div);
			resultFound = true;
		});
	}

	// No results are found:
	if (!resultFound) {
		resultsDiv.innerHTML = "<p>No suggestions found. Please try a different search.</p>";
	}
}

// Display detailed information for the selected item:
function showDetails(item, type) {
	detailsDiv.style.display = "block"; // Make details visible.
	detailsDiv.innerHTML = `<h3>Details for ${type.slice(0, -1).toUpperCase()}</h3>`;

	if (type === "businesses") {
		fetch(`/businesses?id=${item.id}`)
		.then(response => response.json())
		.then(data => {
			detailsDiv.innerHTML += `<pre>${JSON.stringify(data, null, 2)}</pre>`;
		}) .catch(error => showError("Error fetching business details: " + error.message));
	}
}

// Display error messages:
function showError(message) {
	resultsDiv.innerHTML = `<div class='error'>${message}</div>`;
}
