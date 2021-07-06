<template>
  <v-app>
    <v-navigation-drawer
      app
      v-model="drawer"
      :mini-variant.sync="mini"
      permanent
      :expand-on-hover="$vuetify.breakpoint.mdAndUp"
      class="blue accent-4"
      dark
    >
      <v-list-item class="px-2">
        <v-list-item-avatar>
          <v-img src="https://randomuser.me/api/portraits/men/85.jpg"></v-img>
        </v-list-item-avatar>

        <v-list-item-title>Brian Manning</v-list-item-title>

        <v-btn icon @click.stop="mini = !mini">
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </v-list-item>

      <v-divider></v-divider>

      <v-list>
        <v-list-item
          v-for="item in items"
          :key="item.title"
          :to="item.link"
          link
          @click="showSheet()"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-switch
        ripple
        append-icon="mdi-moon"
        v-model="$vuetify.theme.dark"
        v-on:change="darkMap()"
        inset
      ></v-switch>
    </v-navigation-drawer>
    <v-main>
      <v-navigation-drawer
        v-if="$vuetify.breakpoint.mdAndUp"
        absolute
        width="30vw"
        id="MapOptions"
      >
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="text-h4">
              <v-icon large>mdi-bus-stop-covered</v-icon>
              CityRoute
            </v-list-item-title>
            <v-list-item-subtitle>
              Dublin Bus Directions Service
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-spacer></v-spacer>
        <router-view />
      </v-navigation-drawer>

      <div class="text-center" v-else>
        <v-bottom-sheet scrollable v-model="sheet" inset>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              id="thebutton"
              fab
              fixed
              bottom
              dark
              v-bind="attrs"
              v-on="on"
              color="blue darken-2"
            >
              <v-icon>
                mdi-account-circle
              </v-icon>
            </v-btn>
          </template>
          <v-card class="text-center">
            <v-card-title>Select Country</v-card-title>
            <v-card-text style="height: 50vh;">
              <v-btn class="mt-6" text color="error" @click="sheet = !sheet">
                close
              </v-btn>
              <router-view />
            </v-card-text>
          </v-card>
        </v-bottom-sheet>
      </div>
      <div id="map"></div>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "App",
  components: {},
  data: () => ({
    sheet: true,
    model: null,
    text: null,
    drawer: true,
    items: [
      {
        title: "Journey Planner",
        icon: "mdi-map-marker-distance",
        link: "/directions",
      },
      {
        title: "Route Viewer",
        icon: "mdi-map-marker-path",
        link: "/route-viewer",
      },
      { title: "Stop Finder", icon: "mdi-bus-stop", link: "/stop-finder" },
      {
        title: "Landmarks",
        icon: "mdi-map-search-outline",
        link: "/landmarks",
      },
      { title: "Favourites", icon: "mdi-heart", link: "/favourites" },
      { title: "Reviews", icon: "mdi-star", link: "/ratings" },
      { title: "News", icon: "mdi-newspaper", link: "/news" },
      { title: "My Account", icon: "mdi-account", link: "/myaccount" },
    ],
    mini: true,
  }),
  mounted: {},
  methods: {
    showSheet() {
      this.sheet = true;
    },
  },
  computed: {},
};
</script>

<style>
html {
  scrollbar-width: none; /* For Firefox */
  -ms-overflow-style: none; /* For Internet Explorer and Edge */
}

html::-webkit-scrollbar {
  width: 0px; /* For Chrome, Safari, and Opera */
}

/* Optional: Makes the sample page fill the window. */
body {
  padding-top: 56px;
  padding-bottom: 56px;
  padding: 0;
  margin: 0;
  overflow: hidden;
}

#MapOptions {
  position: absolute;
  top: 0;
}

#lateral .v-btn--example {
  bottom: 0;
  position: absolute;
  margin: 0 0 16px 16px;
}
</style>
