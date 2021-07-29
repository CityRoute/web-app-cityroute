<template>
  <div class="about">
    <FilterByStop />
    <SortBy />
    <Rating v-for="index in 10" :key="index" />
    <v-fab-transition>
      <v-btn
        @click="sheet = !sheet"
        large
        dark
        bottom
        left
        class="v-btn--example"
      >
        <v-icon>mdi-bus</v-icon> Rate
      </v-btn>
    </v-fab-transition>
    <v-dialog
      v-model="sheet"
      transition="dialog-bottom-transition"
      max-width="600"
    >
      <RatingInput v-on:submit-review="updateSheet()" />
    </v-dialog>
  </div>
</template>

<script>
import Rating from "../components/Rating.vue";
import RatingInput from "../components/RatingInput";
import FilterByStop from "../components/FilterByStop";
import SortBy from "../components/SortBy";

export default {
  name: "About",
  components: {
    Rating,
    RatingInput,
    FilterByStop,
    SortBy,
  },
  data: () => ({
    sheet: false,
  }),
  methods: {
    updateInput(value, id) {
      // console.log(value, id);
    },
    updateSheet() {
      this.sheet = !this.sheet;
    },
  },
};
</script>
<style>
/* This is for documentation purposes and will not be needed in your application */
.v-btn--example {
  bottom: 0;
  margin: 0 0 64px 16px;
  position: fixed;
  z-index: 999;
}
</style>
