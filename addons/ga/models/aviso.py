from odoo import models, fields

class Aviso(models.Model):
    _name = 'gestion_academica.aviso'
    _description = 'Modelo para gestionar Avisos de sucursales'

    name = fields.Char(string='Titulo del aviso', required=True)
    contenido = fields.Text(string='Contenido')
    fecha = fields.Date(string='Fecha')
    sucursal_id = fields.Many2one('gestion_academica.sucursal', string='Sucursal', required=True)