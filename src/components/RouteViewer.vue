<template>
  <v-card color="blue lighten-2" dark>
    <v-card-title class="text-h5 blue lighten-3">
      Search for your Route
    </v-card-title>
    <v-card-text>
      Explore hundreds of bus routes in and around Dublin! For more information
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
        :items="route_numbers"
        :loading="isLoading"
        :search-input.sync="search"
        color="white"
        @change="getStops()"
        hide-no-data
        hide-selected
        item-text="routeid"
        item-value="routeid"
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
      <!-- <v-btn :disabled="!model" color="yellow darken-3" @click="getStops">
        Schedule
        <v-icon right>
          mdi-clock
        </v-icon>
      </v-btn> -->

      <v-btn
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
    </v-card-actions>

    <v-card-actions class="justify-center">
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
    stops: [],
    route_numbers: [],
    info: null,
    bus_stop_times_div: 0,
    headers: [
      {
        text: "Name",
        value: "name",
      },
      { text: "Number", value: "number" },
    ],
    descriptionLimit: 60,
    entries: [],
    isLoading: false,
    model: null,
    search: null,
    isFetching: true,
  }),
  async mounted() {
    const { data } = await axios.get(`/api/routes-all/`);
    this.route_numbers = data;
  },
  methods: {
    showOnMap() {
      this.$root.$emit("showMarkers", this.info);
    },
    saveToFavourites() {
      console.log(this.model.routeid);
      axios
        .post(
          "/api/add-fav-route/",
          {},
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.accessToken}`,
            },
            params: {
              routeid: this.model.routeid,
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
    async getStops() {
      this.isFetching = true;
      const { data } = await axios.get("api/route-stops/", {
        params: { routeid: this.model.routeid, outbound_yn: "True" },
      });
      this.info = data;
      console.log(data);
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

<style></style>
