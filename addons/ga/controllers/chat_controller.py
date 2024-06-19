
from odoo import http
from odoo.http import request
import json
class ChatController(http.Controller):
    @http.route('/ga/apoderado/<int:apoderado_id>/informacion_completa', type='http', auth='public', methods=['GET'])
    def get_apoderado_informacion_completa(self, apoderado_id):
        try:
            apoderado = request.env['gestion_academica.apoderado'].sudo().browse(apoderado_id)
            if not apoderado.exists():
                return request.make_response(
                    json.dumps({'error': 'Apoderado no encontrado'}),
                    headers=[('Content-Type', 'application/json')],
                    status=404
                )
            apoderado_data = {
                'apoderado_id': apoderado.id,
                'apoderado_name': apoderado.name,
                'telefono': apoderado.telefono,
                'ci': apoderado.ci,
                'estudiantes': []
            }
            for parentesco in apoderado.parentesco_ids:
                estudiante = parentesco.estudiante_id
                estudiante_data = {
                    'estudiante_id': estudiante.id,
                    'estudiante_name': estudiante.name,
                    'correo': estudiante.correo,
                    'genero': estudiante.genero,
                    'direccion': estudiante.direccion,
                    'fecha_nacimiento': estudiante.fecha_nacimiento.strftime('%Y-%m-%d') if estudiante.fecha_nacimiento else '',
                    'telefono': estudiante.telefono,
                    'matriculas': [],
                    'notas': [],
                    'cursos_paralelos': [],
                    'horarios': []
                }
                for matricula in estudiante.matricula_ids:
                    matricula_data = {
                        'matricula_id': matricula.id,
                        'gestion_id': matricula.gestion_id.id,
                        'gestion_name': matricula.gestion_id.name,
                        'subgestion_id': matricula.subgestion_id.id,
                        'subgestion_name': matricula.subgestion_id.name,
                        'monto': matricula.monto,
                        'estado': matricula.pagada
                    }
                    estudiante_data['matriculas'].append(matricula_data)
                inscripciones = request.env['gestion_academica.inscripcion'].sudo().search([('estudiante_id', '=', estudiante.id)])
                for inscripcion in inscripciones:
                    curso_paralelo_data = {
                        'curso_id': inscripcion.curso_id.id,
                        'curso_name': inscripcion.curso_id.name,
                        'paralelo_id': inscripcion.paralelo_id.id,
                        'paralelo_name': inscripcion.paralelo_id.name
                    }
                    estudiante_data['cursos_paralelos'].append(curso_paralelo_data)
                    for gpmph in inscripcion.gestion_paralelo_id.gestion_paralelo_materia_profesor_horario_ids:
                        horario = gpmph.horario_id
                        horario_data = {
                            'dia': horario.dia,
                            'hora_inicio': horario.hora_inicio,
                            'minuto_inicio': horario.minuto_inicio,
                            'am_pm_inicio': horario.am_pm_inicio,
                            'hora_final': horario.hora_final,
                            'minuto_final': horario.minuto_final,
                            'am_pm_final': horario.am_pm_final
                        }
                        estudiante_data['horarios'].append(horario_data)
                for nota in estudiante.nota_ids:
                    nota_data = {
                        'nota_id': nota.id,
                        'materia_id': nota.materia_id.id,
                        'materia_name': nota.materia_id.name,
                        'nota': nota.nota,
                        'gestion_id': nota.gestion_id.id,
                        'gestion_name': nota.gestion_id.name,
                        'subgestion_id': nota.subgestion_id.id,
                        'subgestion_name': nota.subgestion_id.name,
                        'curso_id': nota.curso_id.id,
                        'curso_name': nota.curso_id.name,
                        'paralelo_id': nota.paralelo_id.id,
                        'paralelo_name': nota.paralelo_id.name
                    }
                    estudiante_data['notas'].append(nota_data)
                apoderado_data['estudiantes'].append(estudiante_data)
            return request.make_response(
                json.dumps(apoderado_data),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers=[('Content-Type', 'application/json')],
                status=500
            )
