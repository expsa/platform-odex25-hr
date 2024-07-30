odoo.define("pos_multi_barcode_uom.DB", function (require) {
    "use strict";

    const PosDB = require("point_of_sale.DB");
    const models = require("point_of_sale.models");

    PosDB.include({
        init: function (options) {
            this.product_barcode_uom = [];
            this._super(options);
        },
        add_products: function (products) {
            this._super(products);
            const self = this;
            products.forEach(function (product) {
                if (product.multi_uom_ids) {
                    const barcode_uom_opts = self.product_barcode_uom || [];
                    barcode_uom_opts.forEach(function (option) {
                        if (product.multi_uom_ids.includes(option.id)) {
                            let productWithBarcodeUOM = new models.Product({}, product);
                            productWithBarcodeUOM.uom_id = option.multi_uom_id;
                            productWithBarcodeUOM.lst_price = option.price;
                            self.product_by_barcode[option.barcode] = productWithBarcodeUOM;
                        }
                    });
                }
            });
        },
        add_barcode_uom: function (barcode) {
            this.product_barcode_uom = barcode;
        },
    });
});
