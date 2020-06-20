var cartapp = new Vue({
    el: '#cartapp',
    delimiters: ['[%', '%]'],
    data: {
        subtotal: subtotal,
        deliverycharge: deliverycharge,
        extracharge: extracharge,
        total: total,
        products: products,
        prod_id_index: prod_id_index,
        ModalDeleteConfirm: false,
        ModalAlert: false,
        cart_state: cart_state,
        confirm_name: '',
        confirm_sub: '',
        confirm_qty: '',
        alert_title: '',
        alert_message: '',
        pincode: '',
        pincodedisplay: '',

        address_name:'',
        address_mobile:'',
        address_email: '',
        address_address1:'',
        address_address2:'',

        paymode: 'razorpay',
        ModalCod: false,
        ModalCodConfirm: false,

        referral_code: '',
        referrer: '',
        referrer_details: '',
        show_referral: false,
    },
    computed: {
        rsubtotal: function () {
            return '₹' + this.subtotal.toString();
        },
        rdeliverycharge: function () {
            return '₹' + this.deliverycharge.toString();
        },
        rextracharge: function () {
            return '₹' + this.extracharge.toString();
        },
        rtotal: function () {
            return '₹' + this.total.toString();
        },
        carttitlename: function(){
            if(this.cart_state==0){
                return "Shopping Cart";
            }
            if(this.cart_state==1){
                return "Shipping Address";
            }
            if(this.cart_state==2){
                return "Payment Method";
            }
            if(this.cart_state==3){
                return "Confirmation";
            }

        }

    },
    methods: {
        increase_qty: function(cp_id){
            edit_cart('increase', cp_id);
        },
        decrease_qty: function(cp_id){
            var idx = this.prod_id_index[cp_id];
            var qty = this.products[idx].qty;
            if(qty==1) {
                this.remove_prod(cp_id);
            }
            else{
                edit_cart('decrease', cp_id);
            }
        },
        remove_prod: function(cp_id){
            var idx = this.prod_id_index[cp_id];
            var prod = this.products[idx];
            this.confirm_name = prod.title;
            this.confirm_sub = prod.subtitle;
            this.confirm_qty = prod.qty;
            this.confirm_id = cp_id;
            this.ModalDeleteConfirm = true;
        },
        remove: function(){
            edit_cart('remove', this.confirm_id);
            this.ModalDeleteConfirm = false;
        },
        open_prod_page: function(slug){
            var url = '/product/'+slug;
            var win = window.open(url, '_blank');
            win.focus();
        },
        checkout: function(){
            checkout();
        },
        undocheckout: function(){
            undocheckout();
        },
        undoaddress: function(){
            undoaddress();
        },
        submit_address: function(){
            validate_address();
        },
        update_paymode: function(){
            update_paymode();
        },
        apply_referral_code: function(){
            apply_referral_code();
        },
        handle_pay: function(){
            if(this.paymode=='cod'){
                this.ModalCodConfirm = true;
            }
            else{
                this.submit_pay();
            }
        },
        submit_pay: function(){
            if(this.paymode==''){
                alert_msg('Error', 'Please select Payment Method first')
            } else{
                submit_pay();
            }
        }
    },
    watch: {
        pincode: function(newVal, oldVal){
            if(newVal.length==6){
                if(!isNaN(newVal)){
                    get_pincode_details(newVal);
                }
            }
        },
        paymode: function(newVal, oldVal){
            if(newVal == 'cod') {
                this.ModalCod = true;
            }
            else{
                if(newVal != oldVal){
                    update_paymode();
                }
            }
        },
        cart_state: function(newVal, oldVal){
            if(newVal > oldVal){
                ga('ec:setAction','checkout', {
                    'step': newVal + 1,
                });
                ga('send', 'pageview');
            }
            if(newVal == 3){
                setTimeout(function(){ window.location = "/orders"; }, 2000);
            }

        }
    }
});
