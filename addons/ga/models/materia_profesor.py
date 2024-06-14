from odoo import models, fields, api

class MateriaProfesor(models.Model):
    _name = 'gestion_academica.materia_profesor'
    _description = 'Relación entre Profesores y Materias'
    _rec_name = 'profesor_materia_name'

    profesor_id = fields.Many2one('gestion_academica.profesor', string='Profesor', required=True)
    materia_id = fields.Many2one('gestion_academica.materia', string='Materia', required=True)
    materia_profesor_horario_ids = fields.One2many('gestion_academica.materia_profesor_horario', 'materia_profesor_id', string='Horarios')

    profesor_materia_name = fields.Char(string='Nombre Completo', compute='_compute_profesor_materia_name', store=True)

    @api.depends('profesor_id', 'materia_id')
    def _compute_profesor_materia_name(self):
        for record in self:
            record.profesor_materia_name = f"{record.profesor_id.name} - {record.materia_id.name}"

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.profesor_id.name} - {record.materia_id.name}"
            result.append((record.id, name))
        return result