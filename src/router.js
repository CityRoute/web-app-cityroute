import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("@/components/BusMap.vue"),
      children: [
        {
          path: "directions",
          component: () => import("@/components/BusMap.vue"),
        },
        {
          path: "route-viewer",
          component: () => import("@/components/BusMap.vue"),
        },
        {
          path: "stop-finder",
          component: () => import("@/components/BusMap.vue"),
        },
        {
          path: "landmarks",
          component: () => import("@/components/BusMap.vue"),
        },
        {
          path: "favourites",
          component: () => import("@/components/BusMap.vue"),
        },
      ],
    },
    {
      path: "/ratings",
      name: "Ratings",
      component: () => import("@/views/Rating.vue"),
    },
    {
      path: "/news",
      name: "News",
      component: () => import("@/views/News.vue"),
    },
    {
      path: "/login",
      name: "Login",
      component: () => import("@/views/Login.vue"),
    },
    {
      path: "/logout",
      name: "Logout",
      component: () => import("@/views/Logout.vue"),
      meta: {
        requiresLogin: true,
      },
    },
    {
      path: "/myaccount",
      name: "MyAccount",
      component: () => import("@/views/MyAccount.vue"),
      meta: {
        requiresLogin: true,
      },
    },
    {
      path: "/auth",
      component: () => import("@/views/Auth/Auth.vue"),
      children: [
        {
          path: "signin",
          component: () => import("@/views/Auth/Signin.vue"),
          children: [
            {
              path: "identifier",
              name: "signin",
              component: () => import("@/views/Auth/SigninIdentifier.vue"),
            },
            {
              path: "password",
              name: "password",
              component: () => import("@/views/Auth/SigninPassword.vue"),
            },
            {
              path: "forgot-password",
              name: "forgot-password",
              component: () => import("@/views/Auth/SigninForgotPassword.vue"),
            },
            {
              path: "forgot-password-reset",
              name: "forgot-password-reset",
              component: () =>
                import("@/views/Auth/SigninForgotPasswordReset.vue"),
            },
          ],
        },
        {
          path: "signup",
          component: () => import("@/views/Auth/Signup.vue"),
          name: "signup",
        },
      ],
    },
  ],
});
