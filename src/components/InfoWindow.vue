<template>
  <div id="infoWindowDiv" @click="goFullScreen()">
    <v-card max-width="250" class="mx-auto" id="infoWindowCard" outlined>
      <v-list-item three-line>
        <v-list-item-content>
          <v-list-item-title class="text-h5 mb-1">
            Stop 297
          </v-list-item-title>
          <v-list-item-subtitle
            >Eden Quay, Marlborough Street</v-list-item-subtitle
          >
          <div class="text-overline mb-4">Updated: <strong>2:45pm</strong></div>
        </v-list-item-content>
      </v-list-item>

      <v-simple-table dark id="infoWindowTimes">
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-left">
                Bus
              </th>
              <th class="text-left">
                Destination
              </th>
              <th class="text-left">
                ETA
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in desserts" :key="item.name">
              <td>{{ item.name }}</td>
              <td>{{ item.calories }}</td>
              <td>10 mins</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card>
  </div>
</template>

<script>
// window.addEventListener("load", function(event) {
//   var divTag = document.getElementById("infoWindowDiv");

//   divTag.setAttribute("onclick", "goFullScreen()");
// });

module.exports = {
  name: "infowindow",
  methods: {
    goFullScreen() {
      var elem = document.getElementById("infoWindowDiv");

      if (elem.requestFullscreen) {
        elem.requestFullscreen();
      } else if (elem.mozRequestFullScreen) {
        elem.mozRequestFullScreen();
      } else if (elem.webkitRequestFullscreen) {
        elem.webkitRequestFullscreen();
      } else if (elem.msRequestFullscreen) {
        elem.msRequestFullscreen();
      }
    },
  },
  data() {
    return {
      desserts: [
        {
          name: "60",
          calories: "Dest 1",
        },
        {
          name: "66a",
          calories: "Dest 2",
        },
        {
          name: "145",
          calories: "Dest 3",
        },
      ],
    };
  },

  props: ["content"],
};
</script>
<style>
#infoWindowCard {
  background: rgb(254, 203, 101);
  background: radial-gradient(
    circle,
    rgba(254, 203, 101, 1) 0%,
    rgba(255, 222, 138, 1) 100%
  );
}

#infoWindowTimes {
  background: rgb(44, 47, 44);
}
</style>
