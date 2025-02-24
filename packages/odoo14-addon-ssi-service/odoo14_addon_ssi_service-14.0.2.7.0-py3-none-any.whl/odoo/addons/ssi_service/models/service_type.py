# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class ServiceType(models.Model):
    _name = "service.type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Service Type"

    fix_item_allowed_product_ids = fields.Many2many(
        string="Fix Item Allowed Products",
        comodel_name="product.product",
        relation="rel_service_type_2_fix_item_allowed_product",
        column1="type_id",
        column2="product_id",
    )
    fix_item_allowed_product_categ_ids = fields.Many2many(
        string="Fix Item Allowed Product Categories",
        comodel_name="product.category",
        relation="rel_service_type_2_fix_item_allowed_product_categ",
        column1="type_id",
        column2="product_id",
    )
    fix_item_receivable_journal_id = fields.Many2one(
        string="Fix Item Receivable Journal",
        comodel_name="account.journal",
        company_dependent=True,
    )
    fix_item_receivable_account_id = fields.Many2one(
        string="Fix Item Receivable Account",
        comodel_name="account.account",
        company_dependent=True,
    )
    analytic_group_id = fields.Many2one(
        string="Analytic Group",
        comodel_name="account.analytic.group",
    )
    allowed_pricelist_ids = fields.Many2many(
        string="Allowed Pricelist",
        comodel_name="product.pricelist",
        relation="rel_service_type_2_pricelist",
        column1="type_id",
        column2="pricelist_id",
    )
