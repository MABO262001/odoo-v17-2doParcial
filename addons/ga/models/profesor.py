from odoo import models, fields


class Profesor(models.Model):
    _name = "gestion_academica.profesor"
    _description = "Modelo para gestionar profesores"

    name = fields.Char(string="Nombre", required=True)
    correo = fields.Char(string="Correo")
    genero = fields.Selection(
        [("male", "Masculino"), ("female", "Femenino"), ("other", "Otro")],
        string="Género",
    )
    direccion = fields.Char(string="Dirección")
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")
    telefono = fields.Char(string="Teléfono")
    sueldo = fields.Integer(string="Sueldo")
    sucursal_id = fields.Many2one(
        "gestion_academica.sucursal", string="Sucursal", required=True
    )

    materia_profesor_ids = fields.One2many('gestion_academica.materia_profesor', 'profesor_id', string='Materias')

