var orderapp = new Vue({
    el: '#orderapp',
    delimiters: ['[%', '%]'],
    data: {
        ModalCancel: false,
        order_id: '',
        order_state_no: order_state_no
    },
    computed: {
    },
    methods: {
        confirm_cancel: function(order_id){
            this.order_id = order_id;
            this.ModalCancel = true;
        },
        cancel_order: function(){
            cancel_order();
        },
        open_prod_page: function(slug){
            var url = '/product/'+slug;
            var win = window.open(url, '_blank');
            win.focus();
        }
    }
});
