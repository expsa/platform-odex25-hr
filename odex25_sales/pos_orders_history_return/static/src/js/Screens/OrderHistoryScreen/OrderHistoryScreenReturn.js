odoo.define("pos_orders_history_return.OrdersHistoryScreen", function (require) {
    "use strict";

    const OrdersHistoryScreen = require("pos_orders_history.OrdersHistoryScreen");
    const core = require("web.core");
    const _t = core._t;
    const Registries = require("point_of_sale.Registries");
    const models = require("point_of_sale.models");


    const OrdersHistoryScreenReturn = (OrdersHistoryScreen) =>
        class extends OrdersHistoryScreen {
        mounted() {
            if (this.env.pos.config.return_orders) {
                $(".actions.oe_hidden").removeClass("oe_hidden");
            }
        }
        load_order_by_barcode(barcode) {
            if (this.env.pos.config.return_orders) {
                let self = this;
                this.rpc({
                    model: "pos.order",
                    method: "search_read",
                    args: [[["ean13", "=", barcode]]],
                }).then(
                    function (o) {
                        if (o && o.length) {
                            self.env.pos.update_orders_history(o);
                            o.forEach(function (exist_order) {
                                self.env.pos.fetch_order_history_lines_by_order_ids(exist_order.id).done(function (lines) {
                                    self.env.pos.update_orders_history_lines(lines);
                                    if (!exist_order.returned_order) {
                                        self.search_order_on_history(exist_order);
                                    }
                                });
                            });
                        } else {
                            self.showPopup("ErrorPopup", {
                                title: _t("Error: Could not find the Order"),
                                body: _t("There is no order with this barcode."),
                            });
                        }
                    },
                    function (err, event) {
                        event.preventDefault();
                        console.error(err);
                        self.showPopup("ErrorPopup", {
                            title: _t("Error: Could not find the Order"),
                            body: err.data,
                        });
                    }
                );
            } else {
                super.load_order_by_barcode(barcode);
            }
        }
        return_no_receipt() {
            let options = _.extend({ pos: this.env.pos }, {});
            let order = new models.Order({}, options);
            order.temporary = true;
            order.set_mode("return_without_receipt");
            order.return_lines = [];
            this.env.pos.get("orders").add(order);
            this.trigger('close-temp-screen');
            this.env.pos.set_order(order);
        }
        get orders() {
            let orders = super.orders;
            if (!this.env.pos.config.show_returned_orders) {
                orders = orders.filter((order) => order.returned_order !== true);
            }
            return orders;
        }
        click_return_order_by_id(id) {
            let self = this;
            let order = self.env.pos.db.orders_history_by_id[id];
            let uid =
                order.pos_reference && order.pos_reference.match(/\d{1,}-\d{1,}-\d{1,}/g) && order.pos_reference.match(/\d{1,}-\d{1,}-\d{1,}/g)[0];
            let split_sequence_number = uid.split("-");
            let sequence_number = split_sequence_number[split_sequence_number.length - 1];

            let orders = this.env.pos.get("orders").models;
            let exist_order = _.find(orders, function (o) {
                return o.uid === uid && Number(o.sequence_number) === Number(sequence_number);
            });

            if (exist_order) {
                this.showPopup("ErrorPopup", {
                    title: _t("Warning"),
                    body: _t("You have an unfinished return of the order. Please complete the return of the order and try again."),
                });
                return false;
            }

            let lines = [];
            order.lines.forEach((line_id) => {
                lines.push(this.env.pos.db.line_by_id[line_id]);
            });

            let products = [];
            let current_products_qty_sum = 0;
            lines.forEach(function (line) {
                let product = self.env.pos.db.get_product_by_id(line.product_id[0]);
                if (line.price_unit !== product.price) {
                    product.old_price = line.price_unit;
                }else {
                    product.old_price = product.price;
                }
                current_products_qty_sum += line.qty;
                products.push(product);
            });

            let returned_orders = this.env.pos.get_returned_orders_by_pos_reference(order.pos_reference);
            let exist_products_qty_sum = 0;
            returned_orders.forEach(function (o) {
                o.lines.forEach(function (line_id) {
                    let line = self.env.pos.db.line_by_id[line_id];
                    exist_products_qty_sum += line.qty;
                });
            });

            if (exist_products_qty_sum + current_products_qty_sum <= 0) {
                this.showPopup("ErrorPopup", {
                    title: _t("Error"),
                    body: _t("All products have been returned."),
                });
                return false;
            }

            let partner_id = order.partner_id || false;

            if (products.length > 0) {
                // Create new order for return
                let json = _.extend({}, order);
                json.uid = uid;
                json.sequence_number = Number(sequence_number);
                json.lines = [];
                json.statement_ids = [];
                json.mode = "return";
                json.return_lines = lines;
                json.pricelist_id = this.env.pos.default_pricelist.id;
                let options = _.extend({ pos: this.env.pos }, { json: json });
                order = new models.Order({}, options);
                order.temporary = true;
                let client = null;
                if (partner_id) {
                    client = this.env.pos.db.get_partner_by_id(partner_id[0]);
                    if (!client) {
                        console.error("ERROR: trying to load a partner not available in the pos");
                    }
                }
                order.set_client(client);
                this.env.pos.get("orders").add(order);
                this.showScreen('ProductScreen');
                this.env.pos.set_order(order);
            } else {
                this.showPopup("ErrorPopup", _t("Order Is Empty"));
            }
        }
    }

    Registries.Component.extend(OrdersHistoryScreen, OrdersHistoryScreenReturn);
    return OrdersHistoryScreenReturn;
});
