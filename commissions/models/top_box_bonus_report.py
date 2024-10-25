from odoo import fields, models, api
from datetime import timedelta, datetime


class TopBoxBonusReport(models.TransientModel):
    _name = 'top.box.bonus.report'
    _description = 'Reporte de Bono Top Box'

    team_id = fields.Many2one('crm.team', string='Equipo de Ventas', readonly=True)
    total_boxes_sold = fields.Float(string='Número de Cajas Vendidas', readonly=True)
    amount_to_pay = fields.Float(string='Monto a Pagar', readonly=True)

    @api.model
    def create_report(self, month, year, branch_id, user_id):
        # Limpiar todos los registros anteriores antes de crear uno nuevo
        self.search([]).unlink()

        # Convertir los parámetros a enteros
        month = int(month)
        year = int(year)

        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year, 12, 31, 23, 59, 59)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)

        for team in self.env['crm.team'].search([]):
            total_boxes_sold = self._get_total_boxes_sold(start_date, end_date, team.id)
            amount_to_pay = self._calculate_amount(total_boxes_sold)

            self.create({
                'team_id': team.id,
                'total_boxes_sold': total_boxes_sold,
                'amount_to_pay': amount_to_pay,
            })

    def _get_total_boxes_sold(self, date_start, date_end, team_id):
        """Calcula el total de cajas facturadas para un equipo de ventas en un rango de fechas."""
        query = """
            SELECT
                COALESCE(SUM(qty.qty_invoiced), 0)
            FROM(
                SELECT
                    CASE WHEN l.product_id IS NOT NULL THEN sum(l.qty_invoiced / u.factor * u2.factor) ELSE 0 END as qty_invoiced
                FROM sale_order_line l
                LEFT JOIN sale_order s on (s.id=l.order_id)
                LEFT JOIN product_product p on (l.product_id=p.id)
                LEFT JOIN product_template t on (p.product_tmpl_id=t.id)
                LEFT JOIN uom_uom u on (u.id=l.product_uom)
                LEFT JOIN uom_uom u2 on (u2.id=t.uom_id)
                WHERE s.date_order >= %s AND s.date_order <= %s AND s.team_id = %s
            GROUP BY l.product_id
            ) as qty;
        """
        self.env.cr.execute(query, (date_start, date_end, team_id))
        result = self.env.cr.fetchone()
        return result[0] if result else 0

    def _calculate_amount(self, total_boxes_sold):
        """Calcula el monto a pagar basado en la cantidad de cajas vendidas."""
        if total_boxes_sold < 1501:
            return 0
        elif 1501 <= total_boxes_sold < 2001:
            return 80
        elif 2001 <= total_boxes_sold < 2501:
            return 105
        elif 2501 <= total_boxes_sold < 3001:
            return 130
        elif 3001 <= total_boxes_sold < 3501:
            return 155
        elif 3501 <= total_boxes_sold < 4001:
            return 180
        elif 4001 <= total_boxes_sold < 4501:
            return 205
        elif 4501 <= total_boxes_sold < 5001:
            return 230
        else:
            return 255
