odoo.define("pos_multi_barcode_uom.models", function (require) {
    "use strict";

    let models = require("point_of_sale.models");

    models.load_fields("product.product", ["multi_uom_ids"]);

    models.load_models(
        [
            {
                model: "product.multi.uom",
                condition: function (self) {
                    return self.config.allow_multi_uom;
                },
                fields: ["multi_uom_id", "price", "barcode"],
                loaded: function (self, result) {
                    if (result.length) {
                        self.product_multi_uom_list = result;
                        self.db.add_barcode_uom(result);
                    } else {
                        self.product_multi_uom_list = [];
                    }
                },
            },
        ],
        { after: "pos.category" }
    );

    models.PosModel = models.PosModel.extend({
        scan_product: function (parsed_code) {
            let selectedOrder = this.get_order();
            let product = this.db.get_product_by_barcode(parsed_code.base_code);

            if (!product) {
                return false;
            }

            if (parsed_code.type === "price") {
                selectedOrder.add_product(product, { price: parsed_code.value });
            } else if (parsed_code.type === "weight") {
                selectedOrder.add_product(product, { quantity: parsed_code.value, merge: false });
            } else if (parsed_code.type === "discount") {
                selectedOrder.add_product(product, { discount: parsed_code.value, merge: false });
            } else {
                let temp = true;
                let pos_multi_op = this.product_multi_uom_list;
                for (let i = 0; i < pos_multi_op.length; i++) {
                    if (pos_multi_op[i].barcode == parsed_code.code) {
                        temp = false;
                    }
                }
                if (temp) {
                    selectedOrder.add_product(product);
                } else {
                    selectedOrder.add_product(product, { merge: false });
                }
            }
            let line = selectedOrder.get_last_orderline();
            let pos_multi_op = this.product_multi_uom_list;
            for (let i = 0; i < pos_multi_op.length; i++) {
                if (pos_multi_op[i].barcode == parsed_code.code) {
                    line.set_quantity(1);
                    line.set_unit_price(pos_multi_op[i].price);
                    line.set_product_uom(pos_multi_op[i].multi_uom_id[0]);
                    line.price_manually_set = true;
                }
            }
            return true;
        },
    });

    let _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        initialize: function (attr, options) {
            this.emproduct_uom = "";
            _super_orderline.initialize.call(this, attr, options);
        },
        set_product_uom: function (uom_id) {
            this.emproduct_uom = this.pos.units_by_id[uom_id];
            this.trigger("change", this);
        },

        get_unit: function () {
            let unit_id = this.product.uom_id;
            if (!unit_id) {
                return undefined;
            }
            unit_id = unit_id[0];
            if (!this.pos) {
                return undefined;
            }
            return this.emproduct_uom ? this.emproduct_uom : this.pos.units_by_id[unit_id];
        },

        export_as_JSON: function () {
            let unit_id = this.product.uom_id;
            let json = _super_orderline.export_as_JSON.call(this);
            json.product_uom_id = this.emproduct_uom == "" || !this.emproduct_uom ? unit_id[0] : this.emproduct_uom.id;
            return json;
        },

        init_from_JSON: function (json) {
            _super_orderline.init_from_JSON.apply(this, arguments);
            this.emproduct_uom = this.pos.units_by_id[json.product_uom_id];
        },
    });

    models.Order = models.Order.extend({
        find_reference_unit_price: function (product, product_uom) {
            if (product_uom.uom_type == "reference") {
                return product.list_price;
            } else if (product_uom.uom_type == "smaller") {
                return product.list_price * product_uom.factor;
            } else if (product_uom.uom_type == "bigger") {
                return product.list_price / product_uom.factor_inv;
            }
        },
        get_latest_price: function (uom, product) {
            let uom_by_category = this.get_units_by_category(this.pos.units_by_id, uom.category_id);
            let product_uom = this.pos.units_by_id[product.uom_id[0]];
            let ref_price = this.find_reference_unit_price(product, product_uom);
            let ref_unit = null;
            for (let i in uom_by_category) {
                if (uom_by_category[i].uom_type == "reference") {
                    ref_unit = uom_by_category[i];
                    break;
                }
            }
            if (ref_unit) {
                if (uom.uom_type == "bigger") {
                    return ref_price * uom.factor_inv;
                } else if (uom.uom_type == "smaller") {
                    return ref_price / uom.factor;
                } else if (uom.uom_type == "reference") {
                    return ref_price;
                }
            }
            return product.price;
        },
        get_units_by_category: function (uom_list, categ_id) {
            let uom_by_categ = [];
            for (let uom in uom_list) {
                if (uom_list[uom].category_id[0] == categ_id[0] && uom_list[uom].active) {
                    uom_by_categ.push(uom_list[uom]);
                }
            }
            return uom_by_categ;
        },
    });
});