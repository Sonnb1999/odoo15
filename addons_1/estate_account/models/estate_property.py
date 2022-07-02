from odoo import models, fields, api, Command
import datetime

class inherited_user(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        # account.move = ""
        journal = self.env['account.move'].with_context(
            default_move_type='out_invoice')._get_default_journal()
        # move_type = ""

        a = self.env["account.move"].create(
            {
                'name': self.name,
                'move_type': 'out_invoice',
                'ref': 'INV/2018/0057',
                'partner_id': self.partner_id.id,
                'invoice_user_id': False,
                'invoice_date': datetime.datetime.today(),
                'posted_before': True,
                'payment_reference': None,

                'invoice_line_ids': [
                    Command.create(
                        {'name': self.name, 'quantity': 1, 'price_unit': self.selling_price}),
                ],
            }
        )
        print("ok>>>>>>>>>.", a)
        return super().action_sold()
