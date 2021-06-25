import Vue from "vue";
import Vuex from "vuex";
import messages from "./modules/messages";
import axios from "axios";
Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    messages,
  },
  state: {
    accessToken: null,
    refreshToken: null,
    APIData: "",
  },
  mutations: {
    updateStorage(state, { access, refresh }) {
      state.accessToken = access;
      state.refreshToken = refresh;
    },
    destroyToken(state) {
      state.accessToken = null;
      state.refreshToken = null;
    },
  },
  getters: {
    loggedIn(state) {
      console.log(state.accessToken);
      return state.accessToken != null;
    },
  },
  actions: {
    userLogout(context) {
      if (context.getters.loggedIn) {
        context.commit("destroyToken");
      }
    },
    userLogin(context, usercredentials) {
      return new Promise((resolve, reject) => {
        axios
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
          })
          .catch((err) => {
            reject(err);
          });
      });
    },
  },
});
