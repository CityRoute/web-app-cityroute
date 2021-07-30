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
        <v-list-item-group
          v-model="selectedItem"
          color="primary"
        >
          <v-list-item v-for="child in item.items" :key="child.title">
            <v-list-item-content @add-marker="makeMarker(child)">
              <v-list-item-title v-text="child.name"></v-list-item-title>
              <p>Stop: {{ child.number }}</p>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list-group>
    </v-list>
  </v-card>
</template>

<script>
import axios from "axios";
export default {
  data: () => ({
    selectedItem: 1,
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
  created(){
    EventBus.$on('add-marker', (data)=>{
       let marker = this.makeMarker(data.latitude, data.longitude);
       this.$markers.push(marker);
     });
  },

  methods: {
    makeMarker(latitude, longitude) {
      console.log('hello latitude is ', latitude)
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
  },
};
</script>

<style></style>
