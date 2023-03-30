from odoo import models, fields

class HelpdeskTicketAction(models.Model):
    _name = 'helpdesk.ticket.action'
    _description = 'Action'
    
    name = fields.Char() # string no necesario (se duplica)
    date = fields.Date()

    #campos relacionales
    ticket_id = fields.Many2one(
        comodel_name='helpdesk.ticket',
        string='Ticket')