import Vue from "vue";
import Vuex from "vuex";
import messages from "./modules/messages";
import { getAPI } from "axios";
Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    messages,
  },
  state: {
    accessToken: null,
    refreshToken: null,
  },
  mutations: {
    updateStorage(state, { access, refresh }) {
      state.accessToken = access;
      state.refreshToken = refresh;
    },
  },
  actions: {
    userLogin(context, usercredentials) {
      return new Promise((resolve, reject) => {
        getAPI
          .post("/api-token/", {
            username: usercredentials.username,
            password: usercredentials.password,
          })
          .then((response) => {
            context.commit("updateStorage", {
              access: response.data.access,
              refresh: response.data.refresh,
            });
            resolve();
          });
      });
    },
  },
});
