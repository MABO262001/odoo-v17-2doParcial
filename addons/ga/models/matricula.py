from odoo import models, fields, api

class Matricula(models.Model):
    _name = 'gestion_academica.matricula'
    _description = 'Modelo para gestionar matrículas'

    pagada = fields.Selection(
        [('pagada', 'pagada'),
        ('impaga', 'impaga'),],
        string='Estado',
        required=True
    )

    monto = fields.Float(string="Monto", required=True)
    subgestion_id = fields.Many2one('gestion_academica.subgestion', string='Subgestion', required=True, ondelete='cascade')
    gestion_id = fields.Many2one(related='subgestion_id.gestion_id', string='Gestión', readonly=True)
    estudiante_id = fields.Many2one('gestion_academica.estudiante', string='Estudiante', required=True, ondelete='cascade')

    
    @api.model
    def create_account_move(self, matricula):
        partner_id = matricula.estudiante_id.partner_id.id
        if not partner_id:
            raise ValueError("El estudiante no tiene un partner_id asociado.")
        
        property_account_income_categ_id = self.env['ir.property']._get('property_account_income_categ_id', 'product.category')
        if not property_account_income_categ_id:
            raise ValidationError("No se ha configurado la cuenta de ingresos predeterminada para las categorías de productos.")

        move = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': partner_id,
            'invoice_date': fields.Date.context_today(self),
            'invoice_line_ids': [(0, 0, {
                'name': 'Pago de Matrícula',
                'quantity': 1,
                'price_unit': matricula.monto,
                'account_id': property_account_income_categ_id.id,
            })],
        })
        return move

    @api.model
    def create(self, vals):
        record = super(Matricula, self).create(vals)
        if record.pagada == 'pagada':
            self.create_account_move(record)
        return record

    def write(self, vals):
        result = super(Matricula, self).write(vals)
        for record in self:
            if 'pagada' in vals and vals['pagada'] == 'pagada':
                self.create_account_move(record)
        return result