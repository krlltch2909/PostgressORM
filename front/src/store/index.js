import { createStore } from 'vuex'

const store = createStore({
  state: {
    loggedIn: false,
    role: null,
    config: {
      headers:{
        // ХАРДКОД (╯°□°）╯︵ ┻━┻
        'Authorization': 'Token e222cdf2fae4ff2e6494640269f150b4ff52f468'
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
    }
  },
  actions: {
  },
  modules: {
  }
})

export default store
