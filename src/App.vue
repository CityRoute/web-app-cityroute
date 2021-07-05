<template>
  <v-app>
    <NavBar></NavBar>
    <v-main>
      <router-link to="/Home"></router-link>
      <v-slide-x-transition mode="out-in">
        <keep-alive>
          <router-view />
        </keep-alive>
      </v-slide-x-transition>
      <BottomNavBar></BottomNavBar>
    </v-main>
  </v-app>
</template>

<script>
import NavBar from "./components/NavBar";
import BottomNavBar from "./components/BottomNavBar";

export default {
  name: "App",
  components: {
    NavBar,
    BottomNavBar,
  },
  data: () => ({
    model: null,
    text: null,
    items: [
      { title: "Click Me" },
      { title: "Click Me" },
      { title: "Click Me" },
      { title: "Click Me 2" },
    ],
  }),
  computed: {},
};
</script>

<style>
/* Optional: Makes the sample page fill the window. */
body {
  padding-top: 56px;
  padding-bottom: 56px;
  padding: 0;
  margin: 0;
  overflow: hidden;
}
</style>
