from odoo import models, fields

class Curso(models.Model):
    _name = 'gestion_academica.curso'
    _description = 'Modelo para gestionar cursos'

    name = fields.Char(string='Nombre del Curso', required=True)
    descripcion = fields.Text(string='Descripción')
    sucursal_id = fields.Many2one('gestion_academica.sucursal', string='Sucursal', required=True)
    paralelo_ids = fields.One2many('gestion_academica.paralelo', 'curso_id', string='Paralelos')