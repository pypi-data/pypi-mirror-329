# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ServiceContractFixItem(models.Model):
    _name = "service.contract_fix_item"
    _inherit = "service.contract_fix_item"

    pob_id = fields.Many2one(
        string="# PoB",
        comodel_name="service_contract.performance_obligation",
        compute="_compute_pob_id",
        store=False,
        compute_sudo=True,
    )

    @api.depends(
        "service_id.performance_obligation_ids",
        "service_id.performance_obligation_ids.product_id",
    )
    def _compute_pob_id(self):
        for record in self:
            result = False
            PoB = self.env["service_contract.performance_obligation"]
            criteria = [
                ("contract_id", "=", record.service_id.id),
                ("product_id", "=", record.product_id.id),
            ]
            pobs = PoB.search(criteria)
            if len(pobs) > 0:
                result = pobs[0]
            record.pob_id = result

    def action_create_pob(self):
        for record in self.sudo():
            record._create_pob()

    def _create_pob(self):
        self.ensure_one()
        if self.pob_id:
            return True
        PoB = self.env["service_contract.performance_obligation"]
        data = self._prepare_pob_data()
        PoB.create(data)

    def _prepare_pob_data(self):
        self.ensure_one()
        xmlid = (
            "ssi_revenue_recognition."
            "field_performance_obligation_acceptance__qty_manual_fulfillment"
        )
        manual_field = self.env.ref(xmlid)
        result = {
            "contract_id": self.service_id.id,
            "title": self.name,
            "date": self.service_id.date,
            "product_id": self.product_id.id,
            "currency_id": self.currency_id.id,
            "uom_quantity": self.quantity,
            "uom_id": self.product_id.uom_id.id,
            "price_unit": self.amount_untaxed,
            "progress_completion_method": "input",
            "revenue_recognition_timing": "point_in_time",
            "fulfillment_field_id": manual_field.id,
        }
        return result
