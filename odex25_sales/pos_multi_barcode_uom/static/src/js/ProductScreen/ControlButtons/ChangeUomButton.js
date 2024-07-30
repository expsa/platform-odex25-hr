odoo.define("pos_multi_barcode_uom.ChangeUomButton", function (require) {
    "use strict";

    const PosComponent = require("point_of_sale.PosComponent");
    const ProductScreen = require("point_of_sale.ProductScreen");
    const { useListener } = require("web.custom_hooks");
    const Registries = require("point_of_sale.Registries");

    class ChangeUomButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener("click", this.onClick);
        }
        async onClick() {
            let line = this.env.pos.get_order().get_selected_orderline();
            if (line) {
                let product = line.get_product();
                let order = this.env.pos.get_order();
                let uom_list = this.env.pos.units_by_id;
                let modifiers_list = [];
                let product_multi_uom_list = this.env.pos.product_multi_uom_list;
                let multi_uom_ids = product.multi_uom_ids;
                for (let i = 0; i < product_multi_uom_list.length; i++) {
                    if (multi_uom_ids.indexOf(product_multi_uom_list[i].id) >= 0) {
                        let uom = Object.entries(uom_list).find(([key, value]) => value.id === product_multi_uom_list[i].multi_uom_id[0]);
                        product_multi_uom_list[i].diff = product_multi_uom_list[i].price - order.get_latest_price(uom[1], product);
                        modifiers_list.push(product_multi_uom_list[i]);
                    }
                }
                let selectionList = [];
                let defaultUomAdded = false;
                modifiers_list.forEach((uomOpt) => {
                    defaultUomAdded = uomOpt.multi_uom_id[0] == product.uom_id[0] || defaultUomAdded;
                    let label = `${this.env.pos.format_currency(uomOpt.price, "Product Price")}/${uomOpt.multi_uom_id[1]}`;
                    if (uomOpt.diff) {
                        label.concat(`\n(Diff: ${this.env.pos.format_currency(uomOpt.diff, "Product Price")})`);
                    }
                    selectionList.push({
                        id: uomOpt.multi_uom_id[0],
                        label: label,
                        isSelected: false,
                        item: uomOpt,
                    });
                });
                if (!defaultUomAdded) {
                    selectionList.push({
                        id: product.uom_id[0],
                        label: `${this.env.pos.format_currency(product.lst_price, "Product Price")}/${product.uom_id[1]}`,
                        isSelected: false,
                        item: { price: product.lst_price, multi_uom_id: product.uom_id, barcode: product.barcode },
                    });
                }

                const { confirmed, payload: selectedCategory } = await this.showPopup("SelectionPopup", {
                    title: this.env._t("Select the UOM"),
                    list: selectionList,
                });
                if (confirmed) {
                    const product = this.env.pos.db.get_product_by_barcode(selectedCategory.barcode);
                    line.set_product_uom(selectedCategory.multi_uom_id[0]);
                    line.set_unit_price(selectedCategory.price);
                    line.price_manually_set = true;
                    this.trigger("update-product-available-qty", { product }); // Used to update the available qty tag on the product item , The listener is in product_available module
                }
            }
        }
    }
    ChangeUomButton.template = "ChangeUomButton";

    ProductScreen.addControlButton({
        component: ChangeUomButton,
        condition: function () {
            return this.env.pos.config.allow_multi_uom;
        },
    });

    Registries.Component.add(ChangeUomButton);

    return ChangeUomButton;
});
