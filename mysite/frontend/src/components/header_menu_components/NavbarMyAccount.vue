<template>
  <div id="navAccount" class="navbar-menu is-hidden-desktop" v-bind:class="{'is-active': is_active}">
    <div class="navbar-start">
      <a class="navbar-item" href="https://bulma.io/">
        Log In
      </a>
      <a class="navbar-item" href="https://bulma.io/">
        Sign Up
      </a>
      <a class="navbar-item" href="https://bulma.io/">
        Your Orders
      </a>
      <a class="navbar-item" href="https://bulma.io/">
        Logout
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NavbarMyAccount',
  data: function () {
    return {
    }
  },
  computed: {
    is_active: function() {
      return this.$store.state.navbar.AccountBar;
    }
  },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="sass">


</style>
