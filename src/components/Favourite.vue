<template>
  <v-card class="mx-auto" max-width="500">
    <v-toolbar color="blue" dark>
      <v-toolbar-title>Favourites</v-toolbar-title>

      <v-spacer></v-spacer>
    </v-toolbar>

    <v-list>
      <v-list-group
        v-for="item in favouriteStops"
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
            <v-list-item-title v-text="child.title"></v-list-item-title>
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
    items: [
      {
        action: "mdi-bus-stop",
        active: true,
        items: [
          { title: "Breakfast & brunch" },
          { title: "New American" },
          { title: "Sushi" },
        ],
        title: "Bus Stops",
      },
    ],
  }),
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
        .then(function(response) {
          console.log(response);
          this.favouriteStops = response.data;
        })
        .catch(function(error) {
          console.log(error);
        });
    },
  },
};
</script>

<style></style>
