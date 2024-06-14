from odoo import models, fields

class Bloque(models.Model):
    _name = 'gestion_academica.bloque'
    _description = 'Modelo para gestionar Bloques'

    name = fields.Char(string='Nombre del Bloque', required=True)
    ubicacion = fields.Text(string='Ubicacion')
    sucursal_id = fields.Many2one('gestion_academica.sucursal', string='Sucursal', required=True)
    piso_ids = fields.One2many('gestion_academica.piso', 'bloque_id', string='Pisos')