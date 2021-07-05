// src/plugins/vuetify.js

import Vue from "vue";
import Vuetify from "vuetify";
import "vuetify/dist/vuetify.min.css";
import en from "../locale/en";

Vue.use(Vuetify);

const opts = {
  lang: {
    locales: { en },
    current: "en",
  },
  theme: {
    themes: {
      light: {
        primary: "#1a73e8", // #E53935
      },
    },
  },
};

export default new Vuetify(opts);
