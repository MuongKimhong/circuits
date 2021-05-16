import VuexPersistence from 'vuex-persist'
import Vuex from 'vuex'
import Vue from 'vue'


Vue.use(Vuex)

const vuexLocal = new VuexPersistence({ storage: window.localStorage })


export default new Vuex.Store({
  plugins: [vuexLocal.plugin],

  state: {
    user: { username: null, access: null, id: null, refresh: null }
  },

  mutations: {
    getUserInfo(state, info) {
      state.user = info
    },
    deleteUserInfo(state) {
      for (var key in state.user) {
        state.user[key] = null
      }
    }
  },

  actions: {
  },

  modules: {
  }
})
