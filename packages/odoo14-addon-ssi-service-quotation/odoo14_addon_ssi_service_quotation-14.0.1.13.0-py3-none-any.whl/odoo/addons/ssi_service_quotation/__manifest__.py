# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Service Quotation",
    "version": "14.0.1.13.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_master_data_mixin",
        "ssi_transaction_open_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_win_lost_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_duration_mixin",
        "ssi_partner_mixin",
        "ssi_source_document_mixin",
        "ssi_transaction_pricelist_mixin",
        "ssi_product_line_account_mixin",
        "ssi_service",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "security/ir_rule_data.xml",
        "data/ir_sequence_data.xml",
        "data/sequence_template_data.xml",
        "data/approval_template_data.xml",
        "data/policy_template_data.xml",
        "wizards/copy_quotation_term_views.xml",
        "views/service_quotation_views.xml",
        "views/service_contract_views.xml",
    ],
    "demo": [],
}
