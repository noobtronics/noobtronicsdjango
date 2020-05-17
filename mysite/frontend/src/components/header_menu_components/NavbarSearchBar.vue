<template>
  <div id="navSearch" class="navbar-menu is-hidden-desktop" v-bind:class="{'is-active': is_active}">
    <div class="field has-addons" style="padding: 5px;">
      <div class="control is-expanded">
        <input class="input" placeholder="find product, blog eg. 'arduino uno' " aria-label="email" aria-describedby="call-to-action-search">
      </div>
      <div class="control">
        <button class="button is-danger" id="call-to-action-search">Search</button>
      </div>
    </div>
  </div>

</template>

<script>
export default {
  name: 'SearchBar',
  data: function () {
    return {
    }
  },
  computed: {
    is_active: function() {
      return this.$store.state.navbar.SearchBar;
    }
  },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="sass">


</style>
