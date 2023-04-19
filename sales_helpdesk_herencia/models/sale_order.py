from odoo import models, api, fields, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'SaleOrder'

    ticket_ids = fields.One2many(
        comodel_name='helpdesk.ticket',
        inverse_name='sale_id', 
        string='Tickets')
    
    #boton para crear ticket
    def create_ticket(self):
        self.ensure_one()
        tag_ids = self.order_line.mapped('product_id.helpdesk_tag_id').ids #remirar ¿como lo sabe?
        self.env['helpdesk.ticket'].create({
            'name':f'{self.name} Issue',
            'tag_ids': [(6,0, tag_ids)],
            'sale_id':self.id,
        })
    
    #mod metodo heredado
    def action_cancel(self):
        self.ticket_ids.cancel_multi()
        return super(SaleOrder,self).action_cancel()
    