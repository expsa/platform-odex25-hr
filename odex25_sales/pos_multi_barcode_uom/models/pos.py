# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class PosConfig(models.Model):
    _inherit = 'pos.config'

    allow_multi_uom = fields.Boolean('Product multi uom', default=True)


class ProductMultiUom(models.Model):
    _name = 'product.multi.uom'
    _order = "sequence desc"

    multi_uom_id = fields.Many2one('uom.uom', 'Unit of measure')
    price = fields.Float("Sale Price", default=0)
    sequence = fields.Integer("Sequence", default=1)
    barcode = fields.Char("Barcode")
    product_tmp_id = fields.Many2one("product.template", string="Product")
    product_id = fields.Many2one("product.product", string="Product")

    _sql_constraints = [('product_tmp_uom_unique', 'unique(multi_uom_id, product_tmp_id)', 'Uom definition already exist!')]

    # @api.depends('product_tmp_id')
    # def _compute_product_tmp_id(self):
    #     for record in self:
    #         if record.product_tmp_id:
    #             record.product_id = record.product_tmp_id.product_tmp_id.ids[0]

    @api.onchange('multi_uom_id')
    def unit_id_change(self):
        domain = {'multi_uom_id': [('category_id', '=', self.product_tmp_id.uom_id.category_id.id)]}
        return {'domain': domain}

    @api.model
    def create(self, vals):
        if 'barcode' in vals:
            barcodes = self.env['product.product'].sudo().search([('barcode', '=', vals['barcode'])])
            barcodes2 = self.search([('barcode', '=', vals['barcode'])])
            if vals['barcode'] and (barcodes or barcodes2):
                raise UserError(_('A barcode can only be assigned to one product !'))
        return super(ProductMultiUom, self).create(vals)

    def write(self, vals):
        if 'barcode' in vals:
            barcodes = self.env['product.product'].sudo().search([('barcode', '=', vals['barcode'])])
            barcodes2 = self.search([('barcode', '=', vals['barcode'])])
            if vals['barcode'] and (barcodes or barcodes2):
                raise UserError(_('A barcode can only be assigned to one product !'))
        return super(ProductMultiUom, self).write(vals)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    multi_uom_ids = fields.One2many('product.multi.uom', 'product_tmp_id', )

    @api.constrains('default_code')
    def unique_default_code(self):
        for rec in self:
            if rec.default_code:
                if self.env["product.template"].search_count([('default_code', '=', rec.default_code)]) > 1:
                    raise ValidationError("Default Code must be unique !")

    @api.model
    def create(self, vals):
        if 'barcode' in vals:
            barcodes = self.env['product.multi.uom'].search([('barcode', '=', vals['barcode'])])
            if vals['barcode'] and barcodes:
                raise UserError(_('A barcode can only be assigned to one product !'))
        return super(ProductTemplate, self).create(vals)

    def write(self, vals):
        if 'barcode' in vals:
            barcodes = self.env['product.multi.uom'].search([('barcode', '=', vals['barcode'])])
            if vals['barcode'] and barcodes:
                raise UserError(_('A barcode can only be assigned to one product !'))
        return super(ProductTemplate, self).write(vals)


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    product_uom_id = fields.Many2one(related=False)

    def _export_for_ui(self, orderline):
        res = super()._export_for_ui(orderline)
        res.update({'product_uom_id': orderline.product_uom_id.id})
        return res

