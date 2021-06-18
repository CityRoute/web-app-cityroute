<template>
  <v-bottom-navigation grow fixed>
    <v-btn to="/">
      <span>Explore</span>

      <v-icon>mdi-map-marker</v-icon>
    </v-btn>

    <v-btn to="/ratings">
      <span>Review</span>

      <v-icon>mdi-star</v-icon>
    </v-btn>
    <v-btn to="/news">
      <span>News</span>

      <v-icon>mdi-newspaper</v-icon>
    </v-btn>

    <v-btn>
      <span>My Account</span>

      <v-icon>mdi-account</v-icon>
    </v-btn>
  </v-bottom-navigation>
</template>

<script>
export default { name: "BottomNavBar" };
</script>

<style>
</style>
