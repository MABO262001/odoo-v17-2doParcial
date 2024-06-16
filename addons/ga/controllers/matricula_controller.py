from odoo import http
from odoo.http import request
import json

class MatriculaController(http.Controller):

    @http.route('/ga/matriculas', type='http', auth='public', methods=['GET'])
    def get_matriculas(self):
        try:
            matriculas = request.env['gestion_academica.matricula'].sudo().search([])
            data = []
            for matricula in matriculas:
                data.append({
                    'id_estudiante': matricula.estudiante_id.id,
                    'estudiante': matricula.estudiante_id.name,
                    'gestion': matricula.gestion_id.name,
                    'subgestion': matricula.subgestion_id.name,
                    'monto': matricula.monto,
                    'estado': matricula.pagada,
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
