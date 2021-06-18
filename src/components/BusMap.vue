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

        <v-tab-item>
          <v-card flat>
            <v-card-text>
              <input
                id="locationInput"
                class="controls"
                type="text"
                placeholder="Search Box"
              />
              <v-text-field
                v-model="origin"
                label="Origin"
                id="locationOrigin"
                outlined
                clearable
                append-icon="mdi-map-marker"
                @click:append="toggleMarker"
              ></v-text-field>
              <v-text-field
                v-model="destination"
                label="Destination"
                id="locationDestination"
                outlined
                clearable
                append-icon="mdi-map-marker"
                @click:append="toggleMarker"
              ></v-text-field>
              <date-picker v-model="time2" type="datetime"></date-picker>
              <v-btn block>
                Get Directions
              </v-btn>
            </v-card-text>
          </v-card>
        </v-tab-item>
        <v-tab-item>
          <v-card flat>
            <v-card-text>
              <p>
                Morbi nec metus. Suspendisse faucibus, nunc et pellentesque
                egestas, lacus ante convallis tellus, vitae iaculis lacus elit
                id tortor. Sed mollis, eros et ultrices tempus, mauris ipsum
                aliquam libero, non adipiscing dolor urna a orci. Curabitur
                ligula sapien, tincidunt non, euismod vitae, posuere imperdiet,
                leo. Nunc sed turpis.
              </p>

              <p>
                Suspendisse feugiat. Suspendisse faucibus, nunc et pellentesque
                egestas, lacus ante convallis tellus, vitae iaculis lacus elit
                id tortor. Proin viverra, ligula sit amet ultrices semper,
                ligula arcu tristique sapien, a accumsan nisi mauris ac eros. In
                hac habitasse platea dictumst. Fusce ac felis sit amet ligula
                pharetra condimentum.
              </p>

              <p>
                Sed consequat, leo eget bibendum sodales, augue velit cursus
                nunc, quis gravida magna mi a libero. Nam commodo suscipit quam.
                In consectetuer turpis ut velit. Sed cursus turpis vitae tortor.
                Aliquam eu nunc.
              </p>

              <p>
                Etiam ut purus mattis mauris sodales aliquam. Ut varius
                tincidunt libero. Aenean viverra rhoncus pede. Duis leo. Fusce
                fermentum odio nec arcu.
              </p>

              <p class="mb-0">
                Donec venenatis vulputate lorem. Aenean viverra rhoncus pede. In
                dui magna, posuere eget, vestibulum et, tempor auctor, justo.
                Fusce commodo aliquam arcu. Suspendisse enim turpis, dictum sed,
                iaculis a, condimentum nec, nisi.
              </p>
            </v-card-text>
          </v-card>
        </v-tab-item>
        <v-tab-item>
          <v-card flat>
            <v-card-text>
              <p>
                Fusce a quam. Phasellus nec sem in justo pellentesque facilisis.
                Nam eget dui. Proin viverra, ligula sit amet ultrices semper,
                ligula arcu tristique sapien, a accumsan nisi mauris ac eros. In
                dui magna, posuere eget, vestibulum et, tempor auctor, justo.
              </p>

              <p class="mb-0">
                Cras sagittis. Phasellus nec sem in justo pellentesque
                facilisis. Proin sapien ipsum, porta a, auctor quis, euismod ut,
                mi. Donec quam felis, ultricies nec, pellentesque eu, pretium
                quis, sem. Nam at tortor in tellus interdum sagittis.
              </p>
            </v-card-text>
          </v-card>
        </v-tab-item>
      </v-tabs>
    </v-card>
  </div>
</template>

<script>
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
function bindInfoWindow(marker, map, infowindow, html) {
  marker.addListener("click", function() {
    infowindow.setContent(html);
    infowindow.open(map, this);
  });
}

export default {
  name: "BusMap",
  computed: {},
  data: () => ({
    map: null,
    mapCenter: (0, 0),
    origin: "",
    destination: "",
    time2: null,
  }),
  methods: {
    initMap() {
      this.map = new google.maps.Map(document.getElementById("map"), {
        center: new google.maps.LatLng(53.3498, -6.2603),
        zoom: 14,
        mapTypeId: "roadmap",
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
        console.log(stops[key].stop_lon);
        markers[key] = new google.maps.Marker({
          position: new google.maps.LatLng(
            parseFloat(stops[key].stop_lat),
            parseFloat(stops[key].stop_lon)
          ),
          map: this.map,
          title: stops[key].stop_name,
          icon: icon,
          id: key,
        });
        // instances[key] = new InfoWindow({
        //   propsData: {
        //     content: "This displays as info-window content!",
        //   },
        // });

        new_infowindows[key] = new google.maps.InfoWindow({
          // content: ,
        });
        bindInfoWindow(
          markers[key],
          this.map,
          new_infowindows[key],
          "<h1>" + stops[key].stop_name + "</h1>"
        );

        google.maps.event.addListener(markers[key], "click", function() {
          new_infowindows[key].open(map, markers[key]);
        });
        EventBus.$emit("map", this.map);
        // instances[key].$mount();
      }

      // new_infowindow.open(this.map, marker);

      // let element = this.$refs["locationOrigin"].$el;
      // element = element.querySelector("input");
      let element = document.getElementById("locationInput");
      console.log(element);
      this.autocomplete = new google.maps.places.SearchBox(element);
    },
    toggleMarker() {},
  },
  mounted() {
    this.initMap();
  },
  components: { DatePicker },
};
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
