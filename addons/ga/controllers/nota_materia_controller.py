from odoo import http
from odoo.http import request
import json

class NotaMateriaController(http.Controller):

    @http.route('/ga/notas/materia/<int:estudiante_id>', type='http', auth='public', methods=['GET'])
    def get_notas_materia(self, estudiante_id):
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
            for inscripcion in inscripciones:
                gestion_paralelo_materia_profesor_horarios = inscripcion.gestion_paralelo_id.gestion_paralelo_materia_profesor_horario_ids
                for gpmph in gestion_paralelo_materia_profesor_horarios:
                    notas = request.env['gestion_academica.nota'].sudo().search([
                        ('estudiante_id', '=', estudiante_id),
                        ('materia_id', '=', gpmph.materia_id.id),
                        ('gestion_id', '=', inscripcion.gestion_id.id)
                    ])
                    for nota in notas:
                        notas_data.append({
                            'curso_id': inscripcion.curso_id.id,
                            'curso_name': inscripcion.curso_id.name,
                            'paralelo_id': inscripcion.paralelo_id.id,
                            'paralelo_name': inscripcion.paralelo_id.name,
                            'materia_id': gpmph.materia_id.id,
                            'materia_name': gpmph.materia_id.name,
                            'nota_id': nota.id,
                            'nota_nota': nota.nota,
                            'subgestion_id': nota.subgestion_id.id,
                            'subgestion_name': nota.subgestion_id.name,
                            'gestion_id': inscripcion.gestion_id.id,
                            'gestion_name': inscripcion.gestion_id.name,
                            'estudiante_id': estudiante.id,
                            'estudiante_name': estudiante.name,
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
