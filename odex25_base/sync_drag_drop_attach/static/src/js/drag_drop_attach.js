odoo.define('sync_drag_drop_attach.drag_drop_attach', function (require) {
    "use strict";

    var core = require('web.core');
    var framework = require('web.framework');
    var FormController = require('web.FormController');

    FormController.include({
        _updateButtons: function () {
            var self = this;
            var timeout = null;
            this._super.apply(this, arguments);
            if (this.mode === "readonly") {
                self.$el.find('.o_form_view').on('dragover dragenter', function (e) {
                    clearTimeout(timeout);
                    e.preventDefault();
                    e.stopPropagation();
                    self.$el.find('.o_form_view').closest('.o_content').addClass('o_drop_mode');
                    self.$el.find('.o_form_view').addClass('adjust_sheet');
                }).on('dragleave  drop', function (e) {
                    timeout = setTimeout(function(){
                        e.stopPropagation();
                        self.toggle_effect(e)
                    }, 50);
                }).off('drop').on('drop', function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                    self.toggle_effect(e);
                    if (e.originalEvent.dataTransfer &&
                        e.originalEvent.dataTransfer.files.length) {
                        framework.blockUI();
                        self.upload_files(e.originalEvent.dataTransfer.files);
                    }
                });
            } else {
                self.$el.find('.o_form_view').off('dragover').off('dragleave').off('drop');
            }
        },
        toggle_effect: function (e) {
            var self = this;
            e.preventDefault();
            e.stopPropagation();
            self.$el.find('.o_form_view').removeClass('adjust_sheet');
            self.$el.find('.o_form_view').closest('.o_content').removeClass('o_drop_mode');
        },
        upload_files: function (files) {
            var self = this;
            var record = this.model.get(this.handle, {raw: true});
            var flag = 1;
            _.each(files, function (file) {
                var querydata = new FormData();
                querydata.append('callback', 'oe_fileupload_temp2');
                querydata.append('model', self.modelName);
                querydata.append('id', record.res_id);
                querydata.append('ufile', file);
                querydata.append('multi', 'true');
                querydata.append('csrf_token', core.csrf_token);
                $.ajax({
                    url: '/web/binary/upload_attachment',
                    type: 'POST',
                    data: querydata,
                    cache: false,
                    processData: false,
                    contentType: false,
                    success: function () {
                        self.saveRecord();
                        if (files.length === flag) framework.unblockUI();
                        flag += 1;
                    }
                });
            });
        }
    })
});

$(document).ready(function () {
    $('body').on('dragstart', function () {
        return false;
    });
});