from odoo import models, fields, api

class Horario(models.Model):
    _name = 'gestion_academica.horario'
    _description = 'Modelo para gestionar horarios para las materias'
    _rec_name = 'horario_completo'

    dia = fields.Selection(
        [
            ('lunes', 'Lunes'),
            ('martes', 'Martes'),
            ('miercoles', 'Miércoles'),
            ('jueves', 'Jueves'),
            ('viernes', 'Viernes'),
            ('sabado', 'Sábado'),
            ('domingo', 'Domingo')
        ],
        string='Día',
        required=True
    )

    hora_inicio = fields.Selection(
        [(str(n), str(n)) for n in range(1, 13)],
        string='Hora inicio'
    )

    minuto_inicio = fields.Selection(
        [('00', '00'), ('15', '15'), ('30', '30'), ('45', '45')],
        string='Minuto inicio'
    )

    am_pm_inicio = fields.Selection(
        [('AM', 'AM'), ('PM', 'PM')],
        string='AM/PM inicio'
    )

    hora_final = fields.Selection(
        [(str(n), str(n)) for n in range(1, 13)],
        string='Hora final'
    )

    minuto_final = fields.Selection(
        [('00', '00'), ('15', '15'), ('30', '30'), ('45', '45')],
        string='Minuto final'
    )

    am_pm_final = fields.Selection(
        [('AM', 'AM'), ('PM', 'PM')],
        string='AM/PM final'
    )

    horario_completo = fields.Char(
        string='Horario Completo', 
        compute='_compute_horario', 
        store=True
    )
    
    materia_profesor_horario_ids = fields.One2many('gestion_academica.materia_profesor_horario', 'horario_id', string='Materia y Profesor')

    @api.constrains('hora_inicio', 'minuto_inicio', 'am_pm_inicio', 'hora_final', 'minuto_final', 'am_pm_final')
    def _check_hora_inicio_fin(self):
        for record in self:
            hora_inicio = self._get_time_in_minutes(record.hora_inicio, record.minuto_inicio, record.am_pm_inicio)
            hora_final = self._get_time_in_minutes(record.hora_final, record.minuto_final, record.am_pm_final)
            if hora_inicio >= hora_final:
                raise ValidationError('La hora de inicio debe ser anterior a la hora final.')

    def _get_time_in_minutes(self, hora, minuto, am_pm):
        total_minutes = int(hora) * 60 + int(minuto)
        if am_pm == 'PM' and hora != '12':
            total_minutes += 12 * 60
        if am_pm == 'AM' and hora == '12':
            total_minutes -= 12 * 60
        return total_minutes
        
    @api.depends('hora_inicio', 'minuto_inicio', 'am_pm_inicio', 'hora_final', 'minuto_final', 'am_pm_final')
    def _compute_horario(self):
        for record in self:
            record.horario_completo = f"{record.dia} {record.hora_inicio}:{record.minuto_inicio} {record.am_pm_inicio} - {record.hora_final}:{record.minuto_final} {record.am_pm_final}"

    def name_get(self):
        result = []
        for record in self:
            name = record.horario_completo
            result.append((record.id, name))
        return result
