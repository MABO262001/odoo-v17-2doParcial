from odoo import http
from odoo.http import request
import json

class NotaController(http.Controller):

    @http.route('/ga/notas/<int:estudiante_id>', type='http', auth='public', methods=['GET'])
    def get_notas(self, estudiante_id):
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

            notas_data = []
            unique_combinations = set()
            for inscripcion in inscripciones:
                gestion_id = inscripcion.gestion_id.id
                gestion_name = inscripcion.gestion_id.name
                gestion_paralelo_materia_profesor_horarios = inscripcion.gestion_paralelo_id.gestion_paralelo_materia_profesor_horario_ids
                for gpmph in gestion_paralelo_materia_profesor_horarios:
                    materia = gpmph.materia_id
                    combination_key = (materia.id, gestion_id)
                    if combination_key in unique_combinations:
                        continue
                    unique_combinations.add(combination_key)
                    notas = request.env['gestion_academica.nota'].sudo().search([
                        ('estudiante_id', '=', estudiante_id),
                        ('materia_id', '=', materia.id),
                        ('gestion_id', '=', gestion_id)
                    ])
                    if notas:
                        total_notas = sum(nota.nota for nota in notas)
                        cantidad_notas = len(notas)
                        ppa = total_notas / cantidad_notas if cantidad_notas > 0 else 0
                        notas_data.append({
                            'estudiante_id': estudiante.id,
                            'estudiante_name': estudiante.name,
                            'materia_id': materia.id,
                            'materia_name': materia.name,
                            'gestion_id': gestion_id,
                            'gestion_name': gestion_name,
                            'ppa': ppa
                        })

            return request.make_response(
                json.dumps(notas_data),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers=[('Content-Type', 'application/json')],
                status=500
            )
