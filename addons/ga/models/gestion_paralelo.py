from odoo import models, fields, api

class GestionParalelo(models.Model):
    _name = 'gestion_academica.gestion_paralelo'
    _description = 'Tabla intermedia para gestion y paralelos'
    _rec_name = 'gestion_paralelo_name'

    inscripcion_ids = fields.One2many('gestion_academica.inscripcion', 'gestion_paralelo_id', string='Inscripciones')

    gestion_id = fields.Many2one('gestion_academica.gestion', string='Gestión', required=True, ondelete='cascade')
    paralelo_id = fields.Many2one('gestion_academica.paralelo', string='Paralelo', required=True, ondelete='cascade')
    curso_id = fields.Many2one(related='paralelo_id.curso_id', string='Curso', store=True, readonly=True)
    sucursal_id = fields.Many2one(related='paralelo_id.sucursal_id', string='Sucursal', store=True, readonly=True)

    gestion_paralelo_materia_profesor_horario_ids = fields.One2many('gestion_academica.gestion_paralelo_materia_profesor_horario', 'gestion_paralelo_id', string='Materia Profesor Horarios')


    gestion_paralelo_name = fields.Char(string='Gestion, curso, paralelo', compute='_compute_gestion_paralelo', store=True)

    @api.depends('gestion_id', 'paralelo_id','curso_id','sucursal_id')
    def _compute_gestion_paralelo(self):
        for record in self:
            record.gestion_paralelo_name = f"{record.sucursal_id.name} - {record.gestion_id.name} - {record.curso_id.name}  {record.paralelo_id.name}"

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.sucursal_id.name} - {record.gestion_id.name} - {record.curso_id.name}  {record.paralelo_id.name}"
            result.append((record.id, name))
        return result