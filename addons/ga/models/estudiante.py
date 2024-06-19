from odoo import models, fields, api

class Estudiante(models.Model):
    _name = 'gestion_academica.estudiante'
    _description = 'Modelo para gestionar estudiantes'

    name = fields.Char(string='Nombre', required=True)
    correo = fields.Char(string='Correo')
    genero = fields.Selection(
        [('male', 'Masculino'), ('female', 'Femenino'), ('other', '35 tipos de geys')],
        string='Género'
    )
    direccion = fields.Char(string='Dirección')
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento')
    telefono = fields.Char(string='Teléfono')
    parentesco_ids = fields.One2many('gestion_academica.parentesco', 'estudiante_id', string='Apoderados')
    matricula_ids = fields.One2many('gestion_academica.matricula', 'estudiante_id', string='Pagos')
    
    partner_id = fields.Many2one('res.partner', string='Cliente', readonly=True)
    nota_ids = fields.One2many('gestion_academica.nota', 'estudiante_id', string='Notas')

    pago_ids = fields.One2many('account.move', compute='_compute_pago_id', string='Pagos', store=False)
    
    @api.model
    def create(self, vals):
        
        record = super(Estudiante, self).create(vals)
        partner = self.env['res.partner'].create({
                'name': record.name,
                'complete_name': record.name,
                'tz': 'America/La_Paz',
                'type': 'contact',
                'commercial_company_name': record.name,
                'active': True,
                'is_company': True,
                'partner_share': True,
            })
        record.partner_id = partner.id
        
        return record