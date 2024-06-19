from odoo import models, fields, api


class Profesor(models.Model):
    _name = "gestion_academica.profesor"
    _description = "Modelo para gestionar profesores"

    name = fields.Char(string="Nombre", required=True)
    correo = fields.Char(string="Correo")
    genero = fields.Selection(
        [("male", "Masculino"), ("female", "Femenino"), ("other", "Otro")],
        string="Género",
    )
    direccion = fields.Char(string="Dirección")
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")
    telefono = fields.Char(string="Teléfono")
    sueldo = fields.Integer(string="Sueldo")
    sucursal_id = fields.Many2one(
        "gestion_academica.sucursal", string="Sucursal", required=True
    )
    
    employee_id = fields.Many2one('hr.employee', string='Empleado', readonly=True)

    materia_profesor_ids = fields.One2many('gestion_academica.materia_profesor', 'profesor_id', string='Materias')
    
    #Campo computado
    expense_ids = fields.One2many('hr.expense', compute='_compute_expense_ids', string='Gastos', store=False)
    
    @api.depends('employee_id')
    def _compute_expense_ids(self):
        for profesor in self:
            try:
                if profesor.employee_id:
                    expenses = self.env['hr.expense'].search([('employee_id', '=', profesor.employee_id.id)])
                    profesor.expense_ids = expenses
                else:
                    profesor.expense_ids = []
            except Exception as e:
                _logger.error("Error computing expenses for professor %s: %s", profesor.id, str(e))
                profesor.expense_ids = []
                
    @api.model
    def create(self, vals):
        record = super(Profesor, self).create(vals)

        maestro_job = self.env['hr.job'].search([('name', '=', 'Maestro')], limit=1)
        if not maestro_job:
            maestro_job = self.env['hr.job'].create({
                'name': 'Maestro'
            })
            
        employee = self.env['hr.employee'].create({
            'name': record.name,
            'company_id': self.env.company.id, 
            'job_id': maestro_job.id, 
            'work_phone': record.telefono,
            'mobile_phone': record.telefono,
            'work_email': record.correo,
            'employee_type': 'employee',
        })
        
        record.employee_id = employee.id

        return record
    
    

