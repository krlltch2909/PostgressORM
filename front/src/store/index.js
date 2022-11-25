import { createStore } from 'vuex'

const store = createStore({
  state: {
    loggedIn: false,
    role: null,
    config: {
      headers:{
        'Authorization': 'Token ' + process.env.VUE_APP_BACKEND_TOKEN,
        'Content-Type': 'application/json',
        // TODO: Добавить как-то передачу кук в запросы
      }
    }
  },
  getters: {
    getLoggedIn: (state) => state.loggedIn,
    getConfig: (state) => state.config,
    getRole: (state) => state.role
  },
  mutations: {
    setLoggedIn(state, value) {
      state.loggedIn = value
    },
    setRole(state, value) {
      state.role = value
    },
  },
  actions: {
  },
  modules: {
  }
})

export default store
