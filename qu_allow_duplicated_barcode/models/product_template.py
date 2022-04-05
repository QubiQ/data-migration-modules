from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.product'

    _sql_constraints = [
        ('barcode_uniq', 'CHECK(1=1)', ""),
    ]
