odoo.define("product_negative.pos", function (require) {
    "use strict";

    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");
    let models = require("point_of_sale.models");
    let core = require("web.core");
    let _t = core._t;

    models.load_fields("product.product", ["allow_negative_stock"]);

    const paymentScreenAddValidation = (PaymentScreen) =>
        class extends PaymentScreen {
            async validateOrder(isForceValidate) {
                let self = this;
                let superValidate = super.validateOrder;
                if (!this.env.pos.config.negative_order_manager_permission) {
                    return super.validateOrder(isForceValidate);
                }
                let orderLines = this.currentOrder.get_orderlines();
                let has_negative_product = false;
                for (let i = 0; i < orderLines.length; i++) {
                    let line = orderLines[i];
                    if (
                        line.product.type === "product" &&
                        line.product.qty_available < line.quantity &&
                        line.product.allow_negative_stock === false
                    ) {
                        has_negative_product = true;
                        this.sudo_custom({
                            title: _t("Order has out-of-stock product and must be approved by supervisor"),
                            special_group: this.env.pos.config.negative_order_group_id[0],
                            do_not_change_cashier: true,
                            arguments: { ask_untill_correct: true },
                        }).done(function (user) {
                            self.currentOrder.negative_stock_user_id = user;
                            superValidate(isForceValidate);
                        });
                        break;
                    }
                }
                if (!has_negative_product) {
                    super.validateOrder(isForceValidate);
                }
            }
        };

    let _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        export_as_JSON: function () {
            let json = _super_order.export_as_JSON.apply(this, arguments);
            json.negative_stock_user_id = this.negative_stock_user_id ? this.negative_stock_user_id.id : false;
            return json;
        },
    });

    const ProductScreenAddNegativeWarning = (ProductScreen) =>
        class extends ProductScreen {
            async _clickProduct(event) {
                const product = event.detail;
                if (product.type === "product" && product.qty_available <= 0 && product.allow_negative_stock === false) {
                    await this.showPopup("ErrorPopup", {
                        title: _t("The product is out of stock"),
                        body: _t("You can't add an out of stock product."),
                    });
                } else {
                    super._clickProduct(event);
                }
            }
        };
    Registries.Component.extend(PaymentScreen, paymentScreenAddValidation);
    Registries.Component.extend(ProductScreen, ProductScreenAddNegativeWarning);

    return { PaymentScreen, ProductScreen };
});
