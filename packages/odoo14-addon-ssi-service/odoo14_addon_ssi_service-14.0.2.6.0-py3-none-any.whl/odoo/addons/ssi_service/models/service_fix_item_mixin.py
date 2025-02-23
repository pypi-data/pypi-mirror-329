# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ServiceFixItemMixin(models.AbstractModel):
    _name = "service.fix_item_mixin"
    _description = "Service Fix Item Mixin"
    _order = "service_id, sequence, id"
    _auto = False

    service_id = fields.Many2one(
        string="Service Object",
        comodel_name="service.mixin",
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    name = fields.Char(
        string="Description",
        required=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="service_id.currency_id",
        store=False,
    )
    price_unit = fields.Monetary(
        string="Price Unit",
        currency_field="currency_id",
    )
    quantity = fields.Float(
        string="Qty",
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="uom.uom",
    )
    amount_untaxed = fields.Monetary(
        string="Untaxed",
        currency_field="currency_id",
    )
    amount_tax = fields.Monetary(
        string="Tax",
        currency_field="currency_id",
    )
    amount_total = fields.Monetary(
        string="Total",
        currency_field="currency_id",
    )
