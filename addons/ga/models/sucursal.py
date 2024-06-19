from odoo import models, fields

class Sucursal(models.Model):
    _name = 'gestion_academica.sucursal'
    _description = 'Modelo para gestionar sucursales'

    name = fields.Char(string='Nombre de la Sucursal', required=True)
    direccion = fields.Char(string='Dirección')
    curso_ids = fields.One2many('gestion_academica.curso', 'sucursal_id', string='Cursos')
    profesor_ids = fields.One2many('gestion_academica.profesor', 'sucursal_id', string='Sucursales')
    
    aviso_ids = fields.One2many('gestion_academica.aviso', 'sucursal_id', string='Avisos')
