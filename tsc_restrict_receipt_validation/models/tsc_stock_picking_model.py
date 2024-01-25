# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class TscStockPicking(models.Model):

    _inherit = 'stock.picking'

    def button_validate(self):
        tsc_has_group = self.env.user.has_group(
            'tsc_restrict_receipt_validation.tsc_group_validate_merchandise_receptions'
        )


        for record in self:
            condicion_propia = record.picking_type_code == 'incoming' and record.location_id.usage != 'customer' and not tsc_has_group

            if condicion_propia:
                raise UserError(_('Due to security restrictions, you have no permission to validate this operation.'))

        return super(TscStockPicking, self).button_validate()
    



