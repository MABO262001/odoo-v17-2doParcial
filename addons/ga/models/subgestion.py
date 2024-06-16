from odoo import models, fields

class Subgestion(models.Model):
    _name = 'gestion_academica.subgestion'
    _description = 'Modelo para gestionar subgestiones'

    name = fields.Char(string='Nombre de la division de la gestión', required=True)
    gestion_id = fields.Many2one('gestion_academica.gestion', string='Gestion', required=True)
