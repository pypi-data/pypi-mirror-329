# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ServiceQuotationFixItemPaymentTermDetail(models.Model):
    _name = "service.quotation_fix_item_payment_term_detail"
    _description = "Service Fix Item Payment Term Detail"
    _inherit = [
        "service.fix_item_payment_term_detail_mixin",
    ]

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    term_id = fields.Many2one(
        string="Service Payment Term",
        comodel_name="service.quotation_fix_item_payment_term",
        ondelete="cascade",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        related="term_id.service_id.pricelist_id",
        store=True,
    )

    @api.onchange(
        "currency_id",
    )
    def onchange_pricelist_id(self):
        pass

    def _prepare_contract_data(self):
        self.ensure_one()
        return {
            "name": self.name,
            "product_id": self.product_id.id and self.product_id.id or False,
            "account_id": self.account_id.id,
            "analytic_account_id": self.analytic_account_id
            and self.analytic_account_id.id
            or False,
            "price_unit": self.price_unit,
            "uom_quantity": self.uom_quantity,
            "uom_id": self.uom_id.id,
            "tax_ids": [(6, 0, self.tax_ids.ids)],
            "pricelist_id": self.pricelist_id.id,
            "currency_id": self.currency_id.id,
        }
