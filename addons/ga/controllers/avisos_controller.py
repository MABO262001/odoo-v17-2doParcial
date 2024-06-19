from odoo import http
from odoo.http import request
import json

class AvisosController(http.Controller):
    @http.route('/ga/sucursal/<int:sucursal_id>/avisos', type='http', auth='public', methods=['GET'])
    def get_avisos_por_sucursal(self, sucursal_id):
        try:
            # Obtener la sucursal especificada por sucursal_id
            sucursal = request.env['gestion_academica.sucursal'].sudo().browse(sucursal_id)
            if not sucursal.exists():
                return request.make_response(
                    json.dumps({'error': 'Sucursal no encontrada'}),
                    headers=[('Content-Type', 'application/json')],
                    status=404
                )
            
            # Preparar la lista de avisos de la sucursal y los datos de la sucursal
            sucursal_data = {
                'sucursal_id': sucursal.id,
                'sucursal_name': sucursal.name,
                'avisos': [],
                'apoderados': []
            }
            apoderados_ids = set()

            # Recorrer los cursos relacionados con la sucursal
            for curso in sucursal.curso_ids:
                # Recorrer los paralelos de cada curso
                for paralelo in curso.paralelo_ids:
                    # Recorrer las inscripciones de cada paralelo
                    for gestion_paralelo in paralelo.gestion_paralelo_ids:
                        for inscripcion in gestion_paralelo.inscripcion_ids:
                            estudiante = inscripcion.estudiante_id
                            # Recorrer los parentescos de cada estudiante para encontrar sus apoderados
                            for parentesco in estudiante.parentesco_ids:
                                apoderado = parentesco.apoderado_id
                                if apoderado.id not in apoderados_ids:
                                    apoderados_ids.add(apoderado.id)
                                    sucursal_data['apoderados'].append({
                                        'apoderado_id': apoderado.id,
                                        'apoderado_name': apoderado.name,
                                        'telefono': apoderado.telefono,
                                        'ci': apoderado.ci
                                    })

            # Agregar los avisos de la sucursal
            for aviso in sucursal.aviso_ids:
                sucursal_data['avisos'].append({
                    'aviso_id': aviso.id,
                    'titulo': aviso.name,
                    'contenido': aviso.contenido,
                    'fecha': aviso.fecha.strftime('%Y-%m-%d') if aviso.fecha else ''
                })
            
            # Responder con la información de los avisos y los apoderados en formato JSON
            return request.make_response(
                json.dumps(sucursal_data),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers=[('Content-Type', 'application/json')],
                status=500
            )
