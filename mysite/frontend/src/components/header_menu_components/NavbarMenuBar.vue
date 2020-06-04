<template>
  <div class="navbar-menu" v-bind:class="{ 'is-active' : is_bar_active}">
    <div class="navbar-start">
      <a class="navbar-item" href="/">
        Home
      </a>
      <div class="navbar-item has-dropdown is-hoverable" v-bind:class="{'is-active': is_shop}">
        <a class="navbar-link" v-on:click="is_shop=!is_shop">
          Shop
        </a>
        <div class="navbar-dropdown " >
          <a class="navbar-item" href="/shop">
            All Products
          </a>
          <a class="navbar-item" href="/shop/microcontrollers">
            Microcontrollers
          </a>
          <a class="navbar-item" href="/shop/kits">
            Learning Kits
          </a>
          <a class="navbar-item" href="/shop/lcd">
            LCD Displays
          </a>
          <a class="navbar-item" href="/shop/tinkering-supply">
            Tinkering Supply
          </a>

        </div>
      </div>
      <div class="navbar-item has-dropdown is-hoverable" v-bind:class="{'is-active': is_blog}">
        <a class="navbar-link" v-on:click="is_blog=!is_blog">
          Blog
        </a>
        <div class="navbar-dropdown " >
          <a class="navbar-item" href="/blog">
            Blog Home
          </a>
          <a class="navbar-item" href="/blog/arduino">
            Arduino Blog
          </a>
          <a class="navbar-item" href="/blog/datasheet">
            Datasheet
          </a>

        </div>
      </div>
      <div class="navbar-item has-dropdown is-hoverable" v-bind:class="{'is-active': is_info}">
        <a class="navbar-link" v-on:click="is_info=!is_info">
          Information
        </a>
        <div class="navbar-dropdown " >
          <a class="navbar-item" href="/about-us">
            About Us
          </a>
          <a class="navbar-item" href="/contact-us">
            Contact Us
          </a>
          <a class="navbar-item" href="/contact-us">
            Delivery Locations
          </a>
        </div>
      </div>
    </div>

    <div class="navbar-end is-hidden-mobile">
      <div class="navbar-item">
        <div class="field is-grouped">
          <p class="control">
            <a class="bd-tw-button button ">
              <span class="icon">
                <img alt="store icon" class="lazyload" data-src="/static/images/icons/store_icon.png">
              </span>
              <span>
                Store
              </span>
            </a>
          </p>
          <p class="control">
            <a class="button badge is-inverted badge is-badge-danger cartbuttons" v-bind:data-badge="cart_count>0 ? cart_count : false" href="https://github.com/jgthms/bulma/releases/download/0.8.0/bulma-0.8.0.zip">
              <span class="icon">
                <img alt="checkout icon" class="lazyload" data-src="/static/images/icons/cart_icon.png">
              </span>
              <span>Checkout</span>
            </a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NavbarMenuBar',
  data: function () {
    return {
      is_shop: false,
      is_blog: false,
      is_info: false,
    }
  },
  computed: {
    is_bar_active: function() {
      return this.$store.state.navbar.MenuBar;
    },
    cart_count: function() {
      return this.$store.state.cart.cart_count;
    },
  },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="sass">


</style>
