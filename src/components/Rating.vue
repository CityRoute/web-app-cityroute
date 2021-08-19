<template>
  <v-card class="ma-4 mx-auto" color="#ffdd55" max-width="80vw">
    <v-card-title>
      <v-icon large left>
        mdi-bus
      </v-icon>
      <span class="text-h6 font-weight-light">{{ route }}</span>
      <v-rating
        color="blue"
        half-increments
        half-icon="mdi-star-half"
        :value="(speed_rating + clean_rating + accuracy_rating) / 3"
        readonly
        background-color="blue"
      ></v-rating>
    </v-card-title>
    <v-card-subtitle>{{ date.toUTCString() }}</v-card-subtitle>
    <v-card-text class="text-h6 font-weight-bold">
      {{ content }}
    </v-card-text>
    <v-btn aria-label="vuetify-button" class="ma-2" color="primary" elevation="0" disabled>
      {{ speed_rating }}
      <v-icon dark right>
        mdi-speedometer-medium
      </v-icon>
    </v-btn>
    <v-btn aria-label="vuetify-button" class="ma-2" color="primary" elevation="0" disabled>
      {{ accuracy_rating }}
      <v-icon dark right>
        mdi-bullseye-arrow
      </v-icon>
    </v-btn>
    <v-btn aria-label="vuetify-button" class="ma-2" color="primary" elevation="0" disabled>
      {{ clean_rating }}
      <v-icon dark right>
        mdi-spray-bottle
      </v-icon>
    </v-btn>

    <!-- <v-card-actions>
      <v-list-item class="grow">
        <v-list-item-avatar color="grey darken-3">
          <v-img
            class="elevation-6"
            alt=""
            src="https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
          ></v-img>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>Anonymous</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-card-actions> -->
  </v-card>
</template>

<script>
export default {
  name: "Rating",
  props: {
    content: { type: String, required: true },
    route: { type: String, required: true },
    date: {
      type: Date,
      default: function() {
        return new Date();
      },
    },
    accuracy_rating: { type: Number, required: true },
    clean_rating: { type: Number, required: true },
    speed_rating: { type: Number, required: true },
  },
};
</script>

<style></style>
