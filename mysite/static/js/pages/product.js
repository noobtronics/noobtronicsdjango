var prodapp = new Vue({
    el: '#prodapp',
    delimiters: ['[%', '%]'],
    data: {
        activePage:0,
        data: prod_details_data,
        image_data: image_data,
        image_selected: 0,
        quantity: 1,
        related_products: related_products,
        similar_products: similar_products,
        show_checkout: show_checkout,
    },
    computed: {
        display: function () {
            return this.data[this.activePage]
        }
    },
    methods: {
        changePage:function(pageNumber){
            this.activePage=pageNumber;
        },
        openPage:function(url){
            window.location=url;
        },
        openPhotoSwipe:function(){
            openPhotoSwipe();
        },
        increaseQty: function(){
            this.quantity = this.quantity + 1;
        },
        decreaseQty: function(){
            if(this.quantity >= 2){
                this.quantity = this.quantity - 1;
            }
        },
        add_to_cart: function(){
                add_to_cart();
        },
        add_to_waitlist: function(){
            if(!user_authenticated){
                head_app.ModalLogin = true;
            }
            else{
                add_to_waitlist();
            }
        },
        open_prod_page: function(slug){
            var url = '/product/'+slug;
            var win = window.open(url,'_self');
            win.focus();
        },
    },
    watch:{
        image_selected: function(newVal, oldVal){
            var url = image_data.home_images[newVal];
            var doc_img = document.createElement("img");
            doc_img.src = url;
            var ele =document.getElementById("proddisplayi");
            ele.childNodes[0].remove();
            ele.appendChild(doc_img);
        }
    }
})
