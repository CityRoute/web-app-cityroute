<template>
  <v-container id="landmarksContainer">
      <div v-for="(item, index) in categories" v-bind:key="item.name">
          <v-switch
          inset
            color="amber"
            :prepend-icon="item.icon"
            :value="true"
            :label="item.name"
            :input-value="item.shown"
            @change="categories[index].shown = !categories[index].shown"
          ></v-switch>
      </div>
  </v-container>
</template>

<script>
import {
  mdiHospitalBuilding,
  mdiShopping,
  mdiFactory,
  mdiTicket,
  mdiSchool,
  mdiMapMarkerQuestionOutline,
  mdiDramaMasks,
  mdiTheater,
  mdiAccountChild,
  mdiMapMarkerRadius,
  mdiMusicNoteOutline,
  mdiBasketball,
} from "@mdi/js";

export default {
  methods: {},
  data() {
    return {
      categories: {
        Hospital: {
          shown: false,
          name: "Hospital",
          isVenue: false,
          icon: mdiHospitalBuilding,
        },
        Shopping: {
          shown: false,
          name: "Shopping",
          isVenue: false,
          icon: mdiShopping,
        },
        Industrial: {
          shown: false,
          name: "Industrial",
          isVenue: false,
          icon: mdiFactory,
        },
        Attraction: {
          shown: false,
          name: "Attraction",
          isVenue: false,
          icon: mdiTicket,
        },
        College: {
          shown: false,
          name: "College",
          isVenue: false,
          icon: mdiSchool,
        },
        Other: {
          shown: false,
          name: "Other",
          isVenue: false,
          icon: mdiMapMarkerQuestionOutline,
        },
        Arts: {
          shown: false,
          name: "Arts, Theatre & Comedy",
          isVenue: true,
          icon: mdiDramaMasks,
        },
        Exhibition: {
          shown: false,
          name: "Exhibition",
          isVenue: true,
          icon: mdiTheater,
        },
        Family: {
          shown: false,
          name: "Family & Attractions",
          isVenue: true,
          icon: mdiAccountChild,
        },
        Miscellaneous: {
          shown: false,
          name: "Miscellaneous",
          isVenue: true,
          icon: mdiMapMarkerRadius,
        },
        Music: {
          shown: false,
          name: "Music",
          isVenue: true,
          icon: mdiMusicNoteOutline,
        },
        Sport: {
          shown: false,
          name: "Sport",
          isVenue: true,
          icon: mdiBasketball,
        },
      },
    };
  },
};
</script>

<style>
#landmarksContainer {
  height: 30vh;
  overflow-y: auto;
}
</style>
