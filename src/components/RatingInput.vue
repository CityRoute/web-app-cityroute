<template>
  <v-stepper v-model="e1">
    <v-stepper-header class="" style="">
      <v-stepper-step :complete="e1 > 1" step="1">
        Ratings
      </v-stepper-step>

      <v-divider></v-divider>

      <v-stepper-step :complete="e1 > 2" step="2">
        Review
      </v-stepper-step>

      <v-divider></v-divider>

      <v-stepper-step step="3">
        Confirm
      </v-stepper-step>
    </v-stepper-header>

    <v-stepper-items>
      <v-stepper-content step="1">
        <v-card
          class="mb-12"
          color="white lighten-1 elevation-0"
          height="200px"
        >
          <v-card-actions class="pa-4">
            Cleanliness
            <v-icon medium color="blue darken-2">
              mdi-hand-wash-outline
            </v-icon>
            <v-rating
              v-model="ratings.clean"
              color="yellow darken-3"
              background-color="grey darken-1"
              empty-icon="$ratingFull"
              hover
              @input="updateInput($event, 15)"
            ></v-rating>
          </v-card-actions>
          <v-card-actions class="pa-4">
            Speed
            <v-icon medium color="blue darken-2">
              mdi-hand-wash-outline
            </v-icon>
            <v-rating
              v-model="ratings.speed"
              color="yellow darken-3"
              background-color="grey darken-1"
              empty-icon="$ratingFull"
              hover
              @input="updateInput($event, 15)"
            ></v-rating>
          </v-card-actions>
          <v-card-actions class="pa-4">
            Accuracy
            <v-icon medium color="blue darken-2">
              mdi-hand-wash-outline
            </v-icon>
            <v-rating
              v-model="ratings.accuracy"
              color="yellow darken-3"
              background-color="grey darken-1"
              empty-icon="$ratingFull"
              hover
              @input="updateInput($event, 15)"
            ></v-rating> </v-card-actions
        ></v-card>
        <v-btn color="primary" @click="e1 = 2">
          Continue
        </v-btn>

        <v-btn @click="$emit('close-sheet')" text>
          Cancel
        </v-btn>
      </v-stepper-content>

      <v-stepper-content step="2">
        <v-card class="mt-1 mb-12 elevation-0" color="white" height="200px">
          <div class="text-center">
            <v-textarea
              v-model="review"
              outlined
              name="input-7-4"
              label="Your Experience"
              value=""
              height="180px"
            ></v-textarea>
          </div>
        </v-card>

        <v-btn color="primary" @click="e1 = 3">
          Continue
        </v-btn>

        <v-btn @click="$emit('close-sheet')" text>
          Cancel
        </v-btn>
      </v-stepper-content>

      <v-stepper-content step="3">
        <v-card class="mt-1 mb-12" color="white" height="200px">
          <v-autocomplete
            :items="route_numbers"
            v-model="route"
            item-text="routeid"
            item-value="routeid"
            outlined
            dense
            chips
            clearable
            small-chips
            label="Route"
          ></v-autocomplete>
        </v-card>

        <v-btn
          color="primary"
          @click="
            writeReview();
            $emit('submit-review');
            e1 = 1;
          "
        >
          Submit
        </v-btn>

        <v-btn @click="$emit('close-sheet')" text>
          Cancel
        </v-btn>
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</template>

<script>
import axios from "axios";

export default {
  name: "RatingInput",
  data: () => ({
    search: "",
    review: "",
    ratings: {
      clean: 0,
      accuracy: 0,
      speed: 0,
    },
    e1: 1,
    time: null,
    route_numbers: [],
    route: "",
  }),
  async mounted() {
    const { data } = await axios.get(`/api/routes-all/`);
    this.route_numbers = data;
  },

  methods: {
    writeReview() {
      let self = this;
      axios
        .post("/api/write-review/", null, {
          headers: {
            Authorization: `Bearer ${this.$store.state.accessToken}`,
          },

          params: {
            content: this.review,
            clean_rating: this.ratings.clean,
            speed_rating: this.ratings.speed,
            accuracy_rating: this.ratings.accuracy,
            route: this.route,
          },
        })
        .then(function(response) {
          console.log(response);
          self.$root.$emit("showAlert", "Review has been posted!", "success");
        })
        .catch(function(error) {
          self.$root.$emit(
            "showAlert",
            "Review could not be posted. Please try again.",
            "failure"
          );

          console.log(error);
        });
    },
    updateInput(value, id) {
      // console.log(value, id);
    },
  },
};
</script>

<style></style>
