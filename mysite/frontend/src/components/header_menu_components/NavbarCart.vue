<template>
  <div id="navCart" class="navbar-menu is-hidden-desktop" v-bind:class="{'is-active': is_active}">
    <div class="navbar-start">
      <p class="content">Your Cart is Empty</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NavbarCart',
  data: function () {
    return {
    }
  },
  computed: {
    is_active: function() {
      return this.$store.state.navbar.CartBar;
    }
  },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="sass">


</style>
