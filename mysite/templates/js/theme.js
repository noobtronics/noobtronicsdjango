/*! lozad.js - v1.14.0 - 2019-10-19
* https://github.com/ApoorvSaxena/lozad.js
* Copyright (c) 2019 Apoorv Saxena; Licensed MIT */
!function(t,e){"object"==typeof exports&&"undefined"!=typeof module?module.exports=e():"function"==typeof define&&define.amd?define(e):(t=t||self).lozad=e()}(this,function(){"use strict";
/**
   * Detect IE browser
   * @const {boolean}
   * @private
   */var d="undefined"!=typeof document&&document.documentMode,c={rootMargin:"0px",threshold:0,load:function(t){if("picture"===t.nodeName.toLowerCase()){var e=document.createElement("img");d&&t.getAttribute("data-iesrc")&&(e.src=t.getAttribute("data-iesrc")),t.getAttribute("data-alt")&&(e.alt=t.getAttribute("data-alt")),t.append(e)}if("video"===t.nodeName.toLowerCase()&&!t.getAttribute("data-src")&&t.children){for(var r=t.children,a=void 0,o=0;o<=r.length-1;o++)(a=r[o].getAttribute("data-src"))&&(r[o].src=a);t.load()}if(t.getAttribute("data-src")&&(t.src=t.getAttribute("data-src")),t.getAttribute("data-srcset")&&t.setAttribute("srcset",t.getAttribute("data-srcset")),t.getAttribute("data-background-image"))t.style.backgroundImage="url('"+t.getAttribute("data-background-image").split(",").join("'),url('")+"')";else if(t.getAttribute("data-background-image-set")){var i=t.getAttribute("data-background-image-set").split(","),n=i[0].substr(0,i[0].indexOf(" "))||i[0];// Substring before ... 1x
n=-1===n.indexOf("url(")?"url("+n+")":n,1===i.length?t.style.backgroundImage=n:t.setAttribute("style",(t.getAttribute("style")||"")+"background-image: "+n+"; background-image: -webkit-image-set("+i+"); background-image: image-set("+i+")")}t.getAttribute("data-toggle-class")&&t.classList.toggle(t.getAttribute("data-toggle-class"))},loaded:function(){}};function l(t){t.setAttribute("data-loaded",!0)}var b=function(t){return"true"===t.getAttribute("data-loaded")};return function(){var r,a,o=0<arguments.length&&void 0!==arguments[0]?arguments[0]:".lozad",t=1<arguments.length&&void 0!==arguments[1]?arguments[1]:{},e=Object.assign({},c,t),i=e.root,n=e.rootMargin,d=e.threshold,u=e.load,s=e.loaded,g=void 0;return"undefined"!=typeof window&&window.IntersectionObserver&&(g=new IntersectionObserver((r=u,a=s,function(t,e){t.forEach(function(t){(0<t.intersectionRatio||t.isIntersecting)&&(e.unobserve(t.target),b(t.target)||(r(t.target),l(t.target),a(t.target)))})}),{root:i,rootMargin:n,threshold:d})),{observe:function(){for(var t=function(t){var e=1<arguments.length&&void 0!==arguments[1]?arguments[1]:document;return t instanceof Element?[t]:t instanceof NodeList?t:e.querySelectorAll(t)}(o,i),e=0;e<t.length;e++)b(t[e])||(g?g.observe(t[e]):(u(t[e]),l(t[e]),s(t[e])))},triggerLoad:function(t){b(t)||(u(t),l(t),s(t))},observer:g}}});

//
// var initialize_navbar = function(){
//   // Get all "navbar-burger" elements
//   const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
//   // Check if there are any navbar burgers
//   if ($navbarBurgers.length > 0) {
//     // Add a click event on each of them
//     $navbarBurgers.forEach( el => {
//       el.addEventListener('click', () => {
//         // Get the target from the "data-target" attribute
//         const target = el.dataset.target;
//         const $target = document.getElementById(target);
//         // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
//         el.classList.toggle('is-active');
//         $target.classList.toggle('is-active');
//
//       });
//     });
//   }
//   const $navLinks = Array.prototype.slice.call(document.querySelectorAll('.navbar-link'), 0);
//   if ($navLinks.length > 0) {
//     $navLinks.forEach( el => {
//       el.addEventListener('click', () => {
//         // Get the target from the "data-target" attribute
//         const target = el.dataset.target;
//         const $target = document.getElementById(target);
//         // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
//         el.classList.toggle('is-active');
//         $target.classList.toggle('is-active');
//       });
//     });
//   }
// };


document.addEventListener('DOMContentLoaded', () => {

  // initialize lozad
  const observer = lozad(); // lazy loads elements with default selector as '.lozad'
  observer.observe();

});
