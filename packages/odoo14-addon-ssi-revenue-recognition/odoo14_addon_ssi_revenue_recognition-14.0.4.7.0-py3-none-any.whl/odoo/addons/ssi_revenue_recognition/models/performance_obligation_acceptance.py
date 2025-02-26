# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class PerformanceObligationAcceptance(models.Model):
    _name = "performance_obligation_acceptance"
    _inherit = [
        "mixin.date_duration",
        "mixin.partner",
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
    ]
    _description = "Performance Obligation Acceptance"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    # Mixin duration attribute
    _date_start_readonly = True
    _date_end_readonly = True
    _date_start_required = True
    _date_end_required = True
    _date_start_states_list = ["draft"]
    _date_start_states_readonly = ["draft"]
    _date_end_states_list = ["draft"]
    _date_end_states_readonly = ["draft"]

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
    contract_id = fields.Many2one(
        string="# Contract",
        comodel_name="service.contract",
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    performance_obligation_id = fields.Many2one(
        string="# Performance Obligation",
        comodel_name="service_contract.performance_obligation",
        required=True,
        readonly=True,
        ondelete="restrict",
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
    manual_fulfillment_ids = fields.One2many(
        string="Manual Fulfillments",
        comodel_name="performance_obligation_acceptance_manual_fulfillment",
        inverse_name="acceptance_id",
    )
    qty_manual_fulfillment = fields.Float(
        string="Manual Fulfillment Qty",
        compute="_compute_qty_manual_fulfillment",
        store=True,
    )
    qty_fulfilled = fields.Float(
        string="Qty Fulfilled",
        compute="_compute_qty_fulfilled",
        store=True,
    )
    revenue_recognition_id = fields.Many2one(
        string="# Revenue Recognition",
        comodel_name="revenue_recognition",
        readonly=True,
    )
    previous_performance_obligation_acceptance_ids = fields.Many2many(
        string="Performance Obligation Acceptance",
        comodel_name="performance_obligation_acceptance",
        relation="rel_previous_performance_obligation_acceptance",
        column1="poa_id",
        column2="previous_poa_id",
        compute="_compute_previous_performance_obligation_acceptance_ids",
        store=True,
        compute_sudo=True,
    )
    qty_fulfilled_accumulated = fields.Float(
        string="Qty Fulfilled + Accumulated",
        compute="_compute_qty_accumulated",
        store=True,
        compute_sudo=True,
    )
    qty_diff_accumulated = fields.Float(
        string="Qty Diff - Accumulated",
        compute="_compute_qty_accumulated",
        store=True,
        compute_sudo=True,
    )
    qty_accepted = fields.Float(
        string="Qty Accepted",
        compute="_compute_qty_accumulated",
        store=True,
        compute_sudo=True,
    )
    qty_excess = fields.Float(
        string="Excess Qty",
        compute="_compute_qty_accumulated",
        store=True,
        compute_sudo=True,
    )

    @api.depends(
        "date",
        "performance_obligation_id",
        "performance_obligation_id.acceptance_ids",
        "performance_obligation_id.acceptance_ids.state",
        "performance_obligation_id.acceptance_ids.date",
        "performance_obligation_id.acceptance_ids.qty_fulfilled",
    )
    def _compute_previous_performance_obligation_acceptance_ids(self):
        PoA = self.env["performance_obligation_acceptance"]
        for record in self:
            criteria = [
                ("performance_obligation_id", "=", record.performance_obligation_id.id),
                ("state", "=", "done"),
                ("date", "<", record.date),
            ]
            result = PoA.search(criteria)
            record.previous_performance_obligation_acceptance_ids = result

    @api.depends(
        "previous_performance_obligation_acceptance_ids",
        "previous_performance_obligation_acceptance_ids.qty_fulfilled",
    )
    def _compute_qty_accumulated(self):
        for record in self:
            qty_total = record.performance_obligation_id.uom_quantity
            qty_fulfilled = qty_accepted = qty_excess = 0.0
            for poa in record.previous_performance_obligation_acceptance_ids:
                qty_fulfilled += poa.qty_fulfilled
            qty_fulfilled += record.qty_fulfilled
            qty_diff = qty_total - qty_fulfilled
            if qty_diff < 0.0:
                qty_excess = abs(qty_diff)
                qty_accepted = record.qty_fulfilled + qty_diff
            else:
                qty_accepted = record.qty_fulfilled

            record.qty_fulfilled_accumulated = qty_fulfilled
            record.qty_diff_accumulated = qty_diff
            record.qty_accepted = qty_accepted
            record.qty_excess = qty_excess

    @api.depends(
        "manual_fulfillment_ids",
        "manual_fulfillment_ids.quantity",
    )
    def _compute_qty_manual_fulfillment(self):
        for record in self:
            result = 0.0
            for manual in record.manual_fulfillment_ids:
                result += manual.quantity
            record.qty_manual_fulfillment = result
            record._compute_qty_fulfilled()

    def _compute_qty_fulfilled(self):
        for record in self:
            result = 0.0
            if (
                record.performance_obligation_id
                and record.performance_obligation_id.fulfillment_field_id
            ):
                result = getattr(
                    record, record.performance_obligation_id.fulfillment_field_id.name
                )
            record.qty_fulfilled = result

    @api.model
    def _get_policy_field(self):
        res = super(PerformanceObligationAcceptance, self)._get_policy_field()
        policy_field = [
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

    @api.onchange(
        "performance_obligation_id",
    )
    def onchange_policy_template_id(self):
        template_id = self._get_template_policy()
        self.policy_template_id = template_id

    @api.onchange(
        "partner_id",
    )
    def onchange_contract_id(self):
        self.contract_id = False

    @api.onchange(
        "contract_id",
    )
    def onchange_performance_obligation_id(self):
        self.performance_obligation_id = False

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
