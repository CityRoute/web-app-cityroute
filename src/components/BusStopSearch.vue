<template>
  <v-card color="blue lighten-2" dark>
    <v-card-title class="text-h5 blue lighten-3">
      Search for your Stop
    </v-card-title>
    <v-card-text>
      Explore hundreds of bus stops in and around Dublin! For more information
      visit
      <a
        class="grey--text text--lighten-3"
        href="https://www.dublinbus.ie"
        target="_blank"
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
        hide-no-data
        hide-selected
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
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn :disabled="!model" color="yellow darken-3" @click="showSchedule">
        Schedule
        <v-icon right>
          mdi-clock
        </v-icon>
      </v-btn>

      <v-btn
        :disabled="!model"
        color="green darken-3"
        @click="saveToFavourites"
      >
        Save to Favourites
        <v-icon right>
          mdi-star
        </v-icon>
      </v-btn>
      <v-btn :disabled="!model" color="blue darken-3" @click="showOnMap">
        Show on Map
        <v-icon right>
          mdi-map
        </v-icon>
      </v-btn>

      <v-btn :disabled="!model" color="grey darken-3" @click="model = null">
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
    showOnMap() {
      this.$root.$emit("marker", this.model.Description);
    },
    saveToFavourites() {},
    showSchedule() {
      this.isFetching = true;
      let stop_desc = this.model.Description + "";

      stop_desc = stop_desc.split(" ");

      let stop_num = stop_desc[stop_desc.length - 1];
      var self = this;

      axios
        .get("api/bus-stop-times/" + stop_num)
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
        const Description =
          entry.stop_name.length > this.descriptionLimit
            ? entry.stop_name.slice(0, this.descriptionLimit) + "..."
            : entry.stop_name;

        return Object.assign({}, entry, { Description });
      });
    },
  },

  watch: {
    search(val) {
      // Items have already been loaded
      if (this.items.length > 0) return;

      // Items have already been requested
      //   if (this.isLoading) return;

      //   this.isLoading = true;

      // Lazily load input items
      this.entries = stops;
    },
  },
};
</script>

<style>
</style>
