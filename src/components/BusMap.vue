<template>
  <div class="map-container">
    <div id="map"></div>
    <v-navigation-drawer absolute width="30vw" id="MapOptions">
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
            mdi-map-search-outline
          </v-icon>
          Landmarks
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
                dense
                v-model="origin"
                label="Origin"
                id="locationOrigin"
                outlined
                clearable
                append-icon="mdi-map-marker"
                @click:append="currentLocation('origin')"
              ></v-text-field>
              <v-text-field
                dense
                v-model="destination"
                label="Destination"
                id="locationDestination"
                outlined
                clearable
                append-icon="mdi-map-marker"
                @click:append="currentLocation('destination')"
              ></v-text-field>
              <v-row>
                <v-col>
                  <date-picker
                    v-model="time"
                    :open.sync="open"
                    placeholder="Select date & time"
                    type="datetime"
                    close-on-complete
                    format="DD, MMM - hh:mm"
                  ></date-picker
                ></v-col>
                <v-col>
                  <v-btn @click="showRoute()">
                    Get Directions
                  </v-btn>
                </v-col>
              </v-row>
              <v-card
                v-if="directions"
                style="height: 40vh; overflow-y:scroll; overflow-x:hidden;white-space: nowrap;"
                class="mt-5"
              >
                <v-card-text>
                  <v-btn id="close" @click="closeDirections()">
                    Close Directions
                  </v-btn>
                  <div id="card"></div>
                </v-card-text>
              </v-card>
              <div v-if="directions" class="share-network-list mt-5">
                <ShareNetwork
                  v-for="network in networks"
                  :network="network.network"
                  :key="network.network"
                  :style="{ backgroundColor: network.color }"
                  :url="sharing.url"
                  :title="sharing.title"
                  :description="sharing.description"
                  :quote="sharing.quote"
                  :hashtags="sharing.hashtags"
                  :twitterUser="sharing.twitterUser"
                >
                  <i :class="network.icon"></i>
                  <span>{{ network.name }}</span>
                </ShareNetwork>
              </div>
            </v-card-text>
          </v-card>
        </v-tab-item>
        <v-tab-item>
          <v-card flat></v-card>
        </v-tab-item>
        <v-tab-item>
          <v-card flat>
            <BusStopSearch></BusStopSearch>
          </v-card>
        </v-tab-item>
        <v-tab-item>
          <v-card flat>
            <div id="landmarksContainer">
              <v-switch
                v-for="(item, index) in categories"
                v-bind:key="item.name"
                inset
                color="amber"
                :prepend-icon="item.icon"
                :label="item.name"
                :input-value="item.shown"
                @change="flipLandmarkSwitch(index, item)"
              ></v-switch>
            </div>
          </v-card>
        </v-tab-item>
      </v-tabs>
    </v-navigation-drawer>
  </div>
</template>

<script>
import {
  mdiHospitalBuilding,
  mdiShopping,
  mdiFactory,
  mdiTicket,
  mdiSchool,
  mdiMapMarkerQuestionOutline,
  mdiDramaMasks,
  mdiTheater,
  mdiAccountChild,
  mdiMapMarkerRadius,
  mdiMusicNoteOutline,
  mdiBasketball,
} from "@mdi/js";
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
import Landmarks from "./Landmarks.vue";
import landmarks_data from "../assets/landmarks.json";

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
const vw = Math.max(
  document.documentElement.clientWidth || 0,
  window.innerWidth || 0
);
console.log("this", vw);
let overlayWidth = 0.35 * vw;
var leftMargin = 30; // Grace margin to avoid too close fits on the edge of the overlay
var rightMargin = 80;
export default {
  name: "BusMap",
  computed: {},
  data: () => ({
    sharing: {
      url: window.location.href,
      title: "CityRoute directions",
      description: "Thanks for your using our route planner!",
      hashtags: "cityroute,dublinbus",
    },
    networks: [
      {
        network: "sms",
        name: "SMS",
        icon: "far fah fa-lg fa-comment-dots",
        color: "#333333",
      },
      {
        network: "twitter",
        name: "Twitter",
        icon: "fab fah fa-lg fa-twitter",
        color: "#1da1f2",
      },
      {
        network: "whatsapp",
        name: "Whatsapp",
        icon: "fab fah fa-lg fa-whatsapp",
        color: "#25d366",
      },
    ],
    directions: false,
    autocompleteInit: false,
    mapCenter: (0, 0),
    origin: "",
    destination: "",
    time: null,
    open: false,
    sheet: false,
    date: "new Date()",
    categories: {
      Hospital: {
        shown: false,
        name: "Hospital",
        isVenue: false,
        icon: mdiHospitalBuilding,
      },
      Shopping: {
        shown: false,
        name: "Shopping",
        isVenue: false,
        icon: mdiShopping,
      },
      Industrial: {
        shown: false,
        name: "Industrial",
        isVenue: false,
        icon: mdiFactory,
      },
      Attraction: {
        shown: false,
        name: "Attraction",
        isVenue: false,
        icon: mdiTicket,
      },
      College: {
        shown: false,
        name: "College",
        isVenue: false,
        icon: mdiSchool,
      },
      Other: {
        shown: false,
        name: "Other",
        isVenue: false,
        icon: mdiMapMarkerQuestionOutline,
      },
      Arts: {
        shown: false,
        name: "Arts, Theatre & Comedy",
        isVenue: true,
        icon: mdiDramaMasks,
      },
      Exhibition: {
        shown: false,
        name: "Exhibition",
        isVenue: true,
        icon: mdiTheater,
      },
      Family: {
        shown: false,
        name: "Family & Attractions",
        isVenue: true,
        icon: mdiAccountChild,
      },
      Miscellaneous: {
        shown: false,
        name: "Miscellaneous",
        isVenue: true,
        icon: mdiMapMarkerRadius,
      },
      Music: {
        shown: false,
        name: "Music",
        isVenue: true,
        icon: mdiMusicNoteOutline,
      },
      Sport: {
        shown: false,
        name: "Sport",
        isVenue: true,
        icon: mdiBasketball,
      },
    },
  }),
  watch: {
    origin: function() {
      this.$router.push({
        query: { origin: this.origin, destination: this.destination },
      });
    },
    destination: function() {
      this.$router.push({
        query: { origin: this.origin, destination: this.destination },
      });
    },
  },
  methods: {
    closeDirections() {
      this.directions = false;
      this.sheet = !this.sheet;
      $("#card").html("");
    },
    flipLandmarkSwitch(val, item) {
      item.shown = !item.shown;
      for (var entry of Object.keys(landmarkMarkers)) {
        if (landmarkMarkers[entry].category == val) {
          landmarkMarkers[entry].marker.setVisible(this.categories[val].shown);
          landmarkMarkers[entry].marker.setIcon({
            path: this.categories[val].icon,
          });
        }
      }
    },
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
    setOrigin(val) {
      this.origin = val;
    },
    initAutocomplete() {
      if (!this.autocompleteInit) {
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
        this.autocompleteInit = true;
        var self = this;

        autocompleteOrigin.addListener("place_changed", function() {
          self.$data.origin = inputOrigin.value;
        });
        autocompleteDestination.addListener("place_changed", function() {
          self.destination = inputDestination.value;
        });
      }
    },

    showRoute() {
      this.sheet = true;
      this.directions = true;
      this.calcRoute(this.origin, this.destination);
    },
    calcRoute(start, end) {
      if (Array.isArray(start)) {
        start = new google.maps.LatLng(start[0], start[1]);
      }
      if (Array.isArray(end)) {
        end = new google.maps.LatLng(end[0], end[1]);
      }

      let travel_mode = "TRANSIT";
      var request = {
        origin: start,
        destination: end,
        travelMode: travel_mode,
        drivingOptions: {
          departureTime: new Date(this.time),
          trafficModel: "pessimistic",
        },
      };

      directionsService.route(request, function(response, status) {
        if (status === google.maps.DirectionsStatus.OK) {
          console.log(response);
          directionsDisplay.setDirections(response);
          directionsDisplay.setMap(map);
          $("#close").on("click", function() {
            directionsDisplay.setMap(null);
            directionsDisplay.setPanel(null);
            map.setZoom(15);
          });

          directionsDisplay.setPanel(document.getElementById("card"));

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
              console.log(map.getBounds());
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
    (this.origin = this.$route.query.origin),
      (this.destination = this.$route.query.destination),
      initMap();
    this.$root.$on("marker", (text) => {
      console.log(stopMarkers[text]);
      if (!map.getBounds().contains(stopMarkers[text].getPosition())) {
        map.setCenter(stopMarkers[text].getPosition());
      }
    });
    this.showRoute();
  },
  updated() {
    this.initAutocomplete();
  },
  components: { DatePicker, BusStopSearch, Landmarks },
};
let directionsDisplay;
let map;
let myLatLng = { lat: 53.3531, lng: -6.258 };
let geocoder = null;
var stopMarkers;
var landmarkMarkers;
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
  stopMarkers = [];
  // var new_infowindows = [];
  // var instances = [];
  for (var key of Object.keys(stops)) {
    var myLatLng = {
      lat: parseFloat(stops[key].stop_lat),
      lng: parseFloat(stops[key].stop_lon),
    };
    // console.log(stops[key].stop_lon);
    stopMarkers[stops[key].stop_name] = new google.maps.Marker({
      position: new google.maps.LatLng(
        parseFloat(stops[key].stop_lat),
        parseFloat(stops[key].stop_lon)
      ),
      map: map,
      title: stops[key].stop_name,
      icon: icon,
      id: key,
      visible: false,
    });
  }

  landmarkMarkers = [];
  // var new_infowindows = [];
  // var instances = [];
  for (var key of Object.keys(landmarks_data.markers)) {
    // console.log(stops[key].stop_lon);
    const contentString =
      '<div id="content">' +
      '<div id="siteNotice">' +
      "</div>" +
      `<h1 id="firstHeading">${landmarks_data.markers[key].address}</h1>` +
      '<div id="bodyContent">';
    const infowindow = new google.maps.InfoWindow({
      content: contentString,
    });

    landmarkMarkers[landmarks_data.markers[key].address] = {
      marker: new google.maps.Marker({
        position: new google.maps.LatLng(
          parseFloat(landmarks_data.markers[key].lat),
          parseFloat(landmarks_data.markers[key].lng)
        ),
        map: map,
        title: landmarks_data.markers[key].address,
        id: key,
        visible: false,
      }),
      category: landmarks_data.markers[key].category,
    };
    landmarkMarkers[landmarks_data.markers[key].address].marker.addListener(
      "click",
      () => {
        infowindow.open({
          anchor: landmarkMarkers[landmarks_data.markers[key].address].marker,
          map,
          shouldFocus: false,
        });
      }
    );
  }
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

#landmarksContainer {
  height: 50vh;
  overflow-y: auto;
}

.share-network-list {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  max-width: 1000px;
  margin: auto;
}
a[class^="share-network-"] {
  flex: none;
  color: #ffffff !important;
  background-color: #333;
  border-radius: 3px;
  overflow: hidden;
  display: flex;
  flex-direction: row;
  align-content: center;
  align-items: center;
  cursor: pointer;
  margin: 0 10px 10px 0;
}
a[class^="share-network-"] .fah {
  background-color: rgba(0, 0, 0, 0.2) !important;
  padding: 10px;
  flex: 0 1 auto;
}
a[class^="share-network-"] span {
  padding: 0 10px;
  flex: 1 1 0%;
  font-weight: 500;
}

a[class^="share-network-"],
a[class^="share-network-"]:hover,
a[class^="share-network-"]:focus,
a[class^="share-network-"]:active {
  text-decoration: none;
  color: inherit;
}
.warnbox-content,
.adp-warnbox {
  visibility: hidden;
  height: 0;
  width: 0;
}
</style>
