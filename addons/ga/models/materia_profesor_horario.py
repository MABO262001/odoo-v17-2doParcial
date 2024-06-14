from odoo import models, fields, api

class MateriaProfesorHorario(models.Model):
    _name = 'gestion_academica.materia_profesor_horario'
    _description = 'Relación entre MateriaProfesor y Horario'
    _rec_name = 'materia_profesor_horario_name'


    horario_id = fields.Many2one('gestion_academica.horario', string='Horario', required=True)
    materia_profesor_id = fields.Many2one('gestion_academica.materia_profesor', string='Materia Profesor', required=True)
    profesor_id = fields.Many2one(related='materia_profesor_id.profesor_id', string='Profesor', store=True)
    materia_id = fields.Many2one(related='materia_profesor_id.materia_id', string='Materia', store=True)

    gestion_paralelo_materia_profesor_horario_ids = fields.One2many('gestion_academica.gestion_paralelo_materia_profesor_horario', 'materia_profesor_horario_id', string='Materia Profesor Horarios')

    materia_profesor_horario_name = fields.Char(string='Materia - horario - profesor', compute='_compute_materia_profesor_horario', store=True)

    @api.depends('materia_id', 'profesor_id','horario_id')
    def _compute_materia_profesor_horario(self):
        for record in self:
            record.materia_profesor_horario_name = f"{record.materia_id.name} - {record.horario_id.horario_completo} - {record.profesor_id.name} "

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.materia_id.name} - {record.horario_id.horario_completo} - {record.profesor_id.name} "
            result.append((record.id, name))
        return result