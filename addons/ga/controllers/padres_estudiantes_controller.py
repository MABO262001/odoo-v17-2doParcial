from odoo import http
from odoo.http import request
import json

class PadresHijosController(http.Controller):

    @http.route('/ga/apoderados/<int:apoderado_id>/hijos', type='http', auth='public', methods=['GET'])
    def get_hijos(self, apoderado_id):
        try:
            apoderado = request.env['gestion_academica.apoderado'].sudo().browse(apoderado_id)
            if not apoderado.exists():
                return request.make_response(
                    json.dumps({'error': 'Apoderado no encontrado'}),
                    headers=[('Content-Type', 'application/json')],
                    status=404
                )

            hijos = apoderado.parentesco_ids.mapped('estudiante_id')
            data = []
            for hijo in hijos:
                data.append({
                    'id': hijo.id,
                    'name': hijo.name,
                    'correo': hijo.correo,
                    'genero': hijo.genero,
                    'direccion': hijo.direccion,
                    'fecha_nacimiento': hijo.fecha_nacimiento.strftime('%Y-%m-%d') if hijo.fecha_nacimiento else '',
                    'telefono': hijo.telefono,
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
