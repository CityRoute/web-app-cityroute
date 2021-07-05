import Vue from "vue";
import Router from "vue-router";
// import VueDemo from "@/views/VueDemo";
import Home from "@/views/Home.vue";
import Messages from "@/views/Messages";
import News from "@/views/News.vue";
import Login from "@/views/Login.vue";
import Logout from "@/views/Logout.vue";
import MyAccount from "@/views/MyAccount.vue";

import Auth from "@/views/Auth/Auth";
import Signin from "@/views/Auth/Signin";
import SigninIdentifier from "@/views/Auth/SigninIdentifier";
import SigninPassword from "@/views/Auth/SigninPassword";
import SigninForgotPassword from "@/views/Auth/SigninForgotPassword";
import SigninForgotPasswordReset from "@/views/Auth/SigninForgotPasswordReset";

import Signup from "@/views/Auth/Signup";

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
    {
      path: "/auth",
      component: Auth,
      children: [
        {
          path: "signin",
          component: Signin,
          children: [
            {
              path: "identifier",
              name: "signin",
              component: SigninIdentifier,
            },
            {
              path: "password",
              name: "password",
              component: SigninPassword,
            },
            {
              path: "forgot-password",
              name: "forgot-password",
              component: SigninForgotPassword,
            },
            {
              path: "forgot-password-reset",
              name: "forgot-password-reset",
              component: SigninForgotPasswordReset,
            },
          ],
        },
        {
          path: "signup",
          component: Signup,
          name: "signup",
        },
      ],
    },
  ],
});
