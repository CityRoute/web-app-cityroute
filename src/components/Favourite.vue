<template>
  <v-card class="mx-auto" max-width="500">
    <v-toolbar color="blue" dark>
      <v-toolbar-title>Favourites</v-toolbar-title>

      <v-spacer></v-spacer>
    </v-toolbar>

    <v-list v-if="this.favouriteStops.length > 0">
      <v-list-group
        v-for="item in busStops"
        :key="item.title"
        v-model="item.active"
        :prepend-icon="item.action"
        no-action
      >
        <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title v-text="item.title"></v-list-item-title>
          </v-list-item-content>
        </template>

        <v-list-item v-for="child in item.items" :key="child.title">
          <v-list-item-content>
            <v-list-item-title v-text="child.number"></v-list-item-title>
          </v-list-item-content>
          <v-list-item-action>
            <v-btn-toggle dense>
              <v-btn icon>
                <v-icon
                  @click="getDirections(child.latitude, child.longitude)"
                  color="grey lighten-1"
                  >mdi-directions</v-icon
                >
              </v-btn>
              <v-btn icon>
                <v-icon
                  @click="deleteFavourite('stop', child.number)"
                  color="grey lighten-1"
                  >mdi-delete</v-icon
                >
              </v-btn>
            </v-btn-toggle>
          </v-list-item-action>
        </v-list-item>
      </v-list-group>
    </v-list>
    <v-list v-if="this.favouriteRoutes.length > 0">
      <v-list-group
        v-for="item in busRoutes"
        :key="item.title"
        v-model="item.active"
        :prepend-icon="item.action"
        no-action
      >
        <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title v-text="item.title"></v-list-item-title>
          </v-list-item-content>
        </template>

        <v-list-item v-for="child in item.items" :key="child.title">
          <v-list-item-content>
            <v-list-item-title v-text="child.number"></v-list-item-title>
          </v-list-item-content>
          <v-list-item-action>
            <v-btn-toggle dense>
              <v-btn icon @click="getRoute(child.number)">
                <v-icon color="grey lighten-1">mdi-information</v-icon>
              </v-btn>
              <v-btn icon>
                <v-icon
                  @click="deleteFavourite('route', child.number)"
                  color="grey lighten-1"
                  >mdi-delete</v-icon
                >
              </v-btn>
            </v-btn-toggle>
          </v-list-item-action>
        </v-list-item>
      </v-list-group>
    </v-list>
    <v-list v-if="this.favouriteDirections.length > 0">
      <v-list-group
        v-for="item in busDirections"
        :key="item.title"
        v-model="item.active"
        :prepend-icon="item.action"
        no-action
      >
        <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title v-text="item.title"></v-list-item-title>
          </v-list-item-content>
        </template>

        <v-list-item v-for="child in item.items" :key="child.title">
          <v-list-item-content>
            <v-list-item-title v-text="child.origin"></v-list-item-title>
            <v-list-item-subtitle
              v-text="child.destination"
            ></v-list-item-subtitle>
          </v-list-item-content>
          <v-list-item-action>
            <v-btn-toggle dense>
              <v-btn @click="goToURL(child.url)" icon>
                <v-icon color="grey lighten-1">mdi-directions</v-icon>
              </v-btn>
              <v-btn icon>
                <v-icon
                  @click="deleteFavourite('directions', child.directions_id)"
                  color="grey lighten-1"
                  >mdi-delete</v-icon
                >
              </v-btn>
            </v-btn-toggle>
          </v-list-item-action>
        </v-list-item>
      </v-list-group>
    </v-list>
  </v-card>
</template>

<script>
import axios from "axios";
const baseUrl = window.location.protocol + "//" + window.location.host;

export default {
  data: () => ({
    selectedItem: 1,
    favouriteStops: [],
    favouriteRoutes: [],
    favouriteDirections: [],
  }),
  computed: {
    busDirections: function() {
      console.log("favouriteDirections", this.favouriteDirections);
      return [
        {
          action: "mdi-bus-stop",
          active: true,
          items: this.favouriteDirections,
          title: "Directions",
        },
      ];
    },

    busStops: function() {
      console.log("favouriteStops", this.favouriteStops);
      return [
        {
          action: "mdi-bus-stop",
          active: true,
          items: this.favouriteStops,
          title: "Bus Stops",
        },
      ];
    },
    busRoutes: function() {
      return [
        {
          action: "mdi-bus-stop",
          active: true,
          items: this.favouriteRoutes,
          title: "Bus Routes",
        },
      ];
    },
  },
  beforeMount() {
    this.getFavouriteStops();
    this.getFavouriteRoutes();
    this.getFavouriteDirections();
  },
  created() {
    EventBus.$on("add-marker", (data) => {
      let marker = this.makeMarker(data.latitude, data.longitude);
      this.$markers.push(marker);
    });
  },

  methods: {
    deleteFavourite(type, number) {
      let self = this;
      if (type == "stop") {
        axios
          .post(
            "/api/delete-fav-stop/" + number,
            {},
            {
              headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
              },
            }
          )
          .then(function(response) {
            console.log(response);
            self.getFavouriteStops();
          })
          .catch(function(error) {
            console.log(error);
          });
      } else if (type == "route") {
        axios
          .post(
            "/api/delete-fav-route/" + number,
            {},
            {
              headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
              },
            }
          )
          .then(function(response) {
            console.log(response);
            self.getFavouriteRoutes();
          })
          .catch(function(error) {
            console.log(error);
          });
      } else if (type == "directions") {
        axios
          .post(
            "/api/delete-fav-directions/" + number,
            {},
            {
              headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
              },
            }
          )
          .then(function(response) {
            console.log(response);
            self.getFavouriteDirections();
          })
          .catch(function(error) {
            console.log(error);
          });
      }
    },
    goToURL(URL) {
      window.location.assign(URL);
    },
    getDirections(latitude, longitude) {
      window.location.assign(
        "/#/directions?lat=" + latitude + "&lng=" + longitude
      );
    },
    makeMarker(latitude, longitude) {
      console.log("hello latitude is ", latitude);
      return new google.maps.Marker({
        position: new google.maps.LatLng(latitude, longitude),
        icon: null,
        map: this.$map,
        title: null,
      });
    },
    getFavouriteStops() {
      axios
        .get(
          "/api/favourite-stops/",

          {
            headers: {
              Authorization: `Bearer ${this.$store.state.accessToken}`,
            },
          }
        )
        .then((response) => {
          console.log(response.data);
          this.favouriteStops = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getFavouriteDirections() {
      axios
        .get(
          "/api/favourite-directions/",

          {
            headers: {
              Authorization: `Bearer ${this.$store.state.accessToken}`,
            },
          }
        )
        .then((response) => {
          console.log(response.data);
          this.favouriteDirections = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    getFavouriteRoutes() {
      axios
        .get(
          "/api/favourite-routes/",

          {
            headers: {
              Authorization: `Bearer ${this.$store.state.accessToken}`,
            },
          }
        )
        .then((response) => {
          console.log(response.data);
          this.favouriteRoutes = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style></style>
