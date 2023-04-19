from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta


class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Ticket'
    _inherit = ['mail.thread.cc',
                'mail.thread.blacklist',
                'mail.activity.mixin']
    _primary_email = 'email_from'

    #funciones default
        #fecha hoy
    @api.model #para todos los valores que se quiera/ sin ponerlos como default!!!
    def default_get(self, default_fields):
        vals = super(HelpdeskTicket, self).default_get(default_fields)
        vals.update({'date':fields.date.today()})

        return vals

    # campos especificos
    name = fields.Char(string='Name', required=True) #nombre obligado
    description = fields.Text(string='Description')
    date = fields.Date(string='Date')

    # campo estado / darle un nombre mas completo a la base de datos
    state = fields.Selection(
        string='State', default='n',selection=[
        ('n', 'Nuevo'), ('a', 'Asignado'),
        ('p','En proceso'),('pen','Pendiente'),
        ('r','Resuelto'),('c','Cancelado')])
    # tiempo dedicado en horas
    time = fields.Float(string='Time',
        compute='_get_time', #campo calculado / devuelve valores que dependen de otro
        inverse='_set_time', #invesro de compute / fija valores que se reflejan con el compute
        search='_search_time') #filtros de busqueda relacionados con campos que derivan de un compute
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
    # input name tag
    tag_name = fields.Char(
        string = 'Nombre del Tag')
    #email / campo obligado para mixin
    email_from = fields.Char(
        string='Email')
    
    #campos relacionales
    user_id = fields.Many2one(
        comodel_name='res.users', 
        string='Assigned to'
        )
    
    actions_ids = fields.One2many(
        comodel_name='helpdesk.ticket.action',
        inverse_name='ticket_id', #campo m2o de la otra tabla
        string='Actions')
    
    tag_ids = fields.Many2many( #en plural 'ids'
        comodel_name='helpdesk.ticket.tag', 
        string='Tags')

    partner_id = fields.Many2one(
        comodel_name='res.partner', 
        string='Partner')
    
    
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
    #cancelar de uno en uno
    def do_cancel(self):
        self.ensure_one()
        self.state = 'c'
    
    #cancelar varios
    def cancel_multi(self):
        for record in self:
            record.do_cancel()
    
    #compute, inverse y search de action_ids.time
    @api.depends('actions_ids.time') # OJO con lo que pones!!!!!!!!!
    def _get_time(self):
        for record in self:
            record.time = sum(record.actions_ids.mapped('time')) # mapped: funcion que genera un array /el for que se suma; sum: f. que suma todos los datos del array
            #es lo mismo que:
                #total_time = 0
                #for action in record.action_ids:
                #   total_time += action.time
                #record.time = total_time
    def _set_time(self):
        for record in self:
            if record.time:
                time_now = sum(record.actions_ids.mapped('time'))
                next_time= record.time - time_now #con la diferencia se crea otra action para llegar al tiempo total
                if next_time:
                    data = {
                        'name': 'act gen', 
                        'time':next_time, 
                        'date':fields.date.today(), 
                        'ticket_id':record.id}
                    #busc= 'Helpdesk.Ticket.action'; ponerlo bien para que no sea un lio/ busc.lower()
                    self.env['helpdesk.ticket.action'].create(data)

    def _search_time(self, operator, value):
        actions = self.env['helpdesk.ticket.action'].search([('time',operator,value)]) #busqueda sobre el tiempo de la accion, muestra el ticket: nombre, fecha, estado

        return [('id','in',actions.mapped('ticket_id').ids)]
        
    
    #asignado, si le añades user
    @api.depends('user_id')
    def _compute_assigned(self):
        for record in self:
            record.assigned = self.user_id and True or False #lo mismo que un if 

    #total tickets asociados a un user
    @api.depends('user_id')
    def _compute_total(self):
        for record in self:
            #en la busqueda se necesita el .id para que no salga el fallo de dupla
            cont_tickets = self.env['helpdesk.ticket'].search([('user_id','=',record.user_id.id)])
            record.total = len(cont_tickets)

    #actions/ crear a partir de el boton
    def create_tag(self):
        self.ensure_one()
        #opc 1
        #self.write({
        #    'tag_ids':[(0,0,{'name':self.tag_name})]
        #})    
        ##opc 2
        #tag = self.env['helpdesk.ticket.tag'].create({
        #    'name': self.tag_name
        #})
        #self.write({
        #    'tag_ids':[(4,tag.id,0)]
        #}) 
        ##opc 3
        #tag = self.env['helpdesk.ticket.tag'].create({
        #    'name': self.tag_name
        #})
        #self.write({
        #    'tag_ids':[(6,0,tag.ids)]
        #}) 
        ##opc 4
        #tag = self.env['helpdesk.ticket.tag'].create({
        #    'name': self.tag_name,
        #    'ticket_ids':[(6,0,self.ids)]
        #})
        action = self.env.ref('helpdesk_gamez.action_new_tag').read()[0] #modulo.action_xml (hay otras formas)
        action['context'] = {
            'default_name': self.tag_name,
            'default_ticket_ids':[(6,0,self.ids)]
        }
        
        self.tag_name = False

        return action
        

    #decoradores / restricciones y updates(en el momento)
    @api.constrains('time')
    def _limit_time(self): #mod los ifs
        for record in self:
            if record.time and record.time < 0:
                if record.time and record.time > 8: # no funciona hallar la respuesta / (quiza hay que hacer dos funciones)
                    raise ValidationError (_("El tiempo debe estar en horas positivas y ser inferior a 8H" ))
                raise ValidationError (_("El tiempo debe estar en horas positivas"))

    @api.onchange('date') # para que funcionara a la inversa a que meterlo por parametro aqui y if
    def _plus_date(self):
        self.date_limit = self.date and self.date + timedelta(days=1) #hay que usar timedelta para sumar horas o dias o meses / importado arriba
        