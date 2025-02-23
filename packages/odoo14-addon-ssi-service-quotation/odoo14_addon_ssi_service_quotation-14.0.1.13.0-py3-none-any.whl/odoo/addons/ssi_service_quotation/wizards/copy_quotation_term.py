# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CopyQuotationTerm(models.TransientModel):
    _name = "copy_quotation_term"
    _description = "Copy Quotation Term"

    name = fields.Char(
        string="Term",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    term_id = fields.Many2one(
        string="Payment Term",
        comodel_name="service.quotation_fix_item_payment_term",
        required=False,
        default=lambda self: self._default_term_id(),
    )
    set_qty = fields.Boolean(
        string="Set Qty All Items",
        default=False,
    )
    quantity = fields.Float(
        string="Quanity",
        default=0.0,
    )

    @api.model
    def _default_term_id(self):
        return self.env.context.get("active_id", False)

    def action_confirm(self):
        self.ensure_one()
        new_term = self.term_id.copy(
            {
                "name": self.name,
                "sequence": self.sequence,
            }
        )
        new_term.detail_ids.write(
            {
                "uom_quantity": self.quantity,
            }
        )
