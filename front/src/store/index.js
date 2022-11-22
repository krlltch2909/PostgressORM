import { createStore } from 'vuex'

const store = createStore({
  state: {
    loggedIn: false,
  },
  getters: {
    getLoggedIn: (state) => state.loggedIn,
  },
  mutations: {
    setLoggedIn(state, value) {
      state.loggedIn = value
    }
  },
  actions: {
  },
  modules: {
  }
})

export default store
