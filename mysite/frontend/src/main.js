
import "@/assets/noobtronics-theme.sass";


import Vue from 'vue'
import Header_Menu from './components/Header_Menu.vue'
import Notifications_App from './components/Notifications_App.vue'
import Home_Page from './components/Home_Page.vue'
import Product_Page from './components/Product_Page.vue'

window.Vue=Vue;

function init_header_menu() {
  new Vue({
    render: h => h(Header_Menu),
  }).$mount('#components-demo')
}

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


new Vue({
  render: h => h(Notifications_App),
}).$mount('#notifications-app')


window.init_header_menu = init_header_menu;
window.init_home_page = init_home_page;
window.init_product_page = init_product_page;
