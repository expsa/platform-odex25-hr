odoo.define("product_available.ProductItem", function (require) {
    "use strict";

    const ProductItem = require("point_of_sale.ProductItem");
    const OrderWidget = require("point_of_sale.OrderWidget");
    const Registries = require("point_of_sale.Registries");
    const { useState } = owl.hooks;
    const { useExternalListener } = owl.hooks;

    const ProductItemAvailableQty = (ProductItem) =>
        class extends ProductItem {
            static template = "ProductItemWithQuantity";
            constructor() {
                super(...arguments);
                useExternalListener(document, "update-product-available-qty", this.UpdateAvailableQty);
            }
            setup() {
                this.state = useState({ qty_available: this.props.product.qty_available });
            }

            UpdateAvailableQty(ev) {
                const product = ev.detail.product;
                const order = this.env.pos.get_order();
                if (product && this.props.product.id === product.id) {
                    let takenQty = order.computeProductUomQuantity(product);
                    this.state.qty_available = this.props.product.qty_available - takenQty;
                }
            }
        };

    const OrderWidgetEventHook = (OrderWidget) =>
        class extends OrderWidget {
            _onNewOrder(order) {
                super._onNewOrder(order);
                if (order) {
                    order.orderlines.on(
                        "update-product-available-qty",
                        (detail) => {
                            this.trigger("update-product-available-qty", detail);
                        },
                        this
                    );
                }
            }
            _onPrevOrder(order) {
                super._onPrevOrder(order);
                if (order) {
                    order.orderlines.off("update-product-available-qty", null, this);
                }
            }
        };

    Registries.Component.extend(ProductItem, ProductItemAvailableQty);
    Registries.Component.extend(OrderWidget, OrderWidgetEventHook);
    return { ProductItemAvailableQty };
});
