import Vue from "vue";
import Router from "vue-router"
const News = () => import("@/views/News.vue");
const Login = () => import("@/views/Login.vue");
const Logout = () => import("@/views/Logout.vue");
const MyAccount = () => import("@/views/MyAccount.vue");
const Auth = () => import("@/views/Auth/Auth.vue");
const Signin = () => import("@/views/Auth/Signin.vue");
const SigninIdentifier = () => import("@/views/Auth/SigninIdentifier.vue");
const SigninPassword = () => import("@/views/Auth/SigninPassword.vue");
const SigninForgotPassword = () =>
  import("@/views/Auth/SigninForgotPassword.vue");
const SigninForgotPasswordReset = () =>
  import("@/views/Auth/SigninForgotPasswordReset.vue");
const Signup = () => import("@/views/Auth/Signup.vue");

const BusMap = () => import("@/components/BusMap.vue");

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "home",
      component: BusMap,
      children: [
        {
          path: "directions",
          component: BusMap,
        },
        {
          path: "route-viewer",
          component: BusMap,
        },
        {
          path: "stop-finder",
          component: BusMap,
        },
        {
          path: "landmarks",
          component: BusMap,
        },
        {
          path: "favourites",
          component: BusMap,
        },
      ],
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
