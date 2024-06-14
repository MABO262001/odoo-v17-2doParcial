from odoo import models, fields

class Estudiante(models.Model):
    _name = 'gestion_academica.estudiante'
    _description = 'Modelo para gestionar estudiantes'

    name = fields.Char(string='Nombre', required=True)
    correo = fields.Char(string='Correo')
    genero = fields.Selection(
        [('male', 'Masculino'), ('female', 'Femenino'), ('other', 'Otro')],
        string='Género'
    )
    direccion = fields.Char(string='Dirección')
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento')
    telefono = fields.Char(string='Teléfono')
    parentesco_ids = fields.One2many('gestion_academica.parentesco', 'estudiante_id', string='Apoderados')
    matricula_ids = fields.One2many('gestion_academica.matricula', 'estudiante_id', string='Pagos')

    nota_ids = fields.One2many('gestion_academica.nota', 'estudiante_id', string='Notas')
