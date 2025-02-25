# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ServiceFixItemPaymentTermMixin(models.AbstractModel):
    _name = "service.fix_item_payment_term_mixin"
    _description = "Service Fix Item Payment Term Mixin"
    _order = "sequence, id"

    @api.depends(
        "detail_ids",
        "detail_ids.price_subtotal",
        "detail_ids.price_tax",
        "detail_ids.price_total",
    )
    def _compute_total(self):
        for record in self:
            amount_untaxed = amount_tax = amount_total = 0.0
            for detail in record.detail_ids:
                amount_untaxed += detail.price_subtotal
                amount_tax += detail.price_tax
                amount_total += detail.price_total
            record.amount_untaxed = amount_untaxed
            record.amount_tax = amount_tax
            record.amount_total = amount_total

    service_id = fields.Many2one(
        string="Service Object",
        comodel_name="service.mixin",
        ondelete="cascade",
    )
    name = fields.Char(
        string="Term",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    fix_item_allowed_product_ids = fields.Many2many(
        string="Fix Item Allowed Products",
        comodel_name="product.product",
        related="service_id.type_id.fix_item_allowed_product_ids",
    )
    fix_item_allowed_product_categ_ids = fields.Many2many(
        string="Fix Item Allowed Product Categories",
        comodel_name="product.category",
        related="service_id.type_id.fix_item_allowed_product_categ_ids",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="service_id.currency_id",
        store=True,
        required=False,
    )
    detail_ids = fields.One2many(
        string="Detail",
        comodel_name="service.fix_item_payment_term_detail_mixin",
        inverse_name="term_id",
        copy=True,
    )
    amount_untaxed = fields.Monetary(
        string="Untaxed",
        required=False,
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
    )
    amount_tax = fields.Monetary(
        string="Tax",
        required=False,
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
    )
    amount_total = fields.Monetary(
        string="Total",
        required=False,
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
    )
