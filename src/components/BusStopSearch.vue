<template>
  <v-card color="yellow lighten-2">
    <v-card-title class="text-h5 yellow">
      Search for your Stop
    </v-card-title>
    <v-card-text>
      Explore hundreds of bus stops in and around Dublin! For more information
      visit
      <a class="" href="https://www.dublinbus.ie" target="_blank"
        >the Official Wesbite</a
      >.
    </v-card-text>
    <v-card-text>
      <v-autocomplete
        v-model="model"
        :items="items"
        :loading="isLoading"
        :search-input.sync="search"
        color="white"
        @change="showSchedule()"
        item-text="Description"
        item-value="API"
        label="Bus Stops"
        placeholder="Start typing to Search"
        prepend-icon="mdi-bus-stop"
        return-object
      ></v-autocomplete>
    </v-card-text>
    <v-divider></v-divider>
    <v-expand-transition>
      <div v-if="!isFetching && info">
        <v-theme-provider root>
          <v-data-table
            mobile-breakpoint="0"
            :key="bus_stop_times_div"
            v-if="model"
            :headers="headers"
            :items="info"
            :items-per-page="5"
          >
          </v-data-table>
        </v-theme-provider>
      </div>
    </v-expand-transition>
    <v-card-actions class="justify-center">
      <v-btn aria-label="vuetify-button"
        :disabled="!model"
        color="green darken-3"
        @click="saveToFavourites"
        v-if="this.$store.getters.loggedIn"
      >
        Save to Favourites
        <v-icon right>
          mdi-star
        </v-icon>
      </v-btn>
      <v-btn aria-label="vuetify-button"
        :disabled="!model"
        color="green darken-3"
        style="color:white"
        v-on:click="getDirections()"
      >
        Get Directions
        <v-icon right>
          mdi-map
        </v-icon>
      </v-btn>
    </v-card-actions>

    <v-card-actions class="justify-center">
      <v-btn aria-label="vuetify-button"
        :disabled="!model"
        color="blue darken-3"
        style="color:white"
        @click="showOnMap"
      >
        Show on Map
        <v-icon right>
          mdi-map
        </v-icon>
      </v-btn>

      <v-btn aria-label="vuetify-button"
        :disabled="!model"
        color="grey darken-3"
        style="color:white"
        @click="model = null"
      >
        Clear
        <v-icon right>
          mdi-close-circle
        </v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import stops from "../assets/stops.json";
import axios from "axios";

export default {
  name: "BusStopSearch",
  data: () => ({
    info: null,
    bus_stop_times_div: 0,
    headers: [
      {
        text: "Route",
        align: "start",
        sortable: false,
        value: "Route",
      },
      { text: "Destination", value: "Destination" },
      { text: "Expected Time", value: "Expected_Time" },
    ],
    descriptionLimit: 60,
    entries: [],
    isLoading: false,
    model: null,
    search: null,
    isFetching: true,
  }),
  methods: {
    getDirections() {
      window.location.assign(
        '<a href="/#/directions?lat=' +
          this.model.latitude +
          "&lng=" +
          this.model.longitude
      );
    },
    showOnMap() {
      this.$root.$emit("showStopMarker", this.model.Description);
    },
    saveToFavourites() {
      axios
        .post(
          "/api/add-fav-stop/" + this.model.number,
          {},
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.accessToken}`,
            },
          }
        )
        .then(function(response) {
          console.log(response);
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    showSchedule() {
      console.log(this.model);
      this.isFetching = true;
      let stop_desc = this.model.Description + "";
      // console.log(this.model.number);
      stop_desc = stop_desc.split(" ");
      let stop_num = stop_desc[stop_desc.length - 1];
      var self = this;
      axios
        .get("api/bus-stop-times/" + this.model.number)
        .then(function(response) {
          self.info = response.data;
          bus_stop_times_div += 1;
          this.$parent.refresh();
        })
        .catch((e) => {});
      this.isFetching = false;
    },
  },
  computed: {
    fields() {
      if (!this.model) return [];

      return Object.keys(this.model).map((key) => {
        return {
          key,
          value: this.model[key] || "n/a",
        };
      });
    },
    items() {
      return this.entries.map((entry) => {
        let Description =
          entry.name.length > this.descriptionLimit
            ? entry.name.slice(0, this.descriptionLimit) + "..."
            : entry.name;
        Description = entry.number + " " + Description;
        return Object.assign({}, entry, { Description });
      });
    },
  },

  watch: {
    search() {
      if (this.items.length > 0) return;
      this.entries = stops;
      console.log(stops);
    },
  },
};
</script>

<style></style>
