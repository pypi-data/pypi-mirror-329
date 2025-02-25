# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ServiceMixin(models.AbstractModel):
    _name = "service.mixin"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.date_duration",
        "mixin.partner",
        "mixin.source_document",
        "mixin.transaction_pricelist",
        "mixin.transaction_salesperson",
    ]
    _description = "Mixin Class for Service"
    _approval_from_state = "confirm"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"
    _create_sequence_state = "open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_open_policy_fields = False
    _automatically_insert_open_button = False

    _statusbar_visible_label = "draft,confirm,open,done"

    _policy_field_order = [
        "confirm_ok",
        "open_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]

    _header_button_order = [
        "action_confirm",
        "action_open",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_open",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    title = fields.Char(
        string="Title",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        domain=[
            ("parent_id", "=", False),
        ],
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    contact_partner_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_contact_contractor_ids = fields.Many2many(
        string="Allowed Contractor's Contact",
        comodel_name="res.partner",
        compute="_compute_allowed_contact_contractor_ids",
        store=False,
    )
    contractor_id = fields.Many2one(
        string="Contractor",
        comodel_name="res.partner",
        domain=[
            ("parent_id", "=", False),
        ],
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    contact_contractor_id = fields.Many2one(
        string="Contact's Contact",
        comodel_name="res.partner",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="service.type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    fix_item_allowed_product_ids = fields.Many2many(
        string="Fix Item Allowed Products",
        comodel_name="product.product",
        related="type_id.fix_item_allowed_product_ids",
    )
    fix_item_allowed_product_categ_ids = fields.Many2many(
        string="Fix Item Allowed Product Categories",
        comodel_name="product.category",
        related="type_id.fix_item_allowed_product_categ_ids",
    )
    manager_id = fields.Many2one(
        string="Manager",
        comodel_name="res.users",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    fix_item_ids = fields.One2many(
        string="Fixed Items",
        comodel_name="service.fix_item_mixin",
        inverse_name="service_id",
        readonly=True,
        copy=False,
    )
    fix_item_payment_term_ids = fields.One2many(
        string="Fix Item Payment Terms",
        comodel_name="service.fix_item_payment_term_mixin",
        inverse_name="service_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        copy=True,
    )
    amount_untaxed = fields.Monetary(
        string="Untaxed",
        compute="_compute_amount",
        store=True,
        currency_field="currency_id",
    )
    amount_tax = fields.Monetary(
        string="Tax",
        compute="_compute_amount",
        store=True,
        currency_field="currency_id",
    )
    amount_total = fields.Monetary(
        string="Total",
        compute="_compute_amount",
        store=True,
        currency_field="currency_id",
    )
    allowed_pricelist_ids = fields.Many2many(
        string="Allowed Pricelists",
        comodel_name="product.pricelist",
        compute="_compute_allowed_pricelist_ids",
        store=False,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("terminate", "Terminated"),
            ("reject", "Rejected"),
        ],
        default="draft",
        copy=False,
    )

    @api.depends(
        "contractor_id",
    )
    def _compute_allowed_contact_contractor_ids(self):
        Partner = self.env["res.partner"]
        for record in self:
            result = []
            if record.contractor_id:
                criteria = [
                    ("commercial_partner_id", "=", record.contractor_id.id),
                    ("id", "!=", record.contractor_id.id),
                    ("type", "=", "contact"),
                ]
                result = Partner.search(criteria).ids
            record.allowed_contact_contractor_ids = result

    @api.onchange("contractor_id")
    def onchange_contact_contractor_id(self):
        self.contact_contractor_id = False

    @api.depends("policy_template_id")
    def _compute_policy(self):
        _super = super(ServiceMixin, self)
        _super._compute_policy()

    @api.model
    def _get_policy_field(self):
        res = super(ServiceMixin, self)._get_policy_field()
        policy_field = [
            "open_ok",
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.model
    def _get_under_approval_exceptions(self):
        _super = super(ServiceMixin, self)
        result = _super._get_under_approval_exceptions()
        result.append("name")
        return result

    @api.depends(
        "currency_id",
        "type_id",
    )
    def _compute_allowed_pricelist_ids(self):
        Pricelist = self.env["product.pricelist"]
        for record in self:
            result = False
            if record.currency_id and record.type_id:
                criteria = [
                    ("currency_id", "=", record.currency_id.id),
                ]
                if record.type_id.allowed_pricelist_ids:
                    criteria += [("id", "in", record.type_id.allowed_pricelist_ids.ids)]
                result = Pricelist.search(criteria).ids
            record.allowed_pricelist_ids = result

    @api.depends(
        "fix_item_payment_term_ids",
        "fix_item_payment_term_ids.amount_untaxed",
        "fix_item_payment_term_ids.amount_tax",
        "fix_item_payment_term_ids.amount_total",
    )
    def _compute_amount(self):
        for record in self:
            amount_untaxed = amount_tax = amount_total = 0.0
            for term in record.fix_item_payment_term_ids:
                amount_untaxed += term.amount_untaxed
                amount_tax += term.amount_tax
                amount_total += term.amount_total
            record.amount_untaxed = amount_untaxed
            record.amount_tax = amount_tax
            record.amount_total = amount_total
