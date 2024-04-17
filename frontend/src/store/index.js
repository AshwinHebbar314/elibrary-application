import { createStore } from 'vuex'

export default createStore({
  state: {
    BASEURL: 'http://localhost:5000',
    user: {
      token: null,
      roles: [],
      username: null,
      user_id: null
    }
  },
  getters: {
    BASEURL(state) {
      return state.BASEURL
    },
    getToken(state) {
      return state.user.token
    },
    getRoles(state) {
      return state.user.roles
    },
    getUserID(state) {
      return state.user.user_id
    }
  },
  mutations: {
    setUser(state, user) {
      state.user = user
      // check if json is stringified, if not then stringify it
      if (typeof user === 'object') {
        user = JSON.stringify(user)
      }
      sessionStorage.setItem('user', user)
    }
  }
})
