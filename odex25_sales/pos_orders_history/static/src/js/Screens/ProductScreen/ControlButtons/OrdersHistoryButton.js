odoo.define("pos_orders_history.OrdersHistoryButton", function (require) {
    "use strict";

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    class OrdersHistoryButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        async onClick() {
            const orders = this.env.pos.get_order_list();
            this.showScreen('OrdersHistoryScreen', {orders: orders});
        }
    }
    OrdersHistoryButton.template = 'OrdersHistoryButton';

    ProductScreen.addControlButton({
        component: OrdersHistoryButton,
        condition: function() {
            return this.env.pos.config.orders_history;
        },
    });

    Registries.Component.add(OrdersHistoryButton);

    return OrdersHistoryButton;


});
