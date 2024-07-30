odoo.define("pos_multi_barcode_uom.ProductScreen", function (require) {
    "use strict";

    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");
    const models = require('point_of_sale.models');

    const ProductScreenUomBarcode = (ProductScreen) =>
        class extends ProductScreen {
            async _barcodeProductAction(code) {
                const product = this.env.pos.db.get_product_by_barcode(code.base_code)
                if (!product) {
                    return this._barcodeErrorAction(code);
                }
                const options = await this._getAddProductOptions(product);
                // Do not proceed on adding the product when no options is returned.
                // This is consistent with _clickProduct.
                if (!options) return;
    
                // update the options depending on the type of the scanned code
                if (code.type === 'price') {
                    Object.assign(options, {
                        price: code.value,
                        extras: {
                            price_manually_set: true,
                        },
                    });
                } else if (code.type === 'weight' || code.type === 'quantity') {
                    Object.assign(options, {
                        quantity: code.value,
                        merge: false,
                    });
                } else if (code.type === 'discount') {
                    Object.assign(options, {
                        discount: code.value,
                        merge: false,
                    });
                }
                let customUom = this.env.pos.db.product_barcode_uom.find((elem) => elem.barcode == code.base_code);
                if (customUom) {
                    let productWithBarcodeUOM = new models.Product({}, product);
                    productWithBarcodeUOM.uom_id = customUom.multi_uom_id;
                    productWithBarcodeUOM.lst_price = customUom.price;
                    this.currentOrder.add_product(productWithBarcodeUOM, options);
                } else {
                    this.currentOrder.add_product(product, options);
                }
            }

        };
    Registries.Component.extend(ProductScreen, ProductScreenUomBarcode);
    return ProductScreenUomBarcode;
});
