odoo.define("multi_commercial_registers.pos", function (require) {
    "use strict";

    let models = require("point_of_sale.models");

    // models.load_fields('res.branch', ['name', 'street', 'zip', 'city', 'logo'])

    models.load_models({
        model: "res.branch",
        fields: [],
        domain: [],
        condition: function (self) {
            return self.config.print_by_branch;
        },
        loaded: function (self, branches) {
            let branch_by_id = {};
            branches.forEach((branch) => branch_by_id[branch.id] = branch);
            self.db.branch_by_id = branch_by_id;
        },
    });

    const _order_super = models.Order.prototype;
    models.Order = models.Order.extend({
        export_for_printing: function(){
            const receipt = _order_super.export_for_printing.apply(this, arguments);
            if(this.pos.config.branch_id && this.pos.config.branch_id.length){
                receipt.branch = this.pos.db.branch_by_id[this.pos.config.branch_id[0]];
            }
            return receipt;
        }
    });
});
