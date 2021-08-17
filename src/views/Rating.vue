<template>
  <v-container>
    <v-card-title class="text-h5">
      Reviews
    </v-card-title>

    <Rating
      v-for="review in reviews"
      :content="review.content"
      :route="review.routeid"
      :key="review"
      :accuracy_rating="review.accuracy_rating"
      :clean_rating="review.clean_rating"
      :speed_rating="review.speed_rating"
    />
    <v-fab-transition>
      <v-btn
        v-if="this.$store.getters.loggedIn"
        @click="sheet = !sheet"
        large
        dark
        bottom
        left
        class="v-btn--example"
      >
        <v-icon>mdi-bus</v-icon> Rate
      </v-btn>
      <v-btn
        v-else
        @click="$router.push({ name: 'MyAccount' })"
        large
        dark
        bottom
        left
        class="v-btn--example"
      >
        <v-icon>mdi-bus</v-icon> Login to review
      </v-btn>
    </v-fab-transition>
    <v-dialog
      v-model="sheet"
      transition="dialog-bottom-transition"
      max-width="600"
    >
      <RatingInput v-on:submit-review="updateSheet()" />
    </v-dialog>
  </v-container>
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
    console.log(data);
    this.reviews = data.reverse();
  },
  data: () => ({
    reviews: [],
    sheet: false,
  }),
  methods: {
    updateInput(value, id) {
      console.log(value, id);
    },
    async updateSheet() {
      this.sheet = !this.sheet;
      const { data } = await axios.get(`/api/reviews-all/`);
      this.reviews = data.reverse();
    },
  },
};
</script>
<style>
.v-btn--example {
  bottom: 0;
  margin: 0 0 64px 16px;
  position: fixed;
  z-index: 999;
}
</style>
