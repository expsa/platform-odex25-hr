odoo.define('report_e_invoice.receipt', function(require){
    "use strict";
    var models = require('point_of_sale.models');
    var _super_ordermodel = models.Order.prototype;

    models.Order = models.Order.extend({
        export_for_printing: function(){
            var receipt = _super_ordermodel.export_for_printing.apply(this, arguments);
            receipt.company.street = this.pos.company.street;
            receipt.company.city = this.pos.company.city;
            receipt.company.zip = this.pos.company.zip;
            return receipt;
        },
    });
});