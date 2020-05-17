

<script>
export default {
  name: 'Header_Menu',

  delimiters: ['[[', ']]'],


  data: function () {
    return {
      menu_btn: false,
      search_btn: false,
      cart_btn: false,
      account_btn: false,
    }
  },

  methods: {
    toggleSearchBar: function () {
      this.$store.commit('toggleSearchBar')
    },
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="sass">

.navbar-logo
  width: 14rem
  margin: auto

#navSearch
  color: black

  ::placeholder
    color: rgba(0,0,0,0.4)

#navCart
  color: black
  padding: 5px 10px


#navbartabs
  margin: 0

  a
    border-color: #4a4a4a
    margin: 0px 0px
    background-color: white

  .is-active
    a
      background-color: hsl(348, 100%, 61%)


.left-burger
  margin: 0
  width: 3rem

.left-search
  margin: 0
  position: relative
  width: 3rem

  svg
    top: calc(50% - 13px)
    left: calc(50% - 13px)
    position: absolute
    display: block

.right-search
  margin-left: auto


@import "bulma/sass/utilities/_all.sass"

+mobile
  .navbar-menu

    .has-dropdown
      .navbar-dropdown
        display: none

    .is-active
      .navbar-dropdown
        display: block



</style>
