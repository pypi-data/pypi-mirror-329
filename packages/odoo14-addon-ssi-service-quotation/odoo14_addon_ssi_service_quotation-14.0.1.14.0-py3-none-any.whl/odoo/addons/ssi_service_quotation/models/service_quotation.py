# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ServiceQuotation(models.Model):
    _name = "service.quotation"
    _inherit = [
        "service.mixin",
        "mixin.transaction_win_lost",
    ]
    _description = "Service Quotation"

    _statusbar_visible_label = "draft,confirm,open,win"

    _policy_field_order = [
        "confirm_ok",
        "open_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "win_ok",
        "lost_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]

    _header_button_order = [
        "action_confirm",
        "action_open",
        "action_approve_approval",
        "action_reject_approval",
        "action_win",
        "%(ssi_transaction_win_lost_mixin.base_select_lost_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_open",
        "dom_confirm",
        "dom_reject",
        "dom_win",
        "dom_lost",
        "dom_cancel",
    ]

    fix_item_ids = fields.One2many(
        comodel_name="service.quotation_fix_item",
    )
    fix_item_payment_term_ids = fields.One2many(
        comodel_name="service.quotation_fix_item_payment_term",
    )
    contract_id = fields.Many2one(
        string="# Contract",
        comodel_name="service.contract",
        readonly=True,
        copy=False,
        ondelete="set null",
    )

    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "In Progress"),
            ("win", "Win"),
            ("lost", "Lost"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        default="draft",
        copy=False,
    )

    @api.model
    def _get_policy_field(self):
        res = super(ServiceQuotation, self)._get_policy_field()
        policy_field = [
            "open_ok",
            "confirm_ok",
            "approve_ok",
            "win_ok",
            "lost_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    def action_win(self):
        _super = super(ServiceQuotation, self)

        _super.action_win()

        for record in self.sudo():
            record._create_contract()

    def action_cancel(self, cancel_reason):
        _super = super(ServiceQuotation, self)

        _super.action_cancel(cancel_reason=cancel_reason)

        for record in self.sudo():
            record._cancel_contract()

    def _cancel_contract(self):
        self.ensure_one()

        if not self.contract_id:
            return True

        contract = self.contract_id
        contract.action_cancel(cancel_reason=self.cancel_reason_id)
        self.write(self._prepare_cancel_contract())

    def _prepare_cancel_contract(self):
        self.ensure_one()
        return {
            "contract_id": False,
        }

    def _create_contract(self):
        self.ensure_one()
        obj_contract = self.env["service.contract"]
        data = self._prepare_contract_data()
        temp_record = obj_contract.new(data)
        temp_record = self._compute_contract_onchange(temp_record)
        values = temp_record._convert_to_write(temp_record._cache)
        contract = obj_contract.create(values)
        self.write(
            {
                "contract_id": contract.id,
            }
        )

    def _compute_contract_onchange(self, temp_record):
        temp_record.onchange_fix_item_receivable_journal_id()
        temp_record.onchange_fix_item_receivable_account_id()
        temp_record.onchange_analytic_group_id()
        return temp_record

    def _prepare_contract_data(self):
        self.ensure_one()
        fix_item_payment_term_ids = []
        for payment_term in self.fix_item_payment_term_ids:
            data = payment_term._prepare_contract_data()
            fix_item_payment_term_ids.append((0, 0, data))
        return {
            "title": self.title,
            "partner_id": self.partner_id.id,
            "contact_partner_id": self.contact_partner_id
            and self.contact_partner_id.id
            or False,
            "type_id": self.type_id.id,
            "contractor_id": self.contractor_id and self.contractor_id.id or False,
            "contact_contractor_id": self.contact_contractor_id
            and self.contact_contractor_id.id
            or False,
            "user_id": self.user_id.id,
            "manager_id": self.manager_id.id,
            "company_id": self.company_id.id,
            "pricelist_id": self.pricelist_id.id,
            "currency_id": self.currency_id.id,
            "date": fields.Date.today(),
            "date_start": self.date_start,
            "date_end": self.date_end,
            "quotation_id": self.id,
            "fix_item_payment_term_ids": fix_item_payment_term_ids,
            "salesperson_id": self.salesperson_id.id,
            "sale_team_id": self.sale_team_id and self.sale_team_id.id or False,
        }

    def action_recompute_price(self):
        for rec in self.sudo().filtered(lambda s: s.state == "draft"):
            for term_id in rec.fix_item_payment_term_ids:
                for detail_id in term_id.detail_ids:
                    detail_id.onchange_price_unit()
