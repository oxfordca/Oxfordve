from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TopBoxBonusRange(models.Model):
    _name = 'top.box.bonus.range'
    _description = 'Rangos Configurables para el Cálculo del Bono Top Box'

    name = fields.Char(string="Rango", compute="_compute_name", store=True)
    min_boxes = fields.Integer(string="Mínimo de Cajas", required=True)
    max_boxes = fields.Integer(string="Máximo de Cajas", required=True)
    amount = fields.Float(string="Monto a Pagar", required=True)

    @api.depends('min_boxes', 'max_boxes')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.min_boxes} - {record.max_boxes} Cajas"

    @api.constrains('min_boxes', 'max_boxes')
    def _check_unique_ranges(self):
        for record in self:
            # Validar que min_boxes y max_boxes sean valores no negativos
            if record.min_boxes < 0 or record.max_boxes < 0:
                raise ValidationError("Los valores de mínimo y máximo de cajas no pueden ser negativos.")

            # Validar que min_boxes sea menor que max_boxes
            if record.min_boxes >= record.max_boxes:
                raise ValidationError("El valor mínimo debe ser menor que el valor máximo.")

            # Comprobar si hay otros registros con rangos que se solapen
            overlapping_ranges = self.search([
                ('id', '!=', record.id),  # Excluir el registro actual
                ('min_boxes', '<=', record.max_boxes),
                ('max_boxes', '>=', record.min_boxes)
            ])
            if overlapping_ranges:
                raise ValidationError("No puedes tener rangos que se solapen con otros existentes.")
