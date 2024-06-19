from odoo import http
from odoo.http import request

class GestionAcademicaController(http.Controller):

    @http.route('/gestion_academica/report_horario', type='http', auth='user')
    def report_horario(self, gestion_id, paralelo_id, **kwargs):
        gestion_id = int(gestion_id)
        paralelo_id = int(paralelo_id)
        data = request.env['gestion_academica.gestion_paralelo_materia_profesor_horario'].get_horario_data(gestion_id, paralelo_id)
        return request.render('gestion_academica.report_horario', {'data': data})
