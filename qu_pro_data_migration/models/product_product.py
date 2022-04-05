from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def init(self):
        self.env.cr.execute(
            "DROP INDEX IF EXISTS  product_product_combination_unique ;")

    @api.model
    def update_product_atribute(self, line):
        '''line recive a dictionary according with data-migration repository'''
        product = self.env.with_context(active_false=False).ref('PROD_PROD_.%s' % line['id'],
                               raise_if_not_found=False)
        if not product:
            print('PROD_PROD_.%s not found' % line['id'])
            return False
        prod_attr = self.env['product.template.attribute.value']
        for attr in line['attribute_value_ids'].split(','):
            atribute = self.env.ref('PROD_ATTR_VAL_.%s' % attr,
                                    raise_if_not_found=False)
            if not atribute:
                print('PROD_ATTR_VAL_.%s not found' % attr)
                return False
            prod_attr += self.env['product.template.attribute.value'].search([
                ('product_attribute_value_id', '=', atribute.id),
                ('product_tmpl_id', '=', product.product_tmpl_id.id),
            ])

        product.write(
            {'product_template_variant_value_ids': [(6, 0, prod_attr.ids)]})
        return "PROD_PROD_.%s Atribute updated" % line['id']
