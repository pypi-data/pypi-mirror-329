# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ServiceContractFixItemPaymentTermDetail(models.Model):
    _name = "service.contract_fix_item_payment_term_detail"
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
        comodel_name="service.contract_fix_item_payment_term",
        ondelete="cascade",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        related="term_id.service_id.pricelist_id",
        store=True,
    )
    invoice_line_id = fields.Many2one(
        string="Invoice Line",
        comodel_name="account.move.line",
        readonly=True,
        ondelete="restrict",
    )

    @api.onchange(
        "currency_id",
    )
    def onchange_pricelist_id(self):
        pass

    def _prepare_invoice_line(self):
        self.ensure_one()
        payment_term = self.term_id
        contract = payment_term.service_id
        aa = (
            self.analytic_account_id
            and self.analytic_account_id.id
            or contract.analytic_account_id
        )
        return {
            "product_id": self.product_id.id,
            "name": self.name,
            "account_id": self.account_id.id,
            "quantity": self.uom_quantity,
            "product_uom_id": self.uom_id.id,
            "price_unit": self.price_unit,
            "tax_ids": [(6, 0, self.tax_ids.ids)],
            "analytic_account_id": aa and aa.id or False,
        }
