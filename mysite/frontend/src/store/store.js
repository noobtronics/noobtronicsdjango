import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    navbar: {
      MenuBar: false,
      SearchBar: false,
      CartBar: false,
      AccountBar: false,
    }
  },
  mutations: {
    navbar_toggleMenuBar (state) {
      state.navbar.MenuBar = !state.navbar.MenuBar;
    },
    navbar_toggleSearchBar (state) {
      state.navbar.SearchBar = !state.navbar.SearchBar;
    },
    navbar_toggleCartBar (state) {
      state.navbar.CartBar = !state.navbar.CartBar;
    },
    navbar_toggleAccountBar (state) {
      state.navbar.AccountBar = !state.navbar.AccountBar;
    },
  }

})
