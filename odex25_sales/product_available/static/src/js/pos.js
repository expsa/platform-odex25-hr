odoo.define("product_available.PosModel", function (require) {
    "use strict";

    const rpc = require("web.rpc");
    const models = require("point_of_sale.models");
    const utils = require("web.utils");
    const round_pr = utils.round_precision;
    const core = require("web.core");
    const { Gui } = require("point_of_sale.Gui");
    const field_utils = require("web.field_utils");
    const _t = core._t;
    const contexts = require('point_of_sale.PosContext');

    let PosModelSuper = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        load_server_data: function () {
            let self = this;
            let loaded = PosModelSuper.load_server_data.call(this);
            let prod_model = _.find(this.models, function (model) {
                return model.model === "product.product";
            });
            if (prod_model) {
                prod_model.fields.push("qty_available", "type");
                let context_super = prod_model.context;
                prod_model.context = function (that) {
                    let ret = context_super(that);
                    ret.location = that.config.stock_location_id[0];
                    return ret;
                };
                let loaded_super = prod_model.loaded;
                prod_model.loaded = function (that, products) {
                    loaded_super(that, products);
                    self.db.product_qtys = products;
                };
                return loaded;
            }

            return loaded.then(function () {
                return rpc
                    .query({
                        model: "product.product",
                        method: "search_read",
                        args: [],
                        fields: ["qty_available", "type"],
                        domain: [
                            ["sale_ok", "=", true],
                            ["available_in_pos", "=", true],
                        ],
                        context: { location: self.config.stock_location_id[0] },
                    })
                    .then(function (products) {
                        self.db.product_qtys = products;
                    });
            });
        },
        update_product_qty_from_order_lines: function (order) {
            let self = this;
            order.orderlines.each(function (line) {
                let product = line.get_product();
                product.qty_available -= order.computeProductUomQuantity(product);
            });
            // compatibility with pos_multi_session
            order.trigger("new_updates_to_send");
        },
        after_load_server_data: function () {
            let self = this;
            let res = PosModelSuper.after_load_server_data.apply(this, arguments);
            _.each(this.db.product_qtys, function (v) {
                _.extend(self.db.get_product_by_id(v.id), v);
            });
            return res;
        },
        push_single_order: function (order, opts) {
            let pushed = PosModelSuper.push_single_order.apply(this, arguments);
            if (order) {
                this.update_product_qty_from_order_lines(order);
            }
            return pushed;
        },
        push_and_invoice_order: function (order) {
            let invoiced = PosModelSuper.push_and_invoice_order.call(this, order);

            if (order && order.get_client() && order.orderlines) {
                this.update_product_qty_from_order_lines(order);
            }

            return invoiced;
        },
    });

    let _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({
        computeUomQuantity: function (originUnit, targetUnit, qty) {
            if (originUnit && targetUnit) {
                if (originUnit.id === targetUnit.id) {
                    return qty;
                } else {
                    let amount = qty / originUnit.factor;
                    if (targetUnit) amount = amount * targetUnit.factor;
                    amount = round_pr(amount, targetUnit.rounding);
                    return amount;
                }
            }
            return 0;
        },
        computeProductUomQuantity: function (product) {
            let unitQtyMapping = {};
            const originalProduct = this.pos.db.get_product_by_id(product.id);
            const targetUnit = originalProduct.get_unit();
            this.get_orderlines().forEach((l) => {
                if (l.get_product().id === product.id) {
                    if (l.get_unit().id in unitQtyMapping) {
                        unitQtyMapping[l.get_unit().id] += l.get_quantity();
                    } else {
                        unitQtyMapping[l.get_unit().id] = l.get_quantity();
                    }
                }
            });
            let takenQty = 0;
            for (const [unitId, qty] of Object.entries(unitQtyMapping)) {
                let unitObj = this.pos.units_by_id[unitId];
                takenQty += this.computeUomQuantity(unitObj, targetUnit, qty);
            }
            return takenQty;
        },
        // Overriding only to edit if (options.draftPackLotLines) line to add into account that a line may not exist
        add_product: function(product, options){
            if(this._printed){
                this.destroy();
                return this.pos.get_order().add_product(product, options);
            }
            this.assert_editable();
            options = options || {};
            var line = new models.Orderline({}, {pos: this.pos, order: this, product: product});
            this.fix_tax_included_price(line);
    
            if(options.quantity !== undefined){
                line.set_quantity(options.quantity);
            }
    
            if (options.price_extra !== undefined){
                line.price_extra = options.price_extra;
                line.set_unit_price(line.product.get_price(this.pricelist, line.get_quantity(), options.price_extra));
                this.fix_tax_included_price(line);
            }
    
            if(options.price !== undefined){
                line.set_unit_price(options.price);
                this.fix_tax_included_price(line);
            }
    
            if(options.lst_price !== undefined){
                line.set_lst_price(options.lst_price);
            }
    
            if(options.discount !== undefined){
                line.set_discount(options.discount);
            }
    
            if (options.description !== undefined){
                line.description += options.description;
            }
    
            if(options.extras !== undefined){
                for (var prop in options.extras) {
                    line[prop] = options.extras[prop];
                }
            }
            if (options.is_tip) {
                this.is_tipped = true;
                this.tip_amount = options.price;
            }
    
            var to_merge_orderline;
            for (var i = 0; i < this.orderlines.length; i++) {
                if(this.orderlines.at(i).can_be_merged_with(line) && options.merge !== false){
                    to_merge_orderline = this.orderlines.at(i);
                }
            }
            if (to_merge_orderline){
                to_merge_orderline.merge(line);
                this.select_orderline(to_merge_orderline);
            } else {
                let reserve = line.product.qty_available - (line.quantity || 1);
                if (
                    !line.pos.config.allow_out_of_stock &&
                    line.product.type === "product" &&
                    reserve < line.pos.config.min_reserve_qty
                ) {
                    Gui.showPopup("ConfirmPopup", {
                        title: _t("Warning: You cannot add this product to the order"),
                        body: _t(
                            `You have exceeded the quantity minimum reserve quantity.There are only ${line.pos.config.min_reserve_qty} units left in stock.\nPlease Check Your stock and try again`
                        ),
                    });
                } else {
                    this.orderlines.add(line);
                    this.select_orderline(this.get_last_orderline());
                    this.trigger("update-product-available-qty", { product: line.product });

                }
            }
    
            if (options.draftPackLotLines && this.selected_orderline) { // fix not checking if a line exist bug
                this.selected_orderline.setPackLotLines(options.draftPackLotLines);
            }
            if (this.pos.config.iface_customer_facing_display) {
                this.pos.send_current_order_to_customer_facing_display();
            }
        },
    });

    let _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        set_quantity: function (quantity, keep_price) {
            let self = this;
            let quant = typeof quantity === "number" ? quantity : quantity !== "remove" ? field_utils.parse.float("" + quantity) || 0 : 0;
            if (
                _.isEmpty(contexts.orderManagement.mapping) && // make sure that we aren't in the order management screen
                quantity !== "remove" &&
                !this.pos.config.allow_out_of_stock &&
                this.product.type === "product" &&
                this.product.qty_available - quant < this.pos.config.min_reserve_qty
            ) {
                Gui.showPopup("ConfirmPopup", {
                    title: _t("Warning: You cannot add this product to the order"),
                    body: _t(
                        `You have exceeded the quantity minimum reserve quantity.There are only ${self.pos.config.min_reserve_qty} units left in stock.\nPlease Check Your stock and try again`
                    ),
                });
            } else {
                _super_orderline.set_quantity.apply(this, arguments);
                this.trigger("update-product-available-qty", { product: this.product });
            }
        },
    });
});
