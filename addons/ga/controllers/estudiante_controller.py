from odoo import http
from odoo.http import request
import json

class EstudianteController(http.Controller):

    @http.route('/ga/estudiantes', type='http', auth='public', methods=['GET'])
    def get_estudiantes(self):
        try:
            estudiantes = request.env['gestion_academica.estudiante'].sudo().search([])
            data = []
            for estudiante in estudiantes:
                data.append({
                    'id': estudiante.id,
                    'name': estudiante.name,
                    'correo': estudiante.correo,
                    'genero': estudiante.genero,
                    'direccion': estudiante.direccion,
                    'fecha_nacimiento': estudiante.fecha_nacimiento.strftime('%Y-%m-%d') if estudiante.fecha_nacimiento else '',
                    'telefono': estudiante.telefono,
                    'apoderado_id': estudiante.parentesco_ids.apoderado_id.id,
                    'apoderado': estudiante.parentesco_ids.apoderado_id.name,
                })
            return request.make_response(
                json.dumps(data),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers=[('Content-Type', 'application/json')],
                status=500
            )
