import Vue from "vue";
import Router from "vue-router";
// import VueDemo from "@/views/VueDemo";
import Home from "@/views/Home.vue";
import Messages from "@/views/Messages";
import News from "@/views/News.vue";
import Login from "@/views/Login.vue";
import Logout from "@/views/Logout.vue";
import MyAccount from "@/views/MyAccount.vue";
Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "home",
      component: Home,
    },
    {
      path: "/messages",
      name: "messages",
      component: Messages,
    },
    {
      path: "/ratings",
      name: "Ratings",
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () =>
        import(/* webpackChunkName: "about" */ "@/views/Rating.vue"),
    },
    {
      path: "/news",
      name: "News",
      component: News,
    },
    {
      path: "/login",
      name: "Login",
      component: Login,
    },
    {
      path: "/logout",
      name: "Logout",
      component: Logout,
      meta: {
        requiresLogin: true,
      },
    },
    {
      path: "/myaccount",
      name: "MyAccount",
      component: MyAccount,
      meta: {
        requiresLogin: true,
      },
    },
  ],
});
