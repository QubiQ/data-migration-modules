from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def recompute_lines(self, move_id=[]):
        if move_id:
            move = self.browse(move_id)
        else:
            move = self.search([])
        move._recompute_dynamic_lines(True, True)
        move._compute_tax_totals_json()

    @api.model
    def mig_reconcile(self, vals):
        ''' input: [{'invoice_id': <search by external_id>, 'move_line_id': <search_by_xmlid>}] '''
        def allow_reconcile_acc(line):
            # Allow reconcile accounts
            for l in line:
                if not l.account_id.reconcile and l.account_id.internal_type != 'liquidity':
                    l.account_id.write({'reconcile': True})

        total = len(vals)
        i = 0
        msg = []
        for v in vals:
            invoices, move_line_id = self.env['account.move'], self.env[
                'account.move.line']
            i += 1
            for inv_id in v.get('invoice_id'):
                xml_id = 'MOVE_.%s' % inv_id
                try:
                    invoices += self.env.ref(xml_id)
                except:
                    e = "not found: %s" % xml_id
                    msg.append(e)
                    continue
            for line_id in v.get('move_line_id'):
                xml_id = 'MOVE_LINE_.%s' % line_id
                try:
                    move_line_id += self.env.ref(xml_id)
                except:
                    e = "not found: %s" % xml_id
                    msg.append(e)
                    continue
            invoice_line = invoices.line_ids.filtered('date_maturity')
            try:
                allow_reconcile_acc(move_line_id + invoice_line)
                (move_line_id + invoice_line).reconcile()
                print("Concilied %i/%i" % (i, total))
            except Exception as e:
                if "han sido conciliado" not in str(e):
                    print(e)
                    msg.append(str(e))
                    msg.append("on MOVE_.%s" % (v.get('invoice_id')))
                print("Concilied %i/%i" % (i, total))
                continue
        return '\n'.join(msg)
