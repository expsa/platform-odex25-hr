odoo.define("pos_orders_history_return.ProductItem", function (require) {
    "use strict";

    const ProductItem = require("point_of_sale.ProductItem");
    const Registries = require("point_of_sale.Registries");
    const { useState } = owl.hooks;
    const { useListener } = require("web.custom_hooks");

    const ProductItemOldPrice = (ProductItem) =>
        class extends ProductItem {
            constructor() {
                super(...arguments);
                useListener("click-product", () => this.max_return_qty.value > 0 ? this.max_return_qty.value-- : this.max_return_qty.value = 0);
            }

            setup() {
                super.setup()
                this.max_return_qty = useState({ value: this.props.product.max_return_qty });
            }
            get price() {
                let order = this.env.pos.get_order();
                let formattedUnitPrice = 0.0;
                if (order && (order.get_mode() === "return")) {
                    formattedUnitPrice = this.env.pos.format_currency(this.props.product.old_price, "Product Price");
                } else {
                    formattedUnitPrice = this.env.pos.format_currency(this.props.product.get_display_price(this.pricelist, 1), "Product Price");
                }
                if (this.props.product.to_weight) {
                    return `${formattedUnitPrice}/${this.env.pos.units_by_id[this.props.product.uom_id[0]].name}`;
                } else {
                    return formattedUnitPrice;
                }
            }
        };

    Registries.Component.extend(ProductItem, ProductItemOldPrice);
    return  ProductItemOldPrice ;
});
