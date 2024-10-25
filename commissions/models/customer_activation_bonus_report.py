from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class CustomerActivationBonusReport(models.TransientModel):
    _name = 'customer.activation.bonus.report'
    _description = 'Reporte de Bono por Activación de Clientes'

    # Definición de campos para el reporte
    team_id = fields.Many2one('crm.team', string='Equipo de Ventas', readonly=True)
    total_active_customers = fields.Integer(string='Cantidad de Clientes Activos', readonly=True)
    activated_customers_month = fields.Integer(string='Clientes Activados en el Mes', readonly=True)
    percentage = fields.Float(string='Porcentaje', readonly=True)
    amount_to_pay = fields.Float(string='Monto a Pagar', readonly=True)
    activated_customers_previous_month = fields.Integer(string='Clientes Activados Mes Anterior', readonly=True)

    @api.model
    def create_report(self, percentage_limit ,bonus_amount, month, year, branch_id, user_id):
        # Limpiar todos los registros anteriores antes de crear uno nuevo
        self.search([]).unlink()

        # Convertir los parámetros a enteros
        month = int(month)
        year = int(year)

        # Definir fechas de inicio y fin del mes actual y del mes anterior
        start_date = fields.Date.from_string(f'{year}-{month}-01')
        if month == 12:
            end_date = fields.Date.from_string(f'{year}-12-31')
        else:
            end_date = fields.Date.from_string(f'{year}-{month + 1}-01') - relativedelta(days=1)

        # Definir fechas del mes anterior
        previous_month_date = start_date - relativedelta(months=1)
        previous_start_date = fields.Date.from_string(f'{previous_month_date.year}-{previous_month_date.month}-01')
        previous_end_date = start_date - relativedelta(days=1)

        report_lines = []

        for team in self.env['crm.team'].search([]):
            # Cantidad total de clientes activos (por ruta y rama) usando el campo `team_id` y `branch_id` de `res.partner`
            total_active_customers = self.env['res.partner'].search_count([
                ('team_id', '=', team.id),  # Filtrar por equipo de ventas
                ('branch_id', '=', branch_id.id),  # Filtrar por la rama seleccionada
                ('active', '=', True),  # Clientes activos
                # ('customer_rank', '>', 0),  # Considerar solo clientes
                ('type', '=', 'contact'),  # Solo contactos
            ])

            if total_active_customers <= 0:
                continue

            # Número de clientes activados en el mes (clientes con facturas posted y parcial o totalmente pagadas)
            activated_customers_month = self.env['account.move'].search_read([
                ('move_type', '=', 'out_invoice'),  # Solo facturas de venta
                ('state', '=', 'posted'),  # Facturas publicadas
                # ('payment_state', 'in', ['partial', 'paid']),  # Parcialmente pagadas o pagadas completamente
                ('invoice_date', '>=', start_date),
                ('invoice_date', '<=', end_date),
                ('team_id', '=', team.id),  # Relacionar la factura con el equipo de ventas
                ('branch_id', '=', branch_id.id),  # Relacionar la factura con la rama seleccionada
            ], ['partner_id'])

            activated_customers_month = len(set([record['partner_id'][0] for record in activated_customers_month]))

            # Número de clientes activados en el mes anterior (clientes con facturas posted y parcial o totalmente pagadas)
            activated_customers_previous_month = self.env['account.move'].search_read([
                ('move_type', '=', 'out_invoice'),  # Solo facturas de venta
                ('state', '=', 'posted'),  # Facturas publicadas
                # ('payment_state', 'in', ['partial', 'paid']),  # Parcialmente pagadas o pagadas completamente
                ('invoice_date', '>=', previous_start_date),
                ('invoice_date', '<=', previous_end_date),
                ('team_id', '=', team.id),  # Relacionar la factura con el equipo de ventas
                ('branch_id', '=', branch_id.id),  # Relacionar la factura con la rama seleccionada
            ], ['partner_id'])

            activated_customers_previous_month = len(
                set([record['partner_id'][0] for record in activated_customers_previous_month]))

            # Calcular el porcentaje de activación del mes
            percentage = (activated_customers_month / total_active_customers) if total_active_customers else 0

            # Calcular el monto a pagar basado en el porcentaje y el monto ingresado en el wizard
            if percentage < (percentage_limit / 100):
                amount_to_pay = 0
            else:
                amount_to_pay = (percentage) * (bonus_amount)

            # Crear el registro del reporte con todos los cálculos
            report_line = self.create({
                'team_id': team.id,
                'total_active_customers': total_active_customers,
                'activated_customers_month': activated_customers_month,
                'activated_customers_previous_month': activated_customers_previous_month,
                'percentage': percentage,
                'amount_to_pay': amount_to_pay,
            })
            report_lines.append(report_line)

        # Retornar todos los registros generados
        return self.search([('id', 'in', [line.id for line in report_lines])])
