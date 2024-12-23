from email.policy import default
from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    codigo_registro= fields.Char(string="Codigo de Registro" )
    employee_autorizado = fields.Char( string='Autorizado ')
    modalidad_sale = fields.Many2one('pago.modalidad', string='Modalidad de Pago',required=True)
    lugar_entrega= fields.Char(string="Lugar de Entrega" , required=True )
    orden_compra= fields.Char(string="Orden de Compra")



    def action_post_cotiz(self):
        #super()
        self.correlativo_cotizacion=self.get_nro_cotizacion()


    def get_nro_cotizacion(self):
        '''metodo que crea el Nombre del asiento contable si la secuencia no esta creada, crea una con el
        nombre: 'l10n_ve_cuenta_retencion_iva'''

        self.ensure_one()
        SEQUENCE_CODE = 'nro_cotizacion'
        company_id = 1
        IrSequence = self.env['ir.sequence'].with_context(force_company=1)
        name = IrSequence.next_by_code(SEQUENCE_CODE)

        # si aún no existe una secuencia para esta empresa, cree una
        if not name:
            IrSequence.sudo().create({
                'prefix': 'COT/',
                'name': 'secuencia de cotizacion al cliente %s' % 1,
                'code': SEQUENCE_CODE,
                'implementation': 'no_gap',
                'padding': 4,
                'number_increment': 1,
                'company_id': 1,
            })
            name = IrSequence.next_by_code(SEQUENCE_CODE)
        #self.invoice_number_cli=name
        return name  



   # partner_id = fields.Many2one('child_ids', string='Autorizado ', required=True)

    def formato_fecha(self,date):
        fecha = str(date)
        fecha_aux=fecha
        ano=fecha_aux[0:4]
        mes=fecha[5:7]
        dia=fecha[8:10]  
        resultado=dia+"/"+mes+"/"+ano
        return resultado

    def float_format(self,valor):
        #valor=self.base_tax
        if valor:
            result = '{:,.2f}'.format(valor)
            result = result.replace(',','*')
            result = result.replace('.',',')
            result = result.replace('*','.')
        else:
            result = "0,00"
        return result


    def doc_cedula(self,aux):
        #nro_doc=self.partner_id.vat
        busca_partner = self.env['res.partner'].search([('id','=',aux)])
        for det in busca_partner:
            tipo_doc=busca_partner.doc_type
            if busca_partner.vat:
                nro_doc=str(busca_partner.vat)
            else:
                nro_doc="00000000"
            tipo_doc=busca_partner.doc_type
        nro_doc=nro_doc.replace('V','')
        nro_doc=nro_doc.replace('v','')
        nro_doc=nro_doc.replace('E','')
        nro_doc=nro_doc.replace('e','')
        nro_doc=nro_doc.replace('G','')
        nro_doc=nro_doc.replace('g','')
        nro_doc=nro_doc.replace('J','')
        nro_doc=nro_doc.replace('j','')
        nro_doc=nro_doc.replace('P','')
        nro_doc=nro_doc.replace('p','')
        nro_doc=nro_doc.replace('-','')
        
        if tipo_doc=="v":
            tipo_doc="V"
        if tipo_doc=="e":
            tipo_doc="E"
        if tipo_doc=="g":
            tipo_doc="G"
        if tipo_doc=="j":
            tipo_doc="J"
        if tipo_doc=="p":
            tipo_doc="P"
        resultado=str(tipo_doc)+"-"+str(nro_doc)
        return resultado





class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    def formato_fecha(self,date):
        fecha = str(date)
        fecha_aux=fecha
        ano=fecha_aux[0:4]
        mes=fecha[5:7]
        dia=fecha[8:10]  
        resultado=dia+"/"+mes+"/"+ano
        return resultado

    
    def fact_div(self,valor):
        self.currency_id.id
        fecha_contable_doc=self.date
        monto_factura=self.amount_total
        valor_aux=0
        #raise UserError(_('moneda compañia: %s')%self.company_id.currency_id.id)
        if self.currency_id.id!=self.doc_currency_id.id:
            if self.currency_id!=self.company_id.currency_id.id:
                tasa= self.env['account.move'].search([('id','=',self.id)],order="id asc")
                for det_tasa in tasa:
                    monto_nativo=det_tasa.amount_untaxed_signed
                    monto_extran=det_tasa.amount_untaxed
                    valor_aux=abs(monto_nativo/monto_extran)
                rate=round(valor_aux,3)  # LANTA
                #rate=round(valor_aux,2)  # ODOO SH
                resultado=valor*rate
            else:
                resultado=valor
        else:
            resultado=valor
        return resultado
   
    def float_format(self,valor):
        #valor=self.base_tax
        if valor:
            result = '{:,.2f}'.format(valor)
            result = result.replace(',','*')
            result = result.replace('.',',')
            result = result.replace('*','.')
        else:
            result = "0,00"
        return result

    def integer_format(self,valor):
        result = '{:,.0f}'.format(valor)
        return result


    def fact_div_line(self,valor):
        valor_aux=0
        #raise UserError(_('moneda compañia: %s')%self.company_id.currency_id.id)
        if self.move_id.currency_id.id!=self.move_id.doc_currency_id.id:
            tasa= self.env['account.move'].search([('id','=',self.move_id.id)],order="id asc")
            for det_tasa in tasa:
                monto_nativo=det_tasa.amount_untaxed_signed
                monto_extran=det_tasa.amount_untaxed
                valor_aux=abs(monto_nativo/monto_extran)
            rate=round(valor_aux,3)  # LANTA
            #rate=round(valor_aux,2)  # ODOO SH
            resultado=valor*rate
        else:
            resultado=valor
        return resultado


class SalesModalidad(models.Model):
    _name = 'pago.modalidad'


    name = fields.Char(string='Nombre de la modalidad')
    codigo = fields.Char(string='Codigo ')
   


class ResCompany(models.Model):
    _inherit = 'res.company'

    name_sucursal = fields.Char(string='Sucursal')
   