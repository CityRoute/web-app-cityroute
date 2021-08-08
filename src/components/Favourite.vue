<template>
  <v-card class="mx-auto" max-width="500">
    <v-toolbar color="blue" dark>
      <v-toolbar-title>Favourites</v-toolbar-title>

      <v-spacer></v-spacer>
    </v-toolbar>

    <v-list>
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
        </v-list-item>
      </v-list-group>
    </v-list>
    <v-list>
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
    favouriteRoutes: [],
  }),
  computed: {
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
