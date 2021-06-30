import Vue from "vue";
import Vuex from "vuex";
import messages from "./modules/messages";
import axios from "axios";
Vue.use(Vuex);
import createPersistedState from "vuex-persistedstate";

export default new Vuex.Store({
  plugins: [createPersistedState()],
  modules: {
    messages,
  },
  state: {
    accessToken: null,
    refreshToken: null,
    APIData: "",
    identifier: "",
    password: "",
    loading: false,
    disabled: false,
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
    updateIdentifier(state, identifier) {
      state.identifier = identifier;
    },

    updatePassword(state, password) {
      state.password = password;
    },

    setLoading(state, loading) {
      state.loading = loading;
    },

    setDisabled(state, disabled) {
      state.disabled = disabled;
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
    userSignup(context, usercredentials) {
      return new Promise((resolve, reject) => {
        axios
          .post("/api/register", {
            username: usercredentials.username,
            password: usercredentials.password,
            email: usercredentials.email,
            first_name: usercredentials.first_name,
            last_name: usercredentials.last_name,
          })
          .then((response) => {
            // not needed for login
            // context.commit("updateStorage", {
            //   access: response.data.access,
            //   refresh: response.data.refresh,
            // });
            console.log(response);
            resolve();
          })
          .catch((err) => {
            reject(err);
          });
      });
    },
  },
});
