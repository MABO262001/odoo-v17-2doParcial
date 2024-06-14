from odoo import models, fields

class Materia(models.Model):
    _name = 'gestion_academica.materia'
    _description = 'Modelo para gestionar materias'

    name = fields.Char(string='Nombre', required=True)
    sigla = fields.Char(string='Sigla', required=True)
    materia_profesor_ids = fields.One2many('gestion_academica.materia_profesor', 'materia_id', string='Profesores')
