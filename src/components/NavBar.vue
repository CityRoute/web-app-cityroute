<template>
  <v-app-bar app dark>
    <v-btn plain to="/">
      <v-icon>mdi-bus-stop-covered</v-icon>
      <v-app-bar-title
        ><u><strong>City</strong>Route</u></v-app-bar-title
      ></v-btn
    >

    <v-spacer></v-spacer>
    <v-dialog v-model="dialog">
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon color="white" v-bind="attrs" v-on="on">
          <v-icon>mdi-magnify</v-icon>
        </v-btn>
      </template>
      <SearchBox></SearchBox>
    </v-dialog>
    <v-bottom-sheet v-model="sheet" inset>
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon color="white" v-bind="attrs" v-on="on">
          <v-icon>mdi-heart</v-icon>
        </v-btn>
      </template>
      <v-sheet class="text-center" height="200px">
        <v-btn class="mt-6" text color="error" @click="sheet = !sheet">
          close
        </v-btn>
        <div class="my-3">
          <Favourite></Favourite>
        </div>
      </v-sheet>
    </v-bottom-sheet>

    <v-menu bottom left>
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon color="white" v-bind="attrs" v-on="on">
          <v-icon>mdi-hamburger</v-icon>
        </v-btn>
        <template>
          <v-switch
            ripple
            append-icon="mdi-moon"
            v-model="$vuetify.theme.dark"
            v-on:change="darkMap()"
            inset
          ></v-switch>
        </template>
      </template>

      <template v-slot:extension>
        <slot></slot>
      </template>
    </v-menu>
  </v-app-bar>
</template>

<script>
import { EventBus } from "./EventBus";

import Favourite from "./Favourite.vue";
import SearchBox from "./SearchBox.vue";

export default {
  name: "NavBar",
  components: {
    SearchBox,
  },
  data: () => ({
    sheet: false,
    map: null,
    dialog: null,
  }),
  methods: {
    darkMap() {
      EventBus.$emit("changeMapStyle");
    },
  },
};
</script>

<style></style>
