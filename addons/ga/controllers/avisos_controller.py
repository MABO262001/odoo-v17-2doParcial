from odoo import http
from odoo.http import request
import json

class AvisosController(http.Controller):
    @http.route('/ga/avisos/completos', type='http', auth='public', methods=['GET'])
    def get_avisos_completos(self):
        try:
            avisos = request.env['gestion_academica.aviso'].sudo().search([])
            avisos_data = []
            for aviso in avisos:
                apoderados_data = []
                sucursal = aviso.sucursal_id
                cursos = sucursal.curso_ids
                for curso in cursos:
                    paralelos = curso.paralelo_ids
                    for paralelo in paralelos:
                        inscripciones = request.env['gestion_academica.inscripcion'].sudo().search([('curso_id', '=', curso.id), ('paralelo_id', '=', paralelo.id)])
                        for inscripcion in inscripciones:
                            estudiante = inscripcion.estudiante_id
                            for parentesco in estudiante.parentesco_ids:
                                apoderado = parentesco.apoderado_id
                                if apoderado not in apoderados_data:
                                    apoderados_data.append({
                                        'apoderado_id': apoderado.id,
                                        'apoderado_name': apoderado.name,
                                        'telefono': apoderado.telefono,
                                        'ci': apoderado.ci
                                    })

                avisos_data.append({
                    'aviso_id': aviso.id,
                    'titulo': aviso.name,
                    'contenido': aviso.contenido,
                    'fecha': aviso.fecha.strftime('%Y-%m-%d'),
                    'sucursal': aviso.sucursal_id.name,
                    'apoderados': apoderados_data
                })

            return request.make_response(
                json.dumps(avisos_data),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers=[('Content-Type', 'application/json')],
                status=500
            )
