// Perform an API call from Yelp Deliveries
function createMap(restaurants) {

    // Create the tile layer that will be the background of our map
    var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}", {
      attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"http://mapbox.com\">Mapbox</a>",
      maxZoom: 18,
      id: "mapbox.light",
      accessToken: API_KEY
    });
  
    // Create a baseMaps object to hold the lightmap layer
    var baseMaps = {
      "Light Map": lightmap
    };
  
    // Create an overlayMaps object to hold the bikeStations layer
    var overlayMaps = {
      "Restaurants": restaurants
    };
  
    // Create the map object with options
    var map = L.map("map-id", {
      center: [37.599724, -122.386950],
      zoom: 12,
      layers: [lightmap, restaurants]
    });
  
    // Create a layer control, pass in the baseMaps and overlayMaps. Add the layer control to the map
    L.control.layers(baseMaps, overlayMaps, {
      collapsed: false
    }).addTo(map);
  }
  function drawDots(){ 
    
    var yelpapi= d3.json("https://cors-anywhere.herokuapp.com/https://api.yelp.com/v3/businesses/search?term=delivery&location=Daly%20City&limit=50&radius=20000") 
          .header("Authorization", "Bearer 4MSriJZOVqZN2Qzr5VJv7ZNFM7XiPtcSA-EmXpB-Pp4eoJi-xfOoFNFHb2A6g0-TWApA6Xeieg9bL8erXqdvBlfnLCGJhnh8p8QEa_UWgKGrnSr4dJgOgNQDcPt7XnYx") 
          .get(function(error, yelpData) { 
            if (error) throw error;
            console.log(yelpData)
            var restoMarkers = [];
            for(var i=0; i < yelpData.businesses.length; i++){
              var resto = (yelpData.businesses[i]) 
              var restoMarker = L.marker([resto.coordinates.latitude, resto.coordinates.longitude])
               .bindPopup("<h3>" + resto.name + "<h3><h3>Ratings: " + resto.rating + "</h3>" + "<h3>Alias:" + resto.alias + "</h3>" + "<h3>Transactions:" + resto.transactions + "</h3>" + "<h3>Address:"+ resto.location.display_address + "</h3>" + "<h3>Phone Number:"+ resto.phone + "</h3>");
          
              // Add the marker to the bikeMarkers array
              restoMarkers.push(restoMarker);
            }
            // console.log(restoMarkers)
            createMap(L.layerGroup(restoMarkers));
          })
  
  }
  drawDots()

  