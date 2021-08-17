<template>
  <v-card class="mx-auto" max-width="434" tile>
    <v-list-item color="rgba(0, 0, 0, .4)">
      <v-list-item-content>
        <v-list-item-title class="title">{{
          this.$store.state.identifier
        }}</v-list-item-title>
        <v-list-item-subtitle>Signed In</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>
    <v-btn @click="logout" elevation="2">Logout</v-btn>
  </v-card>
</template>

<script>
export default {
  name: "MyAccount",
  methods: {
    logout() {
      this.$store.dispatch("userLogout").then(() => {
        this.$root.$emit("showAlert", "Logged out successfully!", "success");
        this.$router.go({ name: "signin" });
      });
    },
  },
};
</script>

<style></style>
