<template>
  <v-card class="mx-auto" max-width="500">
    <v-toolbar color="blue" dark>
      <v-toolbar-title>Favourites</v-toolbar-title>

      <v-spacer></v-spacer>
    </v-toolbar>

    <v-list>
      <v-list-group
        v-for="item in items"
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
            <v-list-item-title v-text="child.stopid"></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-group>
    </v-list>
  </v-card>
</template>

<script>
import axios from "axios";
export default {
  data: () => ({
    favouriteStops: [],
  }),
  computed: {
    items: function() {
      return [
        {
          action: "mdi-bus-stop",
          active: true,
          items: this.favouriteStops,
          title: "Bus Stops",
        },
      ];
    },
  },
  beforeMount() {
    this.getFavouriteStops();
  },

  methods: {
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
  },
};
</script>

<style></style>
