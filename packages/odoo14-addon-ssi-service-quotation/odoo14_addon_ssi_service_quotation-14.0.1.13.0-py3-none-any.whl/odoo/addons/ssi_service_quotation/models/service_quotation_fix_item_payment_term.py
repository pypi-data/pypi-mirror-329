# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ServiceQuotationFixItemPaymentTerm(models.Model):
    _name = "service.quotation_fix_item_payment_term"
    _inherit = ["service.fix_item_payment_term_mixin"]
    _description = "Service Quotation Fix Item Payment Term"

    service_id = fields.Many2one(
        string="Service Quotation",
        comodel_name="service.quotation",
        ondelete="cascade",
    )
    detail_ids = fields.One2many(
        comodel_name="service.quotation_fix_item_payment_term_detail",
    )

    def _prepare_contract_data(self):
        self.ensure_one()
        detail_ids = []
        for detail in self.detail_ids:
            data = detail._prepare_contract_data()
            detail_ids.append((0, 0, data))
        return {
            "name": self.name,
            "sequence": self.sequence,
            "detail_ids": detail_ids,
        }
