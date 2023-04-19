from odoo import models, fields, api

class HelpdeskTicketTag(models.Model): # metodo siempre en singular
    _name = 'helpdesk.ticket.tag'
    _description = 'Tag'
    
    name = fields.Char()
    public = fields.Boolean()
    

    #campos relacionales
    ticket_ids = fields.Many2many( #en plural 'ids'
        comodel_name='helpdesk.ticket', 
        string='Ticket')

    #events /probar en casa
    # api.model
    #def cron_delete_tag(self):
    #    tickets = self.search(['ticket_ids','=',False])
    #    tickets.unlink()
        