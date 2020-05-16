import Vue from 'vue'
import HelloWorld from './components/HelloWorld.vue'


window.Vue=Vue;

function test() {
  new Vue({
    render: h => h(HelloWorld),
  }).$mount('#components-demo')
}

window.test = test;
