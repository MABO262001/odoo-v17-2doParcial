from odoo import models, fields

class Apoderado(models.Model):
    _name = 'gestion_academica.apoderado'
    _description = 'Modelo para gestionar apoderados'

    name = fields.Char(string='Nombre del apoderado', required=True)
    telefono = fields.Char(string='Telefono del apoderado', required=True)
    ci = fields.Char(string='CI del apoderado', required=True)
    parentesco_ids = fields.One2many('gestion_academica.parentesco', 'apoderado_id', string='Estudiantes')


