odoo.define('odex25_purchase_saip.web.radio.required', function(require){
    var relational_fields = require('web.relational_fields');
  
    relational_fields.FieldRadio.include({
        isSet: function () {
            return (this.mode === 'edit')? ($(this.$el).find("[checked='true']")).length > 0: this.value;
        },
    });
  });