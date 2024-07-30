odoo.define("odex25_sale_total_discount.ProductScreen", function (require) {
    "use strict";
    const PosComponent = require("point_of_sale.PosComponent");
    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");

    class OrdersTotalDiscountButton extends PosComponent {
        constructor() {
            super(...arguments);
            this.global_discount_rate = 0;
        }
        async onClick() {
            const { confirmed, payload } = await this.showPopup("NumberPopup", {
                startingValue: 0,
                title: this.env._t("Set Discount Percentage"),
                cheap: true,
            });
            let discount_rate = parseInt(payload, 10);
            if (confirmed) {
                const orderLines = this.env.pos.get_order().get_orderlines();
                const limit = this.env.pos.config.total_discount_limit;
                if (discount_rate > limit) {
                    this.showPopup("ErrorPopup", {
                        title: this.env._t("User Error"),
                        confirmText: 'Ok',
                        cancelText: '',
                        body: `You have exceeded the ${limit}% limit !`,
                    });
                } else {
                    if (discount_rate === this.global_discount_rate) {
                        orderLines.forEach((line) => {
                            let discount = line.get_discount() + discount_rate;
                            line.set_discount(discount);
                        });
                    } else {
                        orderLines.forEach((line) => {
                            let discount = line.get_discount();
                            discount -= this.global_discount_rate;
                            discount += discount_rate;
                            line.set_discount(discount);
                        });
                    }
                    this.global_discount_rate = discount_rate;
                }
            }
        }
    }
    OrdersTotalDiscountButton.template = "TotalDiscountButton";

    ProductScreen.addControlButton({
        component: OrdersTotalDiscountButton,
        condition: function () {
            return this.env.pos.config.total_discount;
        },
    });

    Registries.Component.add(OrdersTotalDiscountButton);

    return OrdersTotalDiscountButton;
});
