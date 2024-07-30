
odoo.define("pos_orders_history_return.models", function (require) {
    "use strict";

    let models = require("pos_orders_history.models");

    models.PosModel = models.PosModel.extend({
        get_returned_orders_by_pos_reference: function (reference) {
            let all_orders = this.db.pos_orders_history;
            return all_orders.filter(function (order) {
                return order.returned_order && order.pos_reference === reference;
            });
        },
    });

    let _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        add_product: function (product, options) {
            options = options || {};
            if (this.get_mode() === "return") {
                let current_return_qty = this.get_current_product_return_qty(product);
                let quantity = 1;
                if (typeof options.quantity !== "undefined") {
                    quantity = options.quantity;
                }
                if (current_return_qty + quantity <= product.max_return_qty) {
                    _super_order.add_product.apply(this, arguments);
                    this.change_return_product_limit(product);
                }
            } else {
                _super_order.add_product.apply(this, arguments);
            }
        },
        get_current_product_return_qty: function (product) {
            let orderlines = this.get_orderlines();
            let product_orderlines = orderlines.filter(function (line) {
                return line.product.id === product.id;
            });
            let qty = 0;
            product_orderlines.forEach(function (line) {
                qty += line.quantity;
            });
            if (qty < 0) {
                qty = -qty;
            }
            return qty;
        },
        change_return_product_limit: function (product) {
            if (this.get_mode() === "return_without_receipt") {
                return;
            }
            let el = $('span[data-product-id="' + product.id + '"] .max-return-qty');
            let qty = this.get_current_product_return_qty(product);
            el.html(product.max_return_qty - qty);
        },
        export_as_JSON: function () {
            let data = _super_order.export_as_JSON.apply(this, arguments);
            data.return_lines = this.return_lines;
            return data;
        },
        init_from_JSON: function (json) {
            this.return_lines = json.return_lines;
            _super_order.init_from_JSON.call(this, json);
        },
    });

    let _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        initialize: function (attr, options) {
            _super_orderline.initialize.apply(this, arguments);
            let order = this.pos.get_order();
            if (order && order.get_mode() === "return" && this.product.old_price && this.product.price !== this.product.old_price) {
                this.set_unit_price(this.product.old_price);
            }
        },
        set_quantity: function (quantity) {
            let order = this.pos.get_order();
            if (order && order.get_mode() === "return_without_receipt" && quantity !== "remove" && quantity > 0) {
                quantity = -quantity;
                _super_orderline.set_quantity.call(this, quantity);
            } else if (order && order.get_mode() === "return" && quantity !== "remove") {
                let current_return_qty = this.order.get_current_product_return_qty(this.product);
                if (this.quantity) {
                    current_return_qty += this.quantity;
                }
                if (quantity && current_return_qty + Number(quantity) <= this.product.max_return_qty) {
                    if (quantity > 0) {
                        quantity = -quantity;
                    }
                    _super_orderline.set_quantity.call(this, quantity);
                    order.change_return_product_limit(this.product);
                } else if (quantity === "") {
                    _super_orderline.set_quantity.call(this, quantity);
                    order.change_return_product_limit(this.product);
                }
            } else {
                _super_orderline.set_quantity.call(this, quantity);
            }
        },
    });
});
