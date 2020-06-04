
import "@/assets/noobtronics-theme.sass";

import Vue from 'vue'

import Axios from 'axios'
Vue.prototype.$http = Axios;
Vue.prototype.$http.defaults.xsrfHeaderName = "X-CSRFToken";
Vue.prototype.$http.defaults.xsrfCookieName = "csrftoken";

Vue.config.devtools = process.env.NODE_ENV === 'development';

import Cookies from 'js-cookie'
Vue.prototype.$cookies = Cookies;

Vue.prototype.$log = console.log;

import StrigFormat from 'string-format'
Vue.prototype.$format = StrigFormat;

import lazySizes from 'lazysizes';
lazySizes.cfg.lazyClass = 'lazyload';



import Header_Menu from './components/Header_Menu.vue'



import SubscribeEmail from './components/header_menu_components/SubscribeEmail.vue'
import Home_Page from './components/Home_Page.vue'
import ProductPage_App from './components/Product_Page.vue'

import {store} from './store/store'


var header_menu_app = new Vue(Header_Menu);
header_menu_app.$store = store;
window.header_menu_app = header_menu_app;


function initialize_vuejs(){
  header_menu_app.$mount('#headermenu-app');
  window.init_vue_app();
}



function init_product_page_app(id) {
   var temp = new Vue(ProductPage_App);
   temp.$store = store;
   temp.$mount(id);
   window.product_page_app = temp;
}
window.init_product_page_app = init_product_page_app;



function init_subscribe_email(id) {
   new Vue(SubscribeEmail).$mount(id);
}
window.init_subscribe_email = init_subscribe_email;


function init_home_page() {
  new Vue({
    render: h => h(Home_Page),
  }).$mount('#components-demo')
}

window.init_home_page = init_home_page;


window.initialize_vuejs = initialize_vuejs;

if(window.load_vuejs){
  initialize_vuejs();
}
