from odoo import models, fields, api
from odoo.exceptions import ValidationError

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
    
    @api.model
    def create(self, vals):
        new_record = super(GestionParaleloMateriaProfesorHorario, self).create(vals)
        new_record._check_horario_overlap()
        return new_record

    def write(self, vals):
        result = super(GestionParaleloMateriaProfesorHorario, self).write(vals)
        self._check_horario_overlap()
        return result

    def _get_time_in_minutes(self, hora, minuto, am_pm):
        total_minutes = int(hora) * 60 + int(minuto)
        if am_pm == 'PM' and hora != '12':
            total_minutes += 12 * 60
        if am_pm == 'AM' and hora == '12':
            total_minutes -= 12 * 60
        return total_minutes

    def _check_horario_overlap(self):
        for record in self:
            horario = record.horario_id
            hora_inicio_nueva = self._get_time_in_minutes(horario.hora_inicio, horario.minuto_inicio, horario.am_pm_inicio)
            hora_final_nueva = self._get_time_in_minutes(horario.hora_final, horario.minuto_final, horario.am_pm_final)
            
            overlapping_records = self.search([
                ('gestion_paralelo_id', '=', record.gestion_paralelo_id.id),
                ('horario_id.dia', '=', horario.dia),
                ('id', '!=', record.id),
            ])
            
            for overlapping_record in overlapping_records:
                horario_existente = overlapping_record.horario_id
                hora_inicio_existente = self._get_time_in_minutes(horario_existente.hora_inicio, horario_existente.minuto_inicio, horario_existente.am_pm_inicio)
                hora_final_existente = self._get_time_in_minutes(horario_existente.hora_final, horario_existente.minuto_final, horario_existente.am_pm_final)
                
                if (hora_inicio_nueva < hora_final_existente and hora_final_nueva > hora_inicio_existente):
                    raise ValidationError('Ya existe un registro con un horario que se superpone en el mismo día y rango de horas.')
    
    def get_horario_data(self, gestion_id, paralelo_id):
        horarios = self.search([('gestion_id', '=', gestion_id), ('paralelo_id', '=', paralelo_id)])
        data = {}
        for horario in horarios:
            dia = horario.horario_id.dia
            if dia not in data:
                data[dia] = []
            data[dia].append({
                'materia': horario.materia_id.name,
                'profesor': horario.profesor_id.name,
                'hora_inicio': f"{horario.horario_id.hora_inicio}:{horario.horario_id.minuto_inicio} {horario.horario_id.am_pm_inicio}",
                'hora_final': f"{horario.horario_id.hora_final}:{horario.horario_id.minuto_final} {horario.horario_id.am_pm_final}",
                'gestion': horario.gestion_id.name,
                'paralelo': horario.paralelo_id.name
            })
        return data