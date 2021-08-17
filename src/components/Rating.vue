<template>
  <v-card class="ma-4 mx-auto" color="#ffdd55" max-width="80vw">
    <v-card-title>
      <v-icon large left>
        mdi-bus
      </v-icon>
      <span class="text-h6 font-weight-light">{{ route }}</span>
    </v-card-title>
    <v-card-subtitle>{{ date }}</v-card-subtitle>
    <v-card-text class="text-h6 font-weight-bold">
      {{ content }}
    </v-card-text>

    <v-card-actions>
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
    </v-card-actions>
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
  },
};
</script>

<style></style>
