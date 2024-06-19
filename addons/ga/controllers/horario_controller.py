from odoo import http
from odoo.http import request
import json

class HorarioController(http.Controller):

    @http.route('/ga/horarios/<int:estudiante_id>', type='http', auth='public', methods=['GET'])
    def get_horarios(self, estudiante_id):
        try:
            estudiante = request.env['gestion_academica.estudiante'].sudo().browse(estudiante_id)
            if not estudiante.exists():
                return request.make_response(
                    json.dumps({'error': 'Estudiante no encontrado'}),
                    headers=[('Content-Type', 'application/json')],
                    status=404
                )

            inscripciones = request.env['gestion_academica.inscripcion'].sudo().search([('estudiante_id', '=', estudiante_id)])
            if not inscripciones:
                return request.make_response(
                    json.dumps({'error': 'No se encontraron inscripciones para el estudiante'}),
                    headers=[('Content-Type', 'application/json')],
                    status=404
                )

            horarios_data = []
            for inscripcion in inscripciones:
                gestion_paralelo_materia_profesor_horarios = inscripcion.gestion_paralelo_id.gestion_paralelo_materia_profesor_horario_ids
                for gpmph in gestion_paralelo_materia_profesor_horarios:
                    horario = gpmph.horario_id
                    materia = gpmph.materia_id
                    profesor = gpmph.profesor_id
                    horarios_data.append({
                        'estudiante_id': estudiante.id,
                        'estudiante': estudiante.name,
                        'materia_id': materia.id,
                        'materia': materia.name,
                        'profesor': profesor.name,
                        'dia': horario.dia,
                        'hora_inicio': horario.hora_inicio,
                        'minuto_inicio': horario.minuto_inicio,
                        'am_pm_inicio': horario.am_pm_inicio,
                        'hora_final': horario.hora_final,
                        'minuto_final': horario.minuto_final,
                        'am_pm_final': horario.am_pm_final,
                    })

            return request.make_response(
                json.dumps(horarios_data),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers=[('Content-Type', 'application/json')],
                status=500
            )
