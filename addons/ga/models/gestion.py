from odoo import models, fields

class Gestion(models.Model):
    _name = 'gestion_academica.gestion'
    _description = 'Modelo para gestionar'

    name = fields.Char(string='Nombre de la Gestión', required=True)
    descripcion = fields.Text(string='Descripción')
    gestion_paralelo_ids = fields.One2many('gestion_academica.gestion_paralelo', 'gestion_id', string='Paralelos')
    subgestion_ids = fields.One2many('gestion_academica.subgestion', 'gestion_id', string='Gestiones')


    def _compute_paralelo_ids(self):
        for record in self:
            record.paralelo_ids = record.gestion_paralelo_ids.mapped('paralelo_id')
