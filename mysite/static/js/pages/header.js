Vue.config.delimiters = ['[%', '%]'];


//var openDeliveryWindow = function(){};

var head_app = new Vue({
    el: '#head_app',
    data: {
        ModalLogin: false,
        loading: false,
        cartqty: cartqty,
        ModalAbout: false,
        HeadModalDelivery: false,
        downloadAbout: true,
        ModalContactUs: false,
        show_mob_nav: false,
        show_mob_acct: false,
        show_mob_shop: false,
        ask_mobile: false,
        location: {},
        mobileinput : '',
        login_email: '',
        login_pwd: '',
        login_help: '',
        login_forgot: 'Forgot Password ?',
    },
    methods: {
        processLogout: function () {
            processLogout();
        },
        handle_cart_click: function(){
            if(this.cartqty > 0){
                window.location='/cart';
            }
            else{

            }
        },
        openAboutWindow:function(){
            openAboutWindow();
        },
        openContactUsWindow: function(){
            this.ModalContactUs = true;
        },
        submit_mobile: function(){
            submit_mobile();
        },
        process_email_login: function(){
            process_email_login();
        },
        process_forgot_pwd: function(){
            process_forgot_pwd();
        },

    }
})

var csrfmiddlewaretoken = getCookie('csrftoken');

var submit_mobile = function(){
  if(head_app.mobileinput.length != 10){
    $("#askmobdiv").find("input").addClass("is-danger");
    $("#askmobdiv").find(".help").html("Enter 10 digit mobile correctly");
    return;
  }
  if(isNaN(head_app.mobileinput)){
    $("#askmobdiv").find("input").addClass("is-danger");
    $("#askmobdiv").find(".help").html("Enter 10 digit mobile correctly");
    return;
  }

  processSaveMobile();
}

function onSignIn(googleUser) {
    if(user_authenticated){
        return;
    }
    var auth2 = gapi.auth2.getAuthInstance();
    var profile = auth2.currentUser.get().getBasicProfile();

    var d = {
        id_token: googleUser.getAuthResponse().id_token,
        first_name: profile.getGivenName(),
        last_name: profile.getFamilyName(),
        email: profile.getEmail(),
        uri: location.pathname.substring(1)
    };
    processLogin(d);
}




var processLogin = function(d){
    head_app.loading = true;
    axios({
        method: 'post',
        url: '/api/login',
        data: d
    }).then(function(response) {
        console.log(response);
        head_app.loading = false;
        if(response.data.success){
            location.reload();
        }
    });
};

var processLogout = function(){
    head_app.loading = true;
    axios({
        method: 'post',
        url: '/api/logout'
    }).then(function(response) {
        head_app.loading = false;
        if(response.data.success){
            console.log('logging out...');
            window.location.reload();
        }
    });
};


var processSaveMobile = function(d){
    head_app.loading = true;

    axios({
        method: 'post',
        url: '/api/savemobile',
        data: {
          'mobile': head_app.mobileinput,
          'location': head_app.location,
        }
    }).then(function(response) {

        if(response.data.success){


          setCookie('mmid', response.data.mmid, 1000);

          ga('send', {
            hitType: 'event',
            eventCategory: 'User',
            eventAction: 'Registration',
            eventLabel: 'SignUp',
            eventValue: 1
          });

        }


    }).finally(function () {
      head_app.loading = false;
      head_app.ask_mobile = false;
    });


};



var footer_app = new Vue({
    el: '#footer_app',
    data: {
        ModalDelivery: false,
        ModalPayment: false,
        ModalTC: false,
        LegalactivePage:0,
        Legaldata:['', '', ''],
        downloadTC: true,
        downloadDelivery: true,
        downloadPayment: true,
    },
    computed: {
        Legaldisplay: function () {
            return this.Legaldata[this.LegalactivePage]
        }
    },
    methods: {
        LegalchangePage:function(pageNumber){
            this.LegalactivePage=pageNumber;
        },

        openLegalWindow:function(){
            openLegalWindow();
        },
        openDeliveryWindow:function(){
            openDeliveryWindow();
        },
        openPaymentWindow:function(){
            openPaymentWindow();
        }
    }
})
