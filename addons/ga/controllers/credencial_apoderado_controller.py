from odoo import http
from odoo.http import request
import json

class CredencialApoderado(http.Controller):

    @http.route('/ga/credencial_apoderado', type='http', auth='public', methods=['GET'])
    def get_apoderados(self):
        try:
            apoderados = request.env['gestion_academica.apoderado'].sudo().search([])
            data = []
            for apoderado in apoderados:
                data.append({
                    'id': apoderado.id,
                    'ci': apoderado.ci,
                    'user': apoderado.name,
                    'telefono': apoderado.telefono,
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
