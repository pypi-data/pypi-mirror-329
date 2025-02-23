# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class ServiceContract(models.Model):
    _name = "service.contract"
    _inherit = [
        "service.mixin",
        "mixin.transaction_terminate",
    ]
    _description = "Service Contract"

    _policy_field_order = [
        "confirm_ok",
        "open_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "terminate_ok",
        "restart_ok",
        "manual_number_ok",
    ]

    _header_button_order = [
        "action_confirm",
        "action_open",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_terminate_mixin.base_select_terminate_reason_action)d",
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
        "dom_terminate",
        "dom_cancel",
    ]

    allowed_partner_bank_ids = fields.Many2many(
        string="Allowed Partner Banks",
        comodel_name="res.partner.bank",
        compute="_compute_allowed_partner_bank_ids",
    )
    partner_bank_id = fields.Many2one(
        string="Recipient Bank",
        comodel_name="res.partner.bank",
        required=False,
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        copy=False,
    )
    analytic_group_id = fields.Many2one(
        string="Analytic Group",
        comodel_name="account.analytic.group",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    fix_item_ids = fields.One2many(
        comodel_name="service.contract_fix_item",
    )
    fix_item_payment_term_ids = fields.One2many(
        comodel_name="service.contract_fix_item_payment_term",
    )

    # Invocing related fields
    fix_item_receivable_journal_id = fields.Many2one(
        string="Fix Item Receivable Journal",
        comodel_name="account.journal",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    fix_item_receivable_account_id = fields.Many2one(
        string="Fix Item Receivable Account",
        comodel_name="account.account",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "company_id",
    )
    def _compute_allowed_partner_bank_ids(self):
        BankAccount = self.env["res.partner.bank"]
        for record in self:
            result = []
            if record.company_id:
                criteria = [("partner_id", "=", record.company_id.partner_id.id)]
                result = BankAccount.search(criteria).ids
            record.allowed_partner_bank_ids = result

    @api.onchange(
        "company_id",
    )
    def onchange_partner_bank_id(self):
        self.partner_bank_id = False

    @api.model
    def _get_policy_field(self):
        res = super(ServiceContract, self)._get_policy_field()
        policy_field = [
            "open_ok",
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "terminate_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.post_open_action()
    def _10_create_analytic_account(self):
        self.ensure_one()
        if self.analytic_account_id:
            self._update_analytic_account()
        else:
            AA = self.env["account.analytic.account"]
            aa = AA.create(self._prepare_analytic_account())
            self.write(
                {
                    "analytic_account_id": aa.id,
                }
            )

    def _update_analytic_account(self):
        self.ensure_one()
        self.analytic_account_id.write(self._prepare_update_analytic_account())

    def _prepare_update_analytic_account(self):
        self.ensure_one()
        group_id = self.analytic_group_id and self.analytic_group_id.id or False
        return {
            "name": self.title,
            "code": self.name,
            "partner_id": self.partner_id.id,
            "group_id": group_id,
            "date_start": self.date_start,
            "date_end": self.date_end,
        }

    def _prepare_analytic_account(self):
        self.ensure_one()
        group_id = self.analytic_group_id and self.analytic_group_id.id or False
        return {
            "name": self.title,
            "code": self.name,
            "partner_id": self.partner_id.id,
            "group_id": group_id,
            "date_start": self.date_start,
            "date_end": self.date_end,
        }

    @api.onchange(
        "type_id",
    )
    def onchange_fix_item_receivable_journal_id(self):
        self.fix_item_receivable_journal_id = False
        if self.type_id:
            self.fix_item_receivable_journal_id = (
                self.type_id.fix_item_receivable_journal_id
            )

    @api.onchange(
        "type_id",
    )
    def onchange_fix_item_receivable_account_id(self):
        self.fix_item_receivable_account_id = False
        if self.type_id:
            self.fix_item_receivable_account_id = (
                self.type_id.fix_item_receivable_account_id
            )

    @api.onchange(
        "type_id",
    )
    def onchange_analytic_group_id(self):
        self.analytic_group_id = False
        if self.type_id:
            self.analytic_group_id = self.type_id.analytic_group_id
