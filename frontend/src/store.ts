import { createStore } from 'vuex';

const store = createStore({
  state: {
    isLoggedIn: false,
    user: null,
  },
  mutations: {
    login(state) {
      state.isLoggedIn = true;
    },
    logout(state) {
      state.isLoggedIn = false;
      state.user = null;
    },
    setUser(state, userData) {
      state.user = userData;
    },
  },
  actions: {
    setUser({ commit }, userData) {
      commit('setUser', userData);
    },
    login({ commit }) {
      commit('login');
    },
    logout({ commit }) {
      sessionStorage.removeItem('token')
      localStorage.removeItem('myAppData')
      commit('logout');
    },
  },
  getters: {
    getUser(state) {
      return state.user;
    },
  },
});

store.subscribe((mutation, state) => {
  localStorage.setItem('myAppData', JSON.stringify(state));
});

export default store;
