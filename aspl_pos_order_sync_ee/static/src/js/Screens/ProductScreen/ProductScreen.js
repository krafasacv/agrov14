odoo.define('aspl_pos_order_sync_ee.ProductScreen', function (require) {
    'use strict';

    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const { useListener } = require('web.custom_hooks');
    const { useState, useRef } = owl.hooks;
    var rpc = require('web.rpc');
    var core = require('web.core');
    var _t = core._t;

    const ProductScreenInherit = (ProductScreen) =>
        class extends ProductScreen {
            constructor() {
                super(...arguments);
                useListener('close-draft-screen', this.closeScreen);
            }

            closeScreen(){
                this.trigger('show-orders-panel');
            }

            async _onClickPay() {
                if(this.env.pos.user.pos_user_type === "salesman" && this.env.pos.config.enable_order_sync){

                    let currentOrder = this.env.pos.get_order();
                    const order = this.env.pos.get_order();
                    var h = '';
                    if (order.get_orderlines().length > 0){
                        var pricelist = this.env.pos.default_pricelist;
                        var pricelist_items = pricelist.items;
                        var x_price_min = 0.00
                        var c_min = 0.00
                        var q =0.00
                        var i;
                        var a = 0;
                        var order_line = _.find(order.get_orderlines(), function (line) {
						    var price_exist = pricelist_items.filter(function(item) {
						        return item['product_tmpl_id'][0] == line.product.product_tmpl_id});
                            a = price_exist.length - 1;


                            for (i = 0; i < price_exist.length; i++) {
                                console.log(a,i,line.quantity, price_exist[i].min_quantity);
                                if (line.quantity >= price_exist[i].min_quantity){
                                     a = i;
                                     break;
                                }

                            }
						    if (price_exist.length > 0 &&
						    price_exist[a].x_price_min>0 &&
						    line.get_unit_price() < price_exist[a].x_price_min){
							x_price_min = price_exist[a].x_price_min;
							c_min = price_exist[a].min_quantity;
							h = pricelist.id
							q = line.quantity
							return true;
						}
                            if (line.quantity == 0){
							x_price_min = price_exist[a].x_price_min;
							c_min = price_exist[a].min_quantity;
							h = pricelist.id
							q = line.quantity
							return true;
                        }
					})


                        if (order_line != undefined){
                            if(q == 0){
                                await this.showPopup('ErrorPopup', {title: this.env._t('Cantidad igual a Cero'),
                                                                body: this.env._t('La cantidad no puede ser igual a cero en  ' + order_line.get_full_product_name() ),})
                            }
                            else{
                                await this.showPopup('ErrorPopup', {title: this.env._t('El precio del producto es menor que el permitido'),
                                                                body: this.env._t('El precio del producto ' + order_line.get_full_product_name() +
                                                                ' es menor del precio mínimo ' + x_price_min + ' para ' + c_min + 'cantidad' + q ),})
                                
                            }
                        }
                       else{

                    var order_str =  currentOrder.get_is_modified_order() ? " Modify " : " Create Draft ";
                    const { confirmed } = await this.showPopup('CreateDraftOrderPopup', {
                        title: this.env._t('Enviar a CAJA'),
                        body: this.env._t('Desea enviar este pedido a la caja?'),
                    });
                    if (confirmed){
                        this.env.pos.get_order().set_salesman_id(this.env.pos.user.id);
                        this.env.pos.push_orders(this.env.pos.get_order());
                        this.showScreen('ReceiptScreen');
                    }
                     }

                    }

                }else{
                    this.showScreen('PaymentScreen');
                }
            }

            async _setValue(val) {
                var discount_limit = this.env.pos.user.discount_limit;
                var managers = this.env.pos.config.pos_managers_ids;
                if(this.env.pos.config.enable_operation_restrict){
                    if(this.state.numpadMode === 'discount'){
                        if(val > discount_limit){
                            if(_.contains(managers,this.env.pos.user.id)){
                                this.currentOrder.get_selected_orderline().set_discount(val);
                                return;
                            }
                            if(managers.length > 0){
                                const { confirmed,payload: enteredPin } = await this.showPopup('AuthenticationPopup', {
                                    title: this.env._t('Authentication'),
                                });
                                if(confirmed){
                                    const userFiltered = this.env.pos.users.filter(user => managers.includes(user.id));
                                    var result_find = _.find(userFiltered, function (user) {
                                        return user.custom_security_pin === enteredPin || user.barcode === enteredPin;
                                    });
                                    if(result_find){
                                        this.currentOrder.get_selected_orderline().set_discount(val);
                                        return;
                                    }else{
                                        alert(_t('Please Enter correct PIN/Barcode!'));
                                        return;
                                    }
                                }
                            }else{
                                alert(_t('Please Contact Your Manager!'));
                                return;
                            }
                        }
                    }
                }
                super._setValue(val);
            }

            quick_delete(order_id){
                var self = this;
                var order_to_be_remove = self.env.pos.db.get_orders_list_by_id(order_id);
                if (order_to_be_remove) {
                    var params = {
                        model: 'pos.order',
                        method: 'unlink',
                        args: [order_to_be_remove.id],
                    }
                    rpc.query(params, {async: false}).then(function(result){});
                }
                var orders_list = self.env.pos.db.get_orders_list();
                orders_list = _.without(orders_list, _.findWhere(orders_list, { id: order_to_be_remove.id }));
                var orderFiltered = orders_list.filter(order => order.state == "draft");
                self.env.pos.db.add_orders(orders_list);
                self.env.pos.db.add_draft_orders(orderFiltered);
                this.trigger('reload-order-count',{ orders_count:orderFiltered.length});
                self.render();
            }

            quick_pay(order_id){
                var self = this;
                var result = self.env.pos.db.get_orders_list_by_id(order_id);
                if(result && result.lines.length > 0){
                    var selectedOrder = this.env.pos.get_order();
                    selectedOrder.destroy();
                    var selectedOrder = this.env.pos.get_order();
                    if (result.partner_id && result.partner_id[0]) {
                        var partner = self.env.pos.db.get_partner_by_id(result.partner_id[0])
                        if(partner){
                            selectedOrder.set_client(partner);
                        }
                    }
                    selectedOrder.set_pos_reference(result.pos_reference);
                    selectedOrder.set_order_id(order_id);
                    selectedOrder.server_id = result.id;

                    selectedOrder.set_sequence(result.name);
                    if(result.salesman_id && result.salesman_id[0]){
                        selectedOrder.set_salesman_id(result.salesman_id[0]);
                    }
                    var order_lines = self.get_orderlines_from_order(result.lines).then(function(order_lines) {
                        if(order_lines && order_lines.length > 0){
                            _.each(order_lines, function(line){
                                var product = self.env.pos.db.get_product_by_id(Number(line.product_id[0]));
                                selectedOrder.add_product(product, {
                                    quantity: line.qty,
                                    discount: line.discount,
                                    price: line.price_unit,
                                });
                            });
                            self.trigger('show-orders-panel');
                            self.showScreen('PaymentScreen',{'order_id':order_id});
                        }
                    })
                }
            }

            get_orderlines_from_order(line_ids){
                var self = this;
                var orderLines = [];
                return new Promise(function (resolve, reject) {
                    rpc.query({
                        model: 'pos.order.line',
                        method: 'search_read',
                        domain: [['id', 'in', line_ids]],
                    }).then(function (order_lines) {
                        resolve(order_lines);
                    })
                });
            }
        };

    Registries.Component.extend(ProductScreen, ProductScreenInherit);

    return ProductScreen;
});
