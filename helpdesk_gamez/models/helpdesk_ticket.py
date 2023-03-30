from odoo import models, fields, api

class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Ticket'
    
    name = fields.Char(string='Name', required=True) #nombre obligado
    description = fields.Text(string='Description')
    date = fields.Date(string='Date')
    
    # campo estado
    state = fields.Selection(
        string='State', default='n',selection=[
        ('n', 'Nuevo'), ('a', 'Asignado'),
        ('p','En proceso'),('pen','Pendiente'),
        ('r','Resuelto'),('c','Cancelado')])
    # tiempo dedicado en horas
    time = fields.Float(string='Time')
    #asignado 
    assigned = fields.Boolean(
        string='Assigned',
        compute='_compute_assigned') # == (readonly=True)
    #fecha limite
    date_limit = fields.Date(string='Date Limit')
    #accion correctiva
    action_corrective = fields.Html(
        string='Corrective Action',
        help='Describe corrective actions to do')
    #accion preventiva
    action_preventive = fields.Html(
        string='Preventive Action',
        help='Describe preventive actions to do')
    #total tickets
    total = fields.Integer(
        string='total',
        compute='_compute_total')
    
    assigned = fields.Boolean(
        string='Assigned',
        compute='_compute_assigned')
    
    #campos relacionales
    user_id = fields.Many2one(
        comodel_name='res.users', 
        string='Assigned to')
    
    actions_ids = fields.One2many(
        comodel_name='helpdesk.ticket.action',
        inverse_name='ticket_id', #campo m2o de la otra tabla
        string='Actions')
    
    tag_ids = fields.Many2many( #en plural 'ids'
        comodel_name='helpdesk.ticket.tag', 
        string='Tags')
    
    # metodos
    #asignar 1 o varios estados
    def do_assign(self):
        self.ensure_one() #pasa de uno en uno/ llamar desde un boton
        self.write({
            'state': 'a',
            'assigned': True
        })
    # Es lo mismo que el WRITE, solo se usa si hay un factor a modificar
    #    for ticket in self:
    #        ticket.state= 'a'
    #        ticket.assigned = 'True' 
    
    #en proceso
    def do_proccess(self):
        self.ensure_one()
        self.state = 'p'
    #pendiente
    def do_pend(self):
        self.ensure_one()
        self.state = 'pen'
    #finalizar
    def do_resolve(self):
        self.ensure_one()
        self.state = 'r'
    #cancelar
    def do_cancel(self):
        self.ensure_one()
        self.state = 'c'
    #asignado, si le añades user
    @api.depends('user_id')
    def _compute_assigned(self):
        for record in self:
            record.assigned = self.user_id and True or False #lo mismo que un if 

    #total tickets asociados a un user
    @api.depends('user_id')
    def _compute_total(self):
        for record in self:
            if self.user_id == record.user_id:
               self.total = len(record.user_id) 
        
    
#total = fields.Float(compute='_compute_total' )
#@api.depends('value', 'tax')
#def _compute_total (self):
#    for record in self:
#        record.total = record.value * record.tax