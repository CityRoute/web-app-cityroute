<template>
  <div class="log"></div>
</template>

<script>
export default {
  created() {
    this.$store.dispatch("userLogout").then(() => {
      this.$router.go({ name: "signin" });
    });
  },
};
</script>

<style></style>
