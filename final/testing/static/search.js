// This file handles the YELP API frontend to display the 
// business information searched for by the user. The javascript
// code here interacts with the backend through fetch calls with 
// the python session variables and flask methods:

let latitude, longitude; // User latitude and longitude.
let origin; // User's origin (location).
let locationReady = false;
let directions = false; // Hide map and directions unless user asks.

// Useful business info to display:
let img, url, is_open, rating, phone, destination = false;

// Select the search bar and results div elements
const searchBar = document.getElementById("search-bar");
const resultsDiv = document.getElementById("results");
const detailsDiv = document.getElementById("details");

//if (origin) { locationReady = true; initMap(origin, destination, directions); }
function getLocation() {
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    latitude = position.coords.latitude;
                    longitude = position.coords.longitude;
                    // Resolve the promise with the coordinates
                    resolve({ latitude, longitude });
			locationReady = true;
                },
                (error) => {
                    // Reject if there's an error with geolocation
                    reject('Geolocation error: ' + error.message);
                }
            );
        } else {
            reject('Geolocation not supported');
        }
    });
}

// Use the getLocation function and handle latitude/longitude outside the callback
getLocation().then((coords) => {
	console.log('Latitude:', coords.latitude, 'Longitude:', coords.longitude);
	// You can use latitude and longitude here safely
	origin = { lat: coords.latitude, lng: coords.longitude };
	console.log('Origin:', origin);

	if (latitude && longitude) {
		console.log(latitude, longitude);
		// Flag to check if a business was clicked before showing details.
		let clickedBusiness = false;

		// Event listener for input in the search bar
		searchBar.addEventListener("input", () => {
		    const query = searchBar.value.trim(); // Clean up input to remove unnecessary spaces
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

// Function to fetch suggestions from the Flask backend
function fetchSuggestions(query) {
    fetch(`/autocomplete?text=${query}&latitude=${latitude}&longitude=${longitude}`)
        .then(response => response.json())
        .then(renderSuggestions)
        .catch(error => showError("Error fetching autocomplete: " + error.message));
}

function renderSuggestions(data) {
    resultsDiv.innerHTML = ""; // Clear previous results
    let resultFound = false;

    if (data['businesses']) {
        console.log(`business: ${JSON.stringify(data['businesses'], null, 2)}`);

        data['businesses'].forEach(item => {
            const div = document.createElement("div");
            div.className = "suggestion";
            div.textContent = `Business: ${item.name}`;

            // Add click event to fetch and display business details
            div.addEventListener("click", () => {
                console.log('clicked');
                console.log(`business_id: ${item.id}`);

                // Fetch details of the clicked business
                //fetch(`/business/${item.id}`)
		fetch(`/business/${item.id}`)
		    .then(response => {
			if (!response.ok) {
			    throw new Error('Network response was not ok');
			}
			return response.json();
		    })
		    .then(details => {
			console.log('Fetched data:', data);
        		// Clear resultsDiv and display the business details
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

			console.log('directions:', directions);
                        // Add a map button to display the map and directions from current location:
                        document.getElementById("map-button").addEventListener("click", () => {
				console.log('cloicked');
				directions = true;
				if (destination) { locationReady = true; initMap(origin, destination, directions); }
				console.log('directions:', directions);
                        });

                        // Add a back button to return to the suggestions
                        document.getElementById("back-button").addEventListener("click", () => {
				directions = false;	
                        	renderSuggestions(data); // Re-render suggestions
                        });

		    })
		    .catch(error => {
			console.error('Error fetching data:', error);
		    });
           });

            resultsDiv.appendChild(div);
            resultFound = true;
        });
    }

    // If no results are found, display a message
    if (!resultFound) {
        resultsDiv.innerHTML = "<p>No suggestions found. Please try a different search.</p>";
        console.log('No suggestions found.');
    }
}

// Function to display detailed information for the selected item
function showDetails(item, type) {
    detailsDiv.style.display = "block"; // Make details visible
    detailsDiv.innerHTML = `<h3>Details for ${type.slice(0, -1).toUpperCase()}</h3>`;
    
    // Fetch additional business details if it's a business item
    if (type === "businesses") {
        fetch(`/businesses?id=${item.id}`)
            .then(response => response.json())
            .then(data => {
                detailsDiv.innerHTML += `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            })
            .catch(error => showError("Error fetching business details: " + error.message));
    } else {
        // For other types, just show the item details directly
        detailsDiv.innerHTML += `<pre>${JSON.stringify(item, null, 2)}</pre>`;
    }
}

// Function to display error messages
function showError(message) {
	resultsDiv.innerHTML = `<div class='error'>${message}</div>`;
}
