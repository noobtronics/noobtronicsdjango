
import "@/assets/noobtronics-theme.sass";


import Vue from 'vue'

import SearchBar from './components/header_menu_components/SearchBar.vue'
import Header_Menu from './components/Header_Menu.vue'

import Home_Page from './components/Home_Page.vue'
import Product_Page from './components/Product_Page.vue'

import {store} from './store/store'



var header_menu_app = new Vue(Header_Menu);
header_menu_app.$store = store;
header_menu_app.$mount('#headermenu-app');
window.header_menu_app = header_menu_app;


var searchbar = new Vue({
  render: h => h(SearchBar),
  store,
})
searchbar.$mount('#SearchBar')

window.searchbar = searchbar;


window.Header_Menu = Header_Menu;


function init_home_page() {
  new Vue({
    render: h => h(Home_Page),
  }).$mount('#components-demo')
}

function init_product_page() {
  new Vue({
    render: h => h(Product_Page),
  }).$mount('#components-demo')
}




window.init_home_page = init_home_page;
window.init_product_page = init_product_page;
