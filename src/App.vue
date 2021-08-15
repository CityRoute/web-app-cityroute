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
          <v-icon large>
            mdi-bus-articulated-front
          </v-icon>
        </v-list-item-avatar>

        <v-list-item-title>CityRoute</v-list-item-title>

        <v-btn icon @click.stop="mini = !mini">
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </v-list-item>

      <v-divider></v-divider>

      <v-list>
        <v-list-item
          v-for="item in filtered_items"
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
      
      <template v-slot:append>
        <div class="pa-2">
          <v-btn block class="text-right" @click="darkMap()">
            <v-icon left>
              mdi-brightness-4
            </v-icon>
            <span v-if="!$vuetify.theme.dark">
              Dark Mode
            </span>
            <span v-else>
              Light Mode
            </span>
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>
    <v-main v-if="$vuetify.breakpoint.mdAndDown">
      <div height="30vh">
        <div id="map" style="height:30vh;"></div>
        <div style="height:70vh; overflow-y: auto;">
          <router-view />
        </div>
      </div>
    </v-main>

    <v-main v-else>
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
    mini: true,
    items: [
      {
        title: "Journey Planner",
        icon: "mdi-map-marker-distance",
        link: "/directions",
        login: false,
      },
      {
        title: "Route Viewer",
        icon: "mdi-map-marker-path",
        link: "/route-viewer",
        login: false,
      },
      {
        title: "Stop Finder",
        icon: "mdi-bus-stop",
        link: "/stop-finder",
        login: false,
      },
      {
        title: "Landmarks",
        icon: "mdi-map-search-outline",
        link: "/landmarks",
        login: false,
      },
      {
        title: "Favourites",
        icon: "mdi-heart",
        link: "/favourites",
        login: true,
      },
      { title: "Reviews", icon: "mdi-star", link: "/ratings", login: false },
      { title: "News", icon: "mdi-newspaper", link: "/news", login: false },
      {
        title: "My Account",
        icon: "mdi-account",
        link: "/myaccount",
        login: false,
      },
    ],
  }),
  
  mounted: {},
  methods: {
    darkMap() {
      this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
    },
    showSheet() {
      this.sheet = true;
    },
  },
  computed: {
    filtered_items: function() {
      if (this.$store.getters.loggedIn) {
        return this.items;
      } else {
        return this.items.filter((item) => !item.login);
      }
    },
  },
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
