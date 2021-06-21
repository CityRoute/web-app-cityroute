<template>
  <v-card
    color="blue lighten-2"
    dark
  >
    <v-card-title class="text-h5 blue lighten-3">
      Search for your Stop
    </v-card-title>
    <v-card-text>
      Explore hundreds of bus stops in and around Dublin! For more information visit
      <a
        class="grey--text text--lighten-3"
        href="https://www.dublinpublictransport.ie/dublin-buses"
        target="_blank"
      >the Official Wesbite</a>.
    </v-card-text>
    <v-card-text>
      <v-autocomplete
        v-model="model"
        :items="items"
        :loading="isLoading"
        :search-input.sync="search"
        color="white"
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
      <v-list
        v-if="model"
        class="blue lighten-3"
      >
        <v-list-item
          v-for="(field, i) in fields"
          :key="i"
        >
          <v-list-item-content>
            <v-list-item-title v-text="field.value"></v-list-item-title>
            <v-list-item-subtitle v-text="field.key"></v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-expand-transition>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
        :disabled="!model"
        color="grey darken-3"
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

export default {
  name: "BusStopSearch",
  data: () => ({
    descriptionLimit: 60,
    entries: [],
    isLoading: false,
    model: null,
    search: null,
  }),

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
