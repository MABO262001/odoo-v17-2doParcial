from odoo import models, fields, api

class GestionParaleloMateriaProfesorHorario(models.Model):
    _name = 'gestion_academica.gestion_paralelo_materia_profesor_horario'
    _description = 'Tabla intermedia para gestión, paralelo y materia_profesor_horario'
    _rec_name = 'combinacion'

    materia_profesor_horario_id = fields.Many2one('gestion_academica.materia_profesor_horario', string='Profesor, materia, horario', required=True)
    profesor_id = fields.Many2one(related='materia_profesor_horario_id.profesor_id', string='Profesor', store=True)
    materia_id = fields.Many2one(related='materia_profesor_horario_id.materia_id', string='Materia simple', store=True)
    horario_id = fields.Many2one(related='materia_profesor_horario_id.horario_id', string='Horario', store=True)

    gestion_paralelo_id = fields.Many2one('gestion_academica.gestion_paralelo', string='Gestion-Paralelo', required=True)
    gestion_id = fields.Many2one(related='gestion_paralelo_id.gestion_id', string='Gestion', store=True)
    paralelo_id = fields.Many2one(related='gestion_paralelo_id.paralelo_id', string='Paralelo', store=True)

    nota_ids = fields.One2many('gestion_academica.nota', 'gestion_paralelo_materia_profesor_horario_id', string='Notas')

    combinacion = fields.Char(string='Materia', compute='_compute_combination', store=True)

    @api.depends('materia_profesor_horario_id', 'gestion_paralelo_id')
    def _compute_combination(self):
        for record in self:
            record.combinacion = f"{record.materia_profesor_horario_id.materia_profesor_horario_name} - {record.gestion_paralelo_id.gestion_paralelo_name} "

    def name_get(self):
        result = []
        for record in self:
            name = combinacion
            result.append((record.id, name))
        return result
