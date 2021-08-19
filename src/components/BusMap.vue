/* eslint-disable no-undef */
<template>
  <div class="map-container">
    <v-card flat v-if="isDirections">
      <v-card-text>
        <v-text-field
          dense
          v-model="origin"
          label="Origin"
          id="locationOrigin"
          outlined
          :placeholder="placeholder"
          ref="locationOrigin"
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
          :placeholder="placeholder"
          ref="locationDestination"
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
              clearable
              :disabled-date="disabledRange"
            >
              ></date-picker
            ></v-col
          >
          <v-col>
            <v-btn
              @click="showRoute()"
              :disabled="!(time && origin && destination)"
            >
              Get Directions
            </v-btn>
          </v-col>
        </v-row>
        <v-row align="center" v-if="directions" justify="space-around">
          <v-btn
            id="fav"
            @click="addFavourite()"
            v-if="this.$store.getters.loggedIn"
          >
            Add Favourite
          </v-btn>
        </v-row>

        <v-card
          style="height: 40vh; overflow-y:scroll; overflow-x:hidden;white-space: nowrap;"
          class="mt-5"
          id="directionsCard"
        >
          <v-banner v-if="directions"
            >Our estimation:
            {{
              new Date(this.total_duration * 1000).toISOString().substr(11, 8)
            }}
          </v-banner>

          <v-card-text>
            <div id="card"></div>
          </v-card-text>
        </v-card>
        <div v-if="directions" class="share-network-list mt-5">
          <ShareNetwork
            v-for="network in networks"
            :network="network.network"
            :key="network.network"
            :style="{ backgroundColor: network.color }"
            :url="sharingLink"
            :title="sharing.title"
            :description="sharing.description"
            :quote="sharing.quote"
            :hashtags="sharing.hashtags"
            :twitterUser="sharing.twitterUser"
          >
            <i :class="network.icon"></i>
            <span>{{ network.name }}</span>
          </ShareNetwork>
          <v-btn aria-label="vuetify-button"id="close" @click="closeDirections()">
            Close Directions
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
    <v-card flat v-if="isRouteViewer">
      <RouteViewer></RouteViewer>
    </v-card>
    <v-card flat v-if="isStopFinder">
      <BusStopSearch></BusStopSearch>
    </v-card>
    <v-card flat v-if="isLandmarks">
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
    <v-card flat v-if="isFavourite"><Favourite></Favourite> </v-card>
  </div>
</template>

<script>
const { google } = require("@/plugins/googleAPI.js");

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
import axios from "axios";
import "vue2-datepicker/index.css";

// const landmarks_data = () => import("../assets/landmarks.json")
// const stops = () => import("../assets/stops.json")


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

let directionsService = new google.maps.DirectionsService();
let routeBounds = false;
const vw = Math.max(
  document.documentElement.clientWidth || 0,
  window.innerWidth || 0
);
// console.log("this", vw);
let overlayWidth = 0.35 * vw;
var leftMargin = 30; // Grace margin to avoid too close fits on the edge of the overlay
var rightMargin = 80;

export default {
  name: "BusMap",
  computed: {
    sharingLink() {
      return window.location.href;
    },
    placeholder() {
      return "";
    },
    isDirections() {
      // console.log(this.$route.fullPath);
      return (
        this.$route.fullPath.includes("directions") || this.$route.path == "/"
      );
    },
    isRouteViewer() {
      return this.$route.fullPath.includes("route-viewer");
    },

    isStopFinder() {
      return this.$route.fullPath.includes("stop-finder");
    },
    isLandmarks() {
      return this.$route.fullPath.includes("landmarks");
    },
    isFavourite() {
      return this.$route.fullPath.includes("favourites");
    },
  },
  data: () => ({
    alert: true,
    total_duration: 0,
    sharing: {
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
    time: new Date(),
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
    "$route.query.lat"() {
      if (this.$route.query.lat != "") {
        this.showRoute();
      }
    },
    placeholder: function() {
      const inputOrigin = document.getElementById("locationOrigin");
      const inputDestination = document.getElementById("locationDestination");
      inputOrigin.placeholder = "";
      inputDestination.placeholder = "";
    },
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
    disabledRange: function(date) {
      return date > new Date(Date.now() + 12096e5) || date < new Date();
    },

    addFavourite() {
      let self = this;

      axios
        .post(
          "/api/add-fav-directions/",
          {},
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.accessToken}`,
            },
            params: {
              origin: this.origin,
              destination: this.destination,
              url: window.location.href,
            },
          }
        )
        .then(function(response) {
          console.log(response);
          self.$root.$emit("showAlert", "Favourite journey added.", "success");
        })
        .catch(function(error) {
          console.log(error);
          self.$root.$emit(
            "showAlert",
            "Favourite journey could not be added.",
            "failure"
          );
        });
    },
    closeDirections() {
      this.directions = false;
      this.sheet = false;
      var card = document.getElementById("card");
      card.innerHTML = "";
      directionsDisplay.setMap(null);
      this.origin = "";
      this.destination = "";
      this.$root.$emit("showAlert", "Directions closed!", "success");
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
          // eslint-disable-next-line no-undef
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
                // const marker = new google.maps.Marker({
                //   position: myLatLng,
                //   map: map,
                // });
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
        },
        onError: (err) => {
          console.log(err);
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

        // timeout to set placeholder to allow for the api to load
        setTimeout(function() {
          inputOrigin.placeholder = "";
          inputDestination.placeholder = "";
        }, 500);

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
      if (this.$route.query.lat & this.$route.query.lng) {
        myLatLng = {
          lat: parseFloat(this.$route.query.lat),
          lng: parseFloat(this.$route.query.lng),
        };
        geocoder.geocode({ location: myLatLng }, (results, status) => {
          if (status === "OK") {
            if (results[0]) {
              console.log("geolocate", results);
              this.destination = results[0].formatted_address;
              this.currentLocation("origin");
              this.sheet = true;
              this.calcRoute(this.origin, this.destination);
            } else {
              window.alert("No results found");
            }
          } else {
            window.alert("Geocoder failed due to: " + status);
          }
        });
        this.currentLocation("origin");
      } else {
        this.sheet = true;
        this.$forceUpdate();

        this.calcRoute(this.origin, this.destination);
      }
    },
    async getDuration(step) {
      await axios
        .get("/api/model-prediction/", {
          params: {
            model_type: "route",
            route_num: step["transit"]["line"].short_name,
            start_stop: step["transit"]["departure_stop"].name,
            end_stop: step["transit"]["arrival_stop"].name,
            num_stops: step["transit"]["num_stops"],
            date_time: this.time,
          },
        })
        .then((response) => {
          console.log(
            "prediction",
            response.data,
            "google",
            step["duration"]["value"]
          );
          this.total_duration +=
            response.data.prediction - step["duration"]["value"];
        })
        .catch((error) => {
          console.log("error", error);
        });
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
          departureTime: this.time,
          trafficModel: "pessimistic",
        },
      };
      directionsService.route(request, (response, status) => {
        if (status === google.maps.DirectionsStatus.OK) {
          this.directions = true;

          // console.log(response);
          let directions = response;
          this.total_duration =
            directions["routes"][0]["legs"][0]["duration"].value;
          for (const step of directions["routes"][0]["legs"][0]["steps"]) {
            if (
              step.travel_mode == "TRANSIT" &&
              step["transit"]["line"]["agencies"][0]["name"] == "Dublin Bus"
            ) {
              this.getDuration(step);
              //  await getDuration(step).then(res => console.log(res));
            }
          }

          directionsDisplay.setDirections(response);
          directionsDisplay.setMap(map);
          var close = document.getElementById("close");

          close.addEventListener("click", function() {
            directionsDisplay.setMap(null);
            directionsDisplay.setPanel(null);
            map.setZoom(15);
            document.getElementById("directionsCard").style.display =
              "none !important";
          });
          document.getElementById("directionsCard").style.display = "block";

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
              // // console.log(routeBounds);
              // Fit updated bounds
              map.fitBounds(routeBounds);
              // console.log(map.getBounds());
              // Write directions steps

              // Offset map
              offsetMap();
            }
          );
          this.$root.$emit("showAlert", "Directions found!", "success");

          return true;
        } else {
          this.$root.$emit(
            "showAlert",
            "Directions not found. Please try again.",
            "failure"
          );
          return false;
        }
      });
    },
  },
  async mounted() {
    
  // const landmarks_data = async  () =>  await  import("../assets/landmarks.json");
  // const stops = async () =>  await import("../assets/stops.json");


  fetch("api/stops.json").then(response => response.json()).then(stops => {
    console.log(stops)
  for (var key of Object.keys(stops)) {
        console.log(key)

    var myLatLng = {
      lat: parseFloat(stops[key].latitude),
      lng: parseFloat(stops[key].longitude),
    };
    // // console.log(stops[key].longitude);
    stopMarkers[stops[key].name] = new google.maps.Marker({
      position: new google.maps.LatLng(
        parseFloat(stops[key].latitude),
        parseFloat(stops[key].longitude)
      ),
      map: map,
      title: stops[key].name,
      icon: icon,
      id: key,
      visible: false,
    });
  }
});
  fetch("api/landmarks.json").then(landmarks_data => {
  landmarkMarkers = [];
  // var new_infowindows = [];
  // var instances = [];
  for (key of Object.keys(landmarks_data.markers)) {
    // // console.log(stops[key].longitude);
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

    let marker = landmarkMarkers[landmarks_data.markers[key].address].marker;

    const landmarkinfowindow = new google.maps.InfoWindow({
      content:
        '<div id="content">' +
        '<div id="siteNotice">' +
        "</div>" +
        `<h1 id="firstHeading">${landmarks_data.markers[key].address}</h1>` +
        '<div id="bodyContent">' +
        '<a href="/#/directions?lat=' +
        landmarks_data.markers[key].lat +
        "&lng=" +
        landmarks_data.markers[key].lng +
        '">Get Directions</a>',
    });

    marker.addListener("click", () => {
      console.log("clicked");
      landmarkinfowindow.open({
        anchor: marker,
        map,
        shouldFocus: false,
      });
    });
  }

});


    (this.origin = this.$route.query.origin),
      (this.destination = this.$route.query.destination),
      initMap();
    this.$root.$on("showStopMarker", (text) => {
      console.log(stopMarkers);
      let marker = stopMarkers[text.substr(text.indexOf(" ") + 1)];
      let marker_position = marker.getPosition();
      console.log(text);
      if (!map.getBounds().contains(marker_position)) {
        map.setCenter(marker_position);
      }

      stopMarkers[text.substr(text.indexOf(" ") + 1)].setVisible(true);

      const infowindow = new google.maps.InfoWindow({
        content:
          text +
          '<a href="/#/directions?lat=' +
          marker_position.lat() +
          "&lng=" +
          marker_position.lng() +
          '">Get Directions</a>',
      });

      marker.addListener("click", () => {
        console.log("clicked");
        infowindow.open({
          anchor: marker,
          map,
          shouldFocus: false,
        });
      });

      map.setZoom(18);
      map.setCenter(marker_position);
    });
    this.$root.$on("showMarkers", (stops) => {
      console.log("text", stops);
      var icon = {
        url: require("@/assets/busstop.png"), // url
        scaledSize: new google.maps.Size(12.5, 25), // scaled size
        origin: new google.maps.Point(0, 0), // origin
        anchor: new google.maps.Point(0, 0), // anchor
      };
      var bounds = new google.maps.LatLngBounds();

      for (var key of Object.keys(stops)) {
        console.log(stops[key]);

        stopMarkers[stops[key].name] = new google.maps.Marker({
          position: new google.maps.LatLng(
            parseFloat(stops[key].latitude),
            parseFloat(stops[key].longitude)
          ),
          map: map,
          title: stops[key].name,
          id: key,
          visible: true,
          icon: icon,
        });
        let marker = stopMarkers[stops[key].name];

        const infowindow = new google.maps.InfoWindow({
          content:
            '<a href="/#/directions?lat=' +
            stops[key].latitude +
            "&lng=" +
            stops[key].longitude +
            '">Get Directions</a>',
        });

        marker.addListener("click", () => {
          console.log("clicked");
          infowindow.open({
            anchor: marker,
            map,
            shouldFocus: false,
          });
        });

        bounds.extend(
          new google.maps.LatLng(
            parseFloat(stops[key].latitude),
            parseFloat(stops[key].longitude)
          )
        );
      }
      map.fitBounds(bounds);
    });

    this.showRoute();
    this.initAutocomplete();
  },
  updated() {},
  components: {
    DatePicker: () => import("vue2-datepicker"),
    BusStopSearch: () => import("./BusStopSearch.vue"),
    Favourite: () => import("./Favourite.vue"),
    RouteViewer: () => import("./RouteViewer.vue"),
  },
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
    polylineOptions: { strokeColor: "#2962ff" },
    panel: document.getElementById("card"),
  });
  directionsDisplay.setMap(map);


  var icon = {
    url: require("@/assets/busstop.png"), // url
    scaledSize: new google.maps.Size(12.5, 25), // scaled size
    origin: new google.maps.Point(0, 0), // origin
    anchor: new google.maps.Point(0, 0), // anchor
  };
  stopMarkers = [];
  // var new_infowindows = [];
  // var instances = [];
}
</script>

<style>
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

#landmarksContainer {
  margin: 5%;
  height: 95vh;
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
