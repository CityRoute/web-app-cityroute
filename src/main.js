import Vue from "vue";
import App from "@/App.vue";

import store from "@/store";
import router from "@/router";
import vuetify from "@/plugins/vuetify"; // path to vuetify export
import VueSocialSharing from "vue-social-sharing";

Vue.config.productionTip = false;
Vue.use(VueSocialSharing);
// Vue.use(VueRouter)

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresLogin)) {
    if (!store.getters.loggedIn) {
      next({ name: "signin" });
    } else {
      next();
    }
  } else {
    next();
  }
});

const vue = new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
});

vue.$mount("#app");
