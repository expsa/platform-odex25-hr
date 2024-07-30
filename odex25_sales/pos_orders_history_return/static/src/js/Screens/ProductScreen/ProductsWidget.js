odoo.define("pos_orders_history_return.ProductsWidget", function (require) {
    "use strict";
    const ProductsWidget = require("point_of_sale.ProductsWidget");
    const Registries = require("point_of_sale.Registries");

    const ProductsWidgetAddReturnProducts = (ProductsWidget) =>
        class extends ProductsWidget {
            get productsToDisplay() {
                let self = this;
                let order = this.env.pos.get_order();
                if (order && (order.get_mode() === "return" || order.get_mode() === "return_without_receipt")) {
                    let returned_orders = this.env.pos.get_returned_orders_by_pos_reference(order.name);
                    // Add exist products
                    let products = [];
                    if (returned_orders && returned_orders.length) {
                        returned_orders.forEach(function (o) {
                            o.lines.forEach(function (line_id) {
                                let line = self.env.pos.db.line_by_id[line_id];
                                let product = self.env.pos.db.get_product_by_id(line.product_id[0]);

                                let exist_product = _.find(products, function (r) {
                                    return r.id === product.id;
                                });
                                if (exist_product) {
                                    exist_product.max_return_qty += line.qty;
                                } else {
                                    product.max_return_qty = line.qty;
                                    if (line.price_unit !== product.price) {
                                        product.old_price = line.price_unit;
                                    }else {
                                        product.old_price = product.price;
                                    }
                                    products.push(product);
                                }
                            });
                        });
                    }
                    // Update max qty for current return order
                    order.return_lines.forEach(function (line) {
                        let product = self.env.pos.db.get_product_by_id(line.product_id[0]);
                        let exist_product = _.find(products, function (r) {
                            return r.id === product.id;
                        });
                        if (exist_product) {
                            exist_product.max_return_qty += line.qty;
                        } else {
                            product.max_return_qty = line.qty;
                            if (line.price_unit !== product.price) {
                                product.old_price = line.price_unit;
                            } else {
                                product.old_price = product.price;
                            }
                            products.push(product);
                        }
                    });
                    if (products.length) {
                        return products;
                    }
                }
                return super.productsToDisplay;
            }

            set productsToDisplay(products) {
                this.productsToDisplay = products;
            }
        };

    Registries.Component.extend(ProductsWidget, ProductsWidgetAddReturnProducts);
    return ProductsWidgetAddReturnProducts;
});
