<template>
  <v-autocomplete
    :items="route_numbers"
    outlined
    dense
    chips
    clearable
    small-chips
    class="ma-2"
    label="Filter By Route"
  ></v-autocomplete>
</template>

<script>
export default {
  name: "FilterByStop",
  data: () => ({
    route_numbers: ["foo", "bar", "fizz", "buzz"],
  }),
};
</script>

<style></style>
