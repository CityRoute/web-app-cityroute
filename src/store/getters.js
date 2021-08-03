// https://vuex.vuejs.org/en/getters.html

// authorized lets you know if the token is true or not, its exported to be used to check state elsewhere(In router. app.vue. toolbar.vue)
//auth status isn't used anywhere??? why did i do this
export default {
  authorized: (state) => !!state.token,
  authstatus: (state) => state.authStatus,
  loggedIn(state) {
    // console.log(state.accessToken);
    return state.accessToken != null;
  },
};
