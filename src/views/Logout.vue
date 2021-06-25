<template>
  <div class="log"></div>
</template>

<script>
export default {
  created() {
    this.$store.dispatch("userLogout").then(() => {
      // this.$router.push("/login");
      this.$router.push({ path: "/login" });
    });
  },
};
</script>

<style></style>
