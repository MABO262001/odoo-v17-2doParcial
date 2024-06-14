from odoo import http
from odoo.http import request

class EstudianteController(http.Controller):

    @http.route('/open_cursos_view', type='http', auth='user', website=True)
    def open_cursos_view(self):
        return 1
