from odoo import models, fields, api

class Inscripcion(models.Model):
    _name = 'gestion_academica.inscripcion'
    _description = 'Modelo para gestionar inscripciones'
    

    gestion_paralelo_id = fields.Many2one('gestion_academica.gestion_paralelo', string='Gestión-Paralelo', required=True, ondelete='cascade')
    gestion_id = fields.Many2one(related='gestion_paralelo_id.gestion_id', string='Gestión', store=True, readonly=True)
    paralelo_id = fields.Many2one(related='gestion_paralelo_id.paralelo_id', string='Paralelo', store=True, readonly=True)
    curso_id = fields.Many2one(related='gestion_paralelo_id.curso_id', string='Curso', store=True, readonly=True)
    sucursal_id = fields.Many2one(related='gestion_paralelo_id.sucursal_id', string='Sucursal', store=True, readonly=True)
    estudiante_id = fields.Many2one('gestion_academica.estudiante', string='Estudiante', required=True, ondelete='cascade')
    fecha = fields.Date(string='Fecha de Inscripción', required=True)
    es_becado = fields.Boolean(string='Es becado?')
    monto_total = fields.Float(string='Monto total')

    
    @api.model
    def create(self, vals):
        record = super(Inscripcion, self).create(vals)
        if record.gestion_id and record.estudiante_id:
            subgestiones = self.env['gestion_academica.subgestion'].search([('gestion_id', '=', record.gestion_id.id)])
            if(record.es_becado == True):
                monto = 0
                pagada = 'pagada'
            else:
                if subgestiones:
                    monto = record.monto_total / len(subgestiones)
                else:
                    monto = record.monto_total
                pagada = 'inpaga'
                
            for subgestion in subgestiones:
                self.env['gestion_academica.matricula'].create({
                    'gestion_id': record.gestion_id.id,
                    'estudiante_id': record.estudiante_id.id,
                    'subgestion_id': subgestion.id,
                    'monto': monto,
                    'pagada' : pagada,
                })
        return record