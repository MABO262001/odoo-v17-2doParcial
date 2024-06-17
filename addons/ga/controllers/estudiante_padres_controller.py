from odoo import http
from odoo.http import request
import json

class EstudiantePadresController(http.Controller):

    @http.route('/ga/estudiantes/<int:estudiante_id>/padres', type='http', auth='public', methods=['GET'])
    def get_padres(self, estudiante_id):
        try:
            estudiante = request.env['gestion_academica.estudiante'].sudo().browse(estudiante_id)
            if not estudiante.exists():
                return request.make_response(
                    json.dumps({'error': 'Estudiante no encontrado'}),
                    headers=[('Content-Type', 'application/json')],
                    status=404
                )

            padres = estudiante.parentesco_ids.mapped('apoderado_id')
            data = []
            for padre in padres:
                data.append({
                    'id': padre.id,
                    'ci': padre.ci,
                    'name': padre.name,
                    'telefono': padre.telefono,
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
