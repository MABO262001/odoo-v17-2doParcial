from odoo import models, fields

class Parentesco(models.Model):
    _name = 'gestion_academica.parentesco'
    _description = 'Tabla intermedia para gestionar parentescos'

    name = fields.Char(string='Tipo de parentesco', required=True)
    apoderado_id = fields.Many2one('gestion_academica.apoderado', string='Apoderado', required=True, ondelete='cascade')
    estudiante_id = fields.Many2one('gestion_academica.estudiante', string='Estudiante', required=True, ondelete='cascade')

    ci_apoderado = fields.Char(related='apoderado_id.ci', string='CI', store=True)
    nombre_apoderado = fields.Char(related='apoderado_id.name', string='Nombre Apoderado', store=True)

    nombre_estudiante = fields.Char(related='estudiante_id.name', string='Nombre Estudiante', store=True)

