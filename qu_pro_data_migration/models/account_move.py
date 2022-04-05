from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def mig_reconcile(self, vals):
        ''' input: [{'invoice_id': <search by external_id>, 'move_line_id': <search_by_xmlid>}] '''
        def allow_reconcile_acc(line):
            # Allow reconcile accounts
            for l in line:
                if not l.account_id.reconcile and l.account_id.internal_type != 'liquidity':
                    l.account_id.write({'reconcile': True})
        for v in vals:
            xml_id = 'MOVE_.%s' % v.get('invoice_id')
            invoice, move_line_id = self.env['account.move'], self.env['account.move.line']
            try:
                invoice = self.env.ref(xml_id)
            except:
                print("not found: %s" % xml_id)
                continue
            for line_id in v.get('move_line_id'):
                xml_id = 'MOVE_LINE_.%s' % line_id
                try:
                    move_line_id += self.env.ref(xml_id)
                except:
                    print("not found: %s" % xml_id)
                    continue
            invoice_line = invoice.line_ids.filtered('date_maturity')
            try:
                allow_reconcile_acc(move_line_id + invoice_line)
                (move_line_id + invoice_line).reconcile()
            except Exception as e:
                print(e)
                continue
