from odoo import models, fields

class HelpdeskTicketTag(models.Model): # metodo siempre en singular
    _name = 'helpdesk.ticket.tag'
    _description = 'Tag'
    
    name = fields.Char()

    #campos relacionales
    ticket_ids = fields.Many2many( #en plural 'ids'
        comodel_name='helpdesk.ticket', 
        string='Ticket')
