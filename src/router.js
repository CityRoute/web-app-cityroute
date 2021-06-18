import Vue from 'vue'
import Router from 'vue-router'
import VueDemo from "@/views/VueDemo";
import Messages from '@/views/Messages'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: VueDemo
    },
    {
      path: '/messages',
      name: 'messages',
      component: Messages
    }
  ]
})
