<template>
  <v-card class="mx-auto" max-width="434" tile>
    <v-list-item color="rgba(0, 0, 0, .4)">
      <v-list-item-content>
        <v-list-item-title class="title">{{this.$store.state.identifier}}</v-list-item-title>
        <v-list-item-subtitle>Signed In</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>
    <v-btn to="/logout" elevation="2">Logout</v-btn>
  </v-card>
</template>

<script>
export default {
  name: "MyAccount",
};
</script>

<style></style>
