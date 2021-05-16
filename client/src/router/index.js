import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import ChatRoom from '../views/ChatRoom.vue'
import JoinRoom from '../views/JoinRoom.vue'

import store from '../store/index.js'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    beforeEnter: function (to, from, next) {
      if (store.state.user.access == null) next({ name: 'Login' })
      next()
    }
  },
  {
    path: '/sign-in',
    name: 'Login',
    component: Login,
    beforeEnter: function (to, from, next) {
      if (store.state.user.access != null) next({ name: 'Home' })
      next()
    }
  },
  {
    path: '/sign-up',
    name: 'Register',
    component: Register,
    beforeEnter: function (to, from, next) {
      if (store.state.user.access != null) next({ name: 'Home' })
      next()
    }
  },
  {
    path: '/room/:slug/:roomToken/:roomId/:virtualId/:ownerId',
    name: 'ChatRoom',
    component: ChatRoom,
    beforeEnter: function (to, from, next) {
      if (store.state.user.access == null) next({ name: 'Login' })
      next()
    }
  },
  {
    path: '/join-room',
    name: 'JoinRoom',
    component: JoinRoom
  },
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
