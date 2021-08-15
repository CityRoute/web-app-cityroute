<template>
  <div class="about">
    <Rating
      v-for="review in reviews"
      :content="review.content"
      :route="review.routeid"
      :key="review"
    />
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
import axios from "axios";
export default {
  name: "About",
  components: {
    Rating,
    RatingInput,
  },
  async mounted() {
    const { data } = await axios.get(`/api/reviews-all/`);
    this.reviews = data;
  },
  data: () => ({
    reviews: [],
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
