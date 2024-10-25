from odoo import models, fields, api
from datetime import datetime


class TopBoxBonusWizard(models.TransientModel):
    _name = 'top.box.bonus.wizard'
    _description = 'Wizard para Generar Reporte de Bono Top Box'

    month = fields.Selection(selection=[
        ('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'),
        ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'),
        ('7', 'Julio'), ('8', 'Agosto'), ('9', 'Septiembre'),
        ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre'),
    ], string='Mes', required=True, default=lambda self: str(datetime.now().month))
    year = fields.Selection(selection=[
        (str(year), str(year)) for year in range(datetime.now().year - 3, datetime.now().year + 1)
    ], string='Año', required=True, default=lambda self: str(datetime.now().year))

    def generate_report(self):
        self.env['top.box.bonus.report'].create_report(self.month, self.year, self.env.user.branch_id,
                                                                        self.env.user.id)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reporte de Bono Top Box',
            'view_mode': 'tree',
            'view_id': self.env.ref('commissions.view_top_box_bonus_report_tree').id,
            'res_model': 'top.box.bonus.report',
            'context': {'wizard_id': self.id},
            'target': 'current',
        }
