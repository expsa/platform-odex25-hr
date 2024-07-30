odoo.define('report_e_invoice.address', function(require){
    'use strict';
    var models = require('point_of_sale.models');
    var _super_company = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function(session, attributes){
            var self = this;
            models.load_fields('res.company', ['street', 'city', 'zip']);
            _super_company.initialize.apply(this, arguments);
        }
    });
});