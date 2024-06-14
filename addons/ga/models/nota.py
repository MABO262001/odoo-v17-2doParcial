from odoo import models, fields, api
import re

class Nota(models.Model):
    _name = 'gestion_academica.nota'
    _description = 'Tabla intermedia para gestionar las notas'
    _rec_name = 'name_completo_nota'

    gestion_paralelo_id = fields.Many2one('gestion_academica.gestion_paralelo', string='Gestion Paralelo', required=True)
    gestion_paralelo_materia_profesor_horario_id = fields.Many2one(
        'gestion_academica.gestion_paralelo_materia_profesor_horario', 
        string='Gestion paralelo materia profesor horario', 
        required=True
    )
    profesor_id = fields.Many2one(related='gestion_paralelo_materia_profesor_horario_id.profesor_id', string='Profesor', store=True)
    materia_id = fields.Many2one(related='gestion_paralelo_materia_profesor_horario_id.materia_id', string='Materia', store=True)
    horario_id = fields.Many2one(related='gestion_paralelo_materia_profesor_horario_id.horario_id', string='Horario', store=True)
    gestion_id = fields.Many2one(related='gestion_paralelo_materia_profesor_horario_id.gestion_id', string='Gestion', store=True)
    paralelo_id = fields.Many2one(related='gestion_paralelo_materia_profesor_horario_id.paralelo_id', string='Paralelo', store=True)
    curso_id = fields.Many2one(related='paralelo_id.curso_id', string='Curso', store=True, readonly=True)
    sucursal_id = fields.Many2one(related='paralelo_id.sucursal_id', string='Sucursal', store=True, readonly=True)
    subgestion_id = fields.Many2one('gestion_academica.subgestion', string='Subgestion', required=True)
    estudiante_id = fields.Many2one('gestion_academica.estudiante', string='Estudiante', store=True)
    name_completo_nota = fields.Char(string='Nombre Completo', compute='_compute_nota', store=True)
    nota = fields.Float(string='Nota', required=True)

    # VARIABLES DE COMPUTO (NO SE ALMACENAAAAAN!!!!!!)
    gestion_paralelo_ids = fields.Many2many('gestion_academica.gestion_paralelo', compute='_compute_gestion_paralelo_ids', store=False)
    subgestion_ids = fields.Many2many('gestion_academica.subgestion', compute='_compute_gestion_paralelo_materia_profesor_horario_ids', store=False)
    gestion_paralelo_materia_profesor_horario_ids = fields.Many2many('gestion_academica.gestion_paralelo_materia_profesor_horario', compute='_compute_gestion_paralelo_materia_profesor_horario_ids', store=False)

    @api.depends('profesor_id', 'materia_id', 'horario_id', 'gestion_id', 'paralelo_id', 'curso_id')
    def _compute_nota(self):
        for record in self:
            record.name_completo_nota = f"{record.curso_id.name}  {record.materia_id.name} - {record.nota} - {record.subgestion_id.name} {record.gestion_id.name}"

    def name_get(self):
        result = []
        for record in self:
            name = record.name_completo_nota
            result.append((record.id, name))
        return result

    @api.depends('estudiante_id')
    def _compute_gestion_paralelo_ids(self):
        for record in self:
            if record.estudiante_id:
                estudiante_id_str = str(record.estudiante_id.id)
                estudiante_id = re.sub(r'NewId_', '', estudiante_id_str)
                if estudiante_id.isdigit():
                    estudiante_id = int(estudiante_id)
                    inscripciones = self.env['gestion_academica.inscripcion'].search([('estudiante_id', '=', estudiante_id)])

                    gestion_paralelo_ids = inscripciones.mapped('gestion_paralelo_id').ids
                    record.gestion_paralelo_ids = [(6, 0, gestion_paralelo_ids)]
                else:
                    record.gestion_paralelo_ids = [(6, 0, [])]
            else:
                record.gestion_paralelo_ids = [(6, 0, [])]

    @api.onchange('estudiante_id')
    def _onchange_estudiante_id(self):
        self._compute_gestion_paralelo_ids()
        return {
            'domain': {
                'gestion_paralelo_id': [('id', 'in', self.gestion_paralelo_ids.ids)]
            }
        }

    @api.onchange('gestion_paralelo_id')
    def _onchange_gestion_paralelo_id(self):
        self._compute_gestion_paralelo_materia_profesor_horario_ids()
        return {
            'domain': {
                'gestion_paralelo_materia_profesor_horario_id': [('id', 'in', self.gestion_paralelo_materia_profesor_horario_ids.ids)],
                'subgestion_id': [('id', 'in', self.subgestion_ids.ids)]
            }
        }

    @api.depends('gestion_paralelo_id')
    def _compute_gestion_paralelo_materia_profesor_horario_ids(self):
        for record in self:
            gestion_paralelo_materia_profesor_horarios = self.env['gestion_academica.gestion_paralelo_materia_profesor_horario'].search([
                ('gestion_paralelo_id', '=', self.gestion_paralelo_id.id)
            ])

            gestion_paralelo_materia_profesor_horario_ids = gestion_paralelo_materia_profesor_horarios.ids

            gestion_ids = gestion_paralelo_materia_profesor_horarios.mapped('gestion_id').ids
            print("GESTION IDS: +++++++", gestion_ids)
            subgestion_ids = self.env['gestion_academica.subgestion'].search([('gestion_id', 'in', gestion_ids)]).ids
            print("SUBGESTION IDS: +++++++", subgestion_ids)
            record.subgestion_ids = [(6, 0, subgestion_ids)]

            record.gestion_paralelo_materia_profesor_horario_ids = gestion_paralelo_materia_profesor_horario_ids

