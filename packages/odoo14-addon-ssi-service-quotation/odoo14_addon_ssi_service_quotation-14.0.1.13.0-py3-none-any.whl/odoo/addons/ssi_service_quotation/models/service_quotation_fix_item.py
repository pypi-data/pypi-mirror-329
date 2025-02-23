# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class ServiceQuotationFixItem(models.Model):
    _name = "service.quotation_fix_item"
    _auto = False
    _inherit = [
        "service.fix_item_mixin",
    ]
    _description = "Service Quotation Fix Item"

    service_id = fields.Many2one(
        string="# Quotation",
        comodel_name="service.quotation",
    )

    def _select(self):
        select_str = """
        SELECT
            ROW_NUMBER() OVER() AS id,
            c.id AS service_id,
            a.product_id AS product_id,
            a.name AS name,
            a.price_unit AS price_unit,
            a.uom_id AS uom_id,
            MAX(a.sequence) AS sequence,
            SUM(a.quantity) AS quantity,
            SUM(a.price_subtotal) AS amount_untaxed,
            SUM(a.price_tax) AS amount_tax,
            SUM(a.price_total) AS amount_total
        """
        return select_str

    def _from(self):
        from_str = """
        service_quotation_fix_item_payment_term_detail AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN service_quotation_fix_item_payment_term AS b
            ON a.term_id = b.id
        JOIN service_quotation AS c
            ON b.service_id = c.id
        """
        return join_str

    def _group_by(self):
        group_str = """
        GROUP BY    c.id,
                    a.product_id,
                    a.name,
                    a.price_unit,
                    a.uom_id
        """
        return group_str

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        self._cr.execute(
            """CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
            %s
        )"""
            % (
                self._table,
                self._select(),
                self._from(),
                self._join(),
                self._where(),
                self._group_by(),
            )
        )
