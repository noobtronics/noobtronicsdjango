var app = new Vue({
    el: '#app',
    delimiters: ['[%', '%]'],
    data: {
        products: products_data,
        menu_selected: menu_data,
        table_page: page_number,
        total_pages: total_pages,
        filterbtnactive: false,
        shifted_to_dynamic: false,
        show_checkout: show_checkout,
    },
    methods :{
        change_menu: function(idx, val) {
            for(var i = idx+1; i<= 5; ++i){
                Vue.set(this.menu_selected, i, 0);
            }
            Vue.set(this.menu_selected, idx, val);
            document.getElementById("shopmenu").reset();
            update_menu_prods(1);
        },
        update_menu_prods: function(page_number){
            update_menu_prods(page_number);
        },
        update_checkbox_prods: function(page_number, tagid){
            for(var i=0; i< this.menu_selected.length; i++){
                if(this.menu_selected[i]==tagid){
                    this.menu_selected[i]=0;
                    break;
                }
            }
            update_menu_prods(page_number);
        },
        open_prod_page: function(slug){
            var url = '/product/'+slug;
            var win = window.open(url, '_blank');
            win.focus();
        },
        change_page: function(new_page){
            if(this.table_page != new_page){
                this.table_page = new_page;
                update_menu_prods(new_page);
            }
        },
        min: function(a,b){
            if(a>=b){
                return b;
            }
            return a;
        },
        max: function(a,b){
            if(a>=b){
                return a;
            }
            return b;
        },
        get_pages: function(){
            var start_page = this.max(this.table_page-5, 1);
            var end_page = this.min(this.table_page+5, this.total_pages);
            var ls = [];
            for(var i=start_page; i <= end_page; i++){
                ls.push(i);
            }
            return ls;
        },
        add_to_cart: function(prod_id){
            event.stopPropagation();
            if(!user_authenticated){
                head_app.ModalLogin = true;
            }
            else{
                add_to_cart(prod_id);
            }
        }
    }
});


for(var i=0; i<menu_data.length;i++ ){
    if(menu_data[i]> 0){
            $("#shopmenu").find("input[type=checkbox][value="+menu_data[i]+"]").prop('checked', true);
    }
}
