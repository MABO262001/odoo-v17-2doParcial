from odoo import models, fields, api

class Paralelo(models.Model):
    _name = 'gestion_academica.paralelo'
    _description = 'Modelo para gestionar paralelos'
    _rec_name = 'paralelo_completo_name'

    
    name = fields.Char(string='Nombre del Paralelo', required=True)
    curso_id = fields.Many2one('gestion_academica.curso', string='Curso', required=True)
    sucursal_id = fields.Many2one(related='curso_id.sucursal_id', string='Sucursal', store=True, readonly=True)
    gestion_paralelo_ids = fields.One2many('gestion_academica.gestion_paralelo', 'paralelo_id', string='Gestiones')

    paralelo_completo_name = fields.Char(string='Paralelo', compute='_compute_paralelo', store=True)


    @api.depends('curso_id', 'name','sucursal_id')
    def _compute_paralelo(self):
        for record in self:
            record.paralelo_completo_name = f"{record.curso_id.name} {record.name} - {record.sucursal_id.name}"

    def name_get(self):
        result = []
        for record in self:
            name = record.paralelo_completo_name
            result.append((record.id, name))
        return result