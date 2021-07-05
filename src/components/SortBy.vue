<template>
  <v-autocomplete
    :items="route_numbers"
    outlined
    dense
    chips
    clearable
    small-chips
    class="ma-2"
    label="Sort By"
  ></v-autocomplete>
</template>

<script>
export default {
  name: "SortBy",
  data: () => ({
    route_numbers: ["foo", "bar", "fizz", "buzz"],
  }),
};
</script>

<style></style>
