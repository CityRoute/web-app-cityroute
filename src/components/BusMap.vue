<template>
  <div class="map-container">

    <div id="map"></div>

    <v-card id="MapOptions">
      <v-tabs>
        <v-tab>
          <v-icon left>
            mdi-map-marker-distance
          </v-icon>
          Plan Your Trip
        </v-tab>
        <v-tab>
          <v-icon left>
            mdi-map-marker-path
          </v-icon>
          Bus Route Viewer
        </v-tab>
        <v-tab>
          <v-icon left>
            mdi-bus-stop
          </v-icon>
          Stop Finder
        </v-tab>
        <v-tab>
          <v-icon left>
            mdi-eye-off
          </v-icon>
        </v-tab>

        <v-tab-item>
          <v-card flat>
            <v-card-text>

              <v-text-field
                v-model="origin"
                label="Origin"
                id="locationOrigin"
                outlined
                clearable
                append-icon="mdi-map-marker"
                @click:append="currentLocation('origin')"
              ></v-text-field>
              <v-text-field
                v-model="destination"
                label="Destination"
                id="locationDestination"
                outlined
                clearable
                append-icon="mdi-map-marker"
                @click:append="currentLocation('destination')"
              ></v-text-field>
              <date-picker v-model="time"         :open.sync="open"
    placeholder="Select date & time"
 type="datetime" close-on-complete format="DD, MMM - hh:mm"
></date-picker>
<!-- <div>
<v-date-picker v-model="date" mode="dateTime" is24hr>
  <template v-slot="{ inputValue, inputEvents }">
    <input
      class="px-2 py-1 border rounded focus:outline-none focus:border-blue-300"
      :value="inputValue"
      v-on="inputEvents"
    />
  </template>
</v-date-picker>
</div> -->

              <v-btn   @click="showRoute();">
                Get Directions
              </v-btn>
                  <v-bottom-sheet
      v-model="sheet"
      inset
         hide-overlay
    no-click-animation
    scrollable
    
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="orange"
          dark
          v-bind="attrs"
          v-on="on"
        >
          Show Directions
        </v-btn>

      </template>
                    <v-card>
        <v-card-text style="height: 300px;">

        <v-btn
          class="mt-6"
          text
          color="error"
          @click="sheet = !sheet"
        >
          close
        </v-btn>
          <div id="card"></div>
                  </v-card-text >

      </v-card>
    </v-bottom-sheet>

            </v-card-text>
          </v-card>
        </v-tab-item>
        <v-tab-item>
          <v-card flat>
            <!-- <div   class="card">
            </div> -->
          </v-card>
        </v-tab-item>
        <v-tab-item>
          <v-card flat>
<BusStopSearch></BusStopSearch>          
</v-card>
        </v-tab-item>
      </v-tabs>

    </v-card>

  </div>
</template>

<script>
import $ from "jquery";
import VCalendar from "v-calendar";
import axios from "axios";
import BusStopSearch from "./BusStopSearch.vue";
import DatePicker from "vue2-datepicker";
import "vue2-datepicker/index.css";
import InfoWindowComponent from "./InfoWindow.vue";
import { EventBus } from "./EventBus";
import Vue from "vue";
var InfoWindow = Vue.extend(InfoWindowComponent);
// var instance = new InfoWindow({
//   propsData: {
//     content: "This displays as info-window content!",
//   },
// });
import stops from "../assets/stops.json";
function offsetMap() {
  if (routeBounds !== false) {
    // Clear listener defined in directions results
    google.maps.event.clearListeners(map, "idle");

    // Top right corner
    var topRightCorner = new google.maps.LatLng(
      map
        .getBounds()
        .getNorthEast()
        .lat(),
      map
        .getBounds()
        .getNorthEast()
        .lng()
    );

    // Top right point
    var topRightPoint = fromLatLngToPoint(topRightCorner).x;

    // Get pixel position of leftmost and rightmost points
    var leftCoords = routeBounds.getSouthWest();
    var leftMost = fromLatLngToPoint(leftCoords).x;
    var rightMost = fromLatLngToPoint(routeBounds.getNorthEast()).x;

    // Calculate left and right offsets
    var leftOffset = overlayWidth - leftMost;
    var rightOffset = topRightPoint - rightMargin - rightMost;

    // Only if left offset is needed
    if (leftOffset >= 0) {
      if (leftOffset < rightOffset) {
        var mapOffset = Math.round((rightOffset - leftOffset) / 2);

        // Pan the map by the offset calculated on the x axis
        map.panBy(-mapOffset, 0);

        // Get the new left point after pan
        var newLeftPoint = fromLatLngToPoint(leftCoords).x;

        if (newLeftPoint <= overlayWidth) {
          // Leftmost point is still under the overlay
          // Offset map again
          offsetMap();
        }
      } else {
        // Cannot offset map at this zoom level otherwise both leftmost and rightmost points will not fit
        // Zoom out and offset map again
        map.setZoom(map.getZoom() - 1);
        offsetMap();
      }
    }
  }
}

function fromLatLngToPoint(latLng) {
  var scale = Math.pow(2, map.getZoom());
  var nw = new google.maps.LatLng(
    map
      .getBounds()
      .getNorthEast()
      .lat(),
    map
      .getBounds()
      .getSouthWest()
      .lng()
  );
  var worldCoordinateNW = map.getProjection().fromLatLngToPoint(nw);
  var worldCoordinate = map.getProjection().fromLatLngToPoint(latLng);

  return new google.maps.Point(
    Math.floor((worldCoordinate.x - worldCoordinateNW.x) * scale),
    Math.floor((worldCoordinate.y - worldCoordinateNW.y) * scale)
  );
}

const trackLocation = ({ onSuccess, onError = () => {} }) => {
  // Omitted for brevity

  return navigator.geolocation.getCurrentPosition(onSuccess, onError, {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0,
  });
};
const getPositionErrorMessage = (code) => {
  switch (code) {
    case 1:
      return "Permission denied.";
    case 2:
      return "Position unavailable.";
    case 3:
      return "Timeout reached.";
    default:
      return null;
  }
};
// https://stackoverflow.com/questions/24952593/how-to-add-my-location-button-in-google-maps
function addYourLocationButton(map) {
  var controlDiv = document.createElement("div");

  var firstChild = document.createElement("button");
  firstChild.style.backgroundColor = "#fff";
  firstChild.style.border = "none";
  firstChild.style.outline = "none";
  firstChild.style.width = "28px";
  firstChild.style.height = "28px";
  firstChild.style.borderRadius = "2px";
  firstChild.style.boxShadow = "0 1px 4px rgba(0,0,0,0.3)";
  firstChild.style.cursor = "pointer";
  firstChild.style.marginRight = "10px";
  firstChild.style.padding = "0";
  firstChild.title = "Your Location";
  controlDiv.appendChild(firstChild);

  var secondChild = document.createElement("div");
  secondChild.style.margin = "5px";
  secondChild.style.width = "18px";
  secondChild.style.height = "18px";
  secondChild.style.backgroundImage =
    "url(https://maps.gstatic.com/tactile/mylocation/mylocation-sprite-2x.png)";
  secondChild.style.backgroundSize = "180px 18px";
  secondChild.style.backgroundPosition = "0 0";
  secondChild.style.backgroundRepeat = "no-repeat";
  firstChild.appendChild(secondChild);

  google.maps.event.addListener(map, "center_changed", function() {
    secondChild.style["background-position"] = "0 0";
  });

  firstChild.addEventListener("click", function() {
    var imgX = 0,
      animationInterval = setInterval(function() {
        imgX = -imgX - 18;
        secondChild.style["background-position"] = imgX + "px 0";
      }, 500);

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        var latlng = new google.maps.LatLng(
          position.coords.latitude,
          position.coords.longitude
        );
        myLatLng = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };

        map.setCenter(latlng);
        clearInterval(animationInterval);
        secondChild.style["background-position"] = "-144px 0";
      });
    } else {
      clearInterval(animationInterval);
      secondChild.style["background-position"] = "0 0";
    }
  });

  controlDiv.index = 1;
  map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(controlDiv);
}

function bindInfoWindow(marker, map, infowindow, html) {
  marker.addListener("click", function() {
    infowindow.setContent(html);
    infowindow.open(map, this);
  });
}

let directionsService = new google.maps.DirectionsService();
let routeBounds = false;
let overlayWidth = 200;
var leftMargin = 30; // Grace margin to avoid too close fits on the edge of the overlay
var rightMargin = 80;
export default {
  name: "BusMap",
  computed: {},
  data: () => ({
    mapCenter: (0, 0),
    origin: "",
    destination: "",
    time: null,
    open: false,
    sheet: false,
    date: "new Date()",
  }),
  methods: {
    hideDateTimePicker(value, type) {
      if (type === "minute") {
        this.open = false;
      }
    },

    currentLocation(textBox) {
      trackLocation({
        onSuccess: ({ coords: { latitude: lat, longitude: lng } }) => {
          let current_marker = new google.maps.Marker({
            position: { lat: lat, lng: lng },
            icon: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
            map,
          });
          current_marker.setPosition({ lat, lng });
          map.panTo({ lat, lng });
          myLatLng = { lat: lat, lng: lng };
          geocoder.geocode({ location: myLatLng }, (results, status) => {
            if (status === "OK") {
              if (results[0]) {
                map.setZoom(11);
                const marker = new google.maps.Marker({
                  position: myLatLng,
                  map: map,
                });
              } else {
                window.alert("No results found");
              }
            } else {
              window.alert("Geocoder failed due to: " + status);
            }
            if (textBox === "origin") {
              this.origin = results[0].formatted_address;
            } else {
              this.destination = results[0].formatted_address;
            }
          });

          // Print out the user's location.
          // $info.textContent = `Current Location Found!`;
          // // Don't forget to remove any error class name.
          // $info.classList.remove("error");
          // $info.classList.add("success");
        },
        onError: (err) => {
          // Print out the error message.
          // $info.textContent = `Error: ${getPositionErrorMessage(err.code) ||
          //   err.message}`;
          // // Add error class name.
          // $info.classList.add("error");
          // $info.classList.remove("success");
        },
      });
    },
    sampleFun() {
      const inputOrigin = document.getElementById("locationOrigin");
      const inputDestination = document.getElementById("locationDestination");

      const options = {
        componentRestrictions: { country: "ie" },
        fields: ["formatted_address", "geometry", "name"],
        origin: map.getCenter(),
        strictBounds: false,
        types: ["establishment"],
      };
      const autocompleteOrigin = new google.maps.places.Autocomplete(
        inputOrigin,
        options
      );
      const autocompleteDestination = new google.maps.places.Autocomplete(
        inputDestination,
        options
      );
      map.addListener("bounds_changed", () => {
        autocompleteOrigin.setBounds(map.getBounds());
      });
      map.addListener("bounds_changed", () => {
        autocompleteDestination.setBounds(map.getBounds());
      });

      inputOrigin.placeholder = "";
      inputDestination.placeholder = "";
    },

    showRoute() {
      console.log(this.time);
      this.sampleFun();
      this.sheet = true;
      let locationOrigin = $("#locationOrigin").val();
      let locationDestination = $("#locationDestination").val();
      console.log(locationOrigin);
      console.log(locationDestination);

      this.calcRoute(locationOrigin, locationDestination);
    },
    calcRoute(start, end) {
      if (Array.isArray(start)) {
        start = new google.maps.LatLng(start[0], start[1]);
      }
      if (Array.isArray(end)) {
        end = new google.maps.LatLng(end[0], end[1]);
      }

      // console.log(start);
      let after_directions_latlng = end;
      let travel_mode = "DRIVING";
      var request = {
        origin: start,
        destination: end,
        travelMode: travel_mode,
        drivingOptions: {
          departureTime: new Date(this.time),
          trafficModel: "pessimistic",
        },
      };
      console.log(Date(this.time));

      directionsService.route(request, function(response, status) {
        if (status === google.maps.DirectionsStatus.OK) {
          directionsDisplay.setDirections(response);
          directionsDisplay.setMap(map);
          console.log($("#card").length);

          $("#card").append(
            "" +
              "            <div class='card' id=\"overlay\">\n" +
              "                <span id='close'\n" +
              "                      onClick='this.parentNode.parentNode.removeChild(this.parentNode);  return false;'>x</span>\n" +
              '                <div id="overlayContent"></div>\n' +
              "            </div>\n"
          );
          $("#close").on("click", function() {
            directionsDisplay.setMap(null);
            directionsDisplay.setPanel(null);
            map.setZoom(15);
            map.setCenter(after_directions_latlng);
          });

          directionsDisplay.setPanel(document.getElementById("overlayContent"));

          // Define route bounds for use in offsetMap function
          routeBounds = response.routes[0].bounds;

          // Write directions steps

          // Wait for map to be idle before calling offsetMap function
          google.maps.event.addListener(map, "idle", function() {
            // Offset map
            offsetMap();
          });

          // Listen for directions changes to update bounds and reapply offset
          google.maps.event.addListener(
            directionsDisplay,
            "directions_changed",
            function() {
              // Get the updated route directions response
              var updatedResponse = directionsDisplay.getDirections();

              // Update route bounds
              routeBounds = updatedResponse.routes[0].bounds;
              // console.log(routeBounds);
              // Fit updated bounds
              map.fitBounds(routeBounds);

              // Write directions steps

              // Offset map
              offsetMap();
            }
          );
        }
      });
    },
  },
  mounted() {
    initMap();
  },
  components: { DatePicker, BusStopSearch },
};
let directionsDisplay;
let map;
let myLatLng = { lat: 53.3531, lng: -6.258 };
let geocoder = null;
function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: new google.maps.LatLng(53.3498, -6.2603),
    zoom: 14,
    mapTypeId: "roadmap",
  });
  addYourLocationButton(map);
  geocoder = new google.maps.Geocoder();

  directionsDisplay = new google.maps.DirectionsRenderer({
    draggable: true,
    map,
    panel: document.getElementById("card"),
  });
  directionsDisplay.setMap(map);
  trackLocation({
    onSuccess: ({ coords: { latitude: lat, longitude: lng } }) => {
      let current_marker = new google.maps.Marker({
        position: { lat: lat, lng: lng },
        icon: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        map,
      });
      current_marker.setPosition({ lat, lng });
      map.panTo({ lat, lng });
      myLatLng = { lat: lat, lng: lng };

      // Print out the user's location.
      // $info.textContent = `Current Location Found!`;
      // // Don't forget to remove any error class name.
      // $info.classList.remove("error");
      // $info.classList.add("success");
    },
    onError: (err) => {
      // Print out the error message.
      // $info.textContent = `Error: ${getPositionErrorMessage(err.code) ||
      //   err.message}`;
      // // Add error class name.
      // $info.classList.add("error");
      // $info.classList.remove("success");
    },
  });

  var icon = {
    url: require("@/assets/busstop.png"), // url
    scaledSize: new google.maps.Size(12.5, 25), // scaled size
    origin: new google.maps.Point(0, 0), // origin
    anchor: new google.maps.Point(0, 0), // anchor
  };
  var markers = [];
  var new_infowindows = [];
  var instances = [];
  for (var key of Object.keys(stops)) {
    var myLatLng = {
      lat: parseFloat(stops[key].stop_lat),
      lng: parseFloat(stops[key].stop_lon),
    };
    // console.log(stops[key].stop_lon);
    markers[key] = new google.maps.Marker({
      position: new google.maps.LatLng(
        parseFloat(stops[key].stop_lat),
        parseFloat(stops[key].stop_lon)
      ),
      map: map,
      title: stops[key].stop_name,
      icon: icon,
      id: key,
    });
    // instances[key] = new InfoWindow({
    //   propsData: {
    //     content: "This displays as info-window content!",
    //   },
    // });

    // new_infowindows[key] = new google.maps.InfoWindow({
    // content: ,
    // });
    // bindInfoWindow(
    //   markers[key],
    //   map,
    //   new_infowindows[key],
    //   "<h1>" + stops[key].stop_name + "</h1>"
    // );

    // google.maps.event.addListener(markers[key], "click", function() {
    //   new_infowindows[key].open(map, markers[key]);
    // });
    // EventBus.$emit("map", map);
    // instances[key].$mount();
  }

  // new_infowindow.open(this.map, marker);

  // let element = this.$refs["locationOrigin"].$el;
  // element = element.querySelector("input");
  // let element = document.getElementById("locationInput");
  // console.log(element);
  // this.autocomplete = new google.maps.places.SearchBox(element);
}
</script>

<style>
/* Always set the map height explicitly to define the size of the div
* element that contains the map. */
#MapOptions {
  position: absolute;
  top: 0;
}
#map {
  height: 100%;
}

.map-container {
  height: calc(100vh - 110px);
  margin: 0px;
  padding: 0px;
}
.gm-style .gm-style-iw-d::-webkit-scrollbar-track,
.gm-style .gm-style-iw-d::-webkit-scrollbar-track-piece,
.gm-style .gm-style-iw-c,
.gm-style .gm-style-iw-t::after {
  background: rgba(255, 255, 255, 0);
}
</style>
