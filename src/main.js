import Vue from "vue";
import App from "@/App.vue";

import store from "@/store";
import router from "@/router";

import vuetify from "@/plugins/vuetify"; // path to vuetify export

Vue.config.productionTip = false;

// Vue.use(VueRouter)

const vue = new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
});

vue.$mount("#app");
