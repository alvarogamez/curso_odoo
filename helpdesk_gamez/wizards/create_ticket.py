from odoo import models, api, fields

class CreateTicket(models.TransientModel):
    _name = 'create.ticket'
    _description='create ticket'
  
    name = fields.Char(required=True)
    
    #@api.model
    def create_ticket(self):
        self.ensure_one()
        active_id = self._context.get('active_id',False)
        if active_id and self._context.get('active_model') == 'helpdesk.ticket.tag':
            ticket = self.env['helpdesk.ticket'].create({
                'name':self.name,
                'tag_ids':[(6,0,[active_id])]
            })
            action = self.env.ref('helpdesk_gamez.helpdesk_ticket_action').read()[0] #modulo.action_xml (hay otras formas)
            action['res_id']=ticket.id
            action['view_mode']= 'form'
            return action
        return {'type':'ir.actions.act_window_close'}