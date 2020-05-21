
import "@/assets/noobtronics-theme.sass";

import Vue from 'vue'

import Axios from 'axios'
Vue.prototype.$http = Axios;
Vue.prototype.$http.defaults.xsrfHeaderName = "X-CSRFToken";
Vue.prototype.$http.defaults.xsrfCookieName = "csrftoken";

Vue.config.devtools = process.env.NODE_ENV === 'development';

import Cookies from 'js-cookie'
Vue.prototype.$cookies = Cookies;


import Header_Menu from './components/Header_Menu.vue'



import SubscribeEmail from './components/header_menu_components/SubscribeEmail.vue'
import Home_Page from './components/Home_Page.vue'
import Product_Page from './components/Product_Page.vue'

import {store} from './store/store'



var header_menu_app = new Vue(Header_Menu);
header_menu_app.$store = store;
header_menu_app.$mount('#headermenu-app');
window.header_menu_app = header_menu_app;





function init_subscribe_email(id) {
   new Vue(SubscribeEmail).$mount(id);
}
window.init_subscribe_email = init_subscribe_email;


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



window.init_vue_app();
