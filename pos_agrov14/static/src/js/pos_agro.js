
console.log('Point of Sale JavaScript loaded');

odoo.define('pos_agro.custom', function (require) {
    "use strict";

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const pos_model = require('point_of_sale.models');

    // lista de precios
    class PosListPriceButton extends PosComponent {
        async onClick() {
            var self = this;
            var pricelist = this.env.pos.default_pricelist;
            const order = this.env.pos.get_order();
            if (order.selected_orderline) {
                var domainp = [['product_tmpl_id','=',order.selected_orderline.product.id],['pricelist_id','=',pricelist.id]]
                var u_p = order.selected_orderline.get_unit().name
                this.rpc({
                    //model: 'pos.order',
                    model: 'product.pricelist.item',
                    method: 'search_read',
                    args: [domainp, ['min_quantity', 'pricelist_id','fixed_price']],
                    kwargs: { limit: 3 },
                    order: 'min_quantity',
                }).then(function (orders) {
                    if (orders.length > 0) {
                        var price_list = _.map(orders, function (o) {
                            return { 'label': _.str.sprintf("Cantidad minima %s %s  a : %s por %s ",
                            o.min_quantity,
                            u_p,
                            o.fixed_price,
                            u_p,
                            //order.selected_orderline.get_standard_price(),
                            ) };

                        });
                        self.showPopup('SelectionPopup', { title: 'Precios', list:_.sortBy(price_list, ['min_quantity'],['desc']).reverse() });
                    } else {
                        self.showPopup('ErrorPopup', { body: 'No Hay precios disponibles' });
                    }
                });
            } else {
                self.showPopup('ErrorPopup', { body: 'Please select the customer' });
            }
        }
    }
    PosListPriceButton.template = 'PosListPriceButton';
    ProductScreen.addControlButton({
        component: PosListPriceButton,
        condition: function () {
            return true;
        },
    });
    Registries.Component.add(PosListPriceButton);
});