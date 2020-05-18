

<script>
export default {
  name: 'SubscribeEmail',
  data: function () {
    return {
      'email': '',
    }
  },
  methods: {
    submit_email: function(){
        let self = this
        this.$http.post(
          '/api/subscribe_email',
          {'email': this.email}
        )
        .then(function (response) {
          self.$cookies.set('eid',response.data.email_token, { expires: 999 });
        })
        .catch(function (error) {
          console.log(error);
        })
        .then(function () {
        });
    }
  },
  computed: {

  },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="sass">


</style>
