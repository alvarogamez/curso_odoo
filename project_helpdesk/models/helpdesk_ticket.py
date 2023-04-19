from odoo import models, api, fields, _

class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Ticket'
    _inherits={'project.task':'task_id'}

    #se necesita para herencias_por_delegacion
    task_id = fields.Many2one(
        comodel_name='project.task', 
        string='Tasks',
        auto_join=True, index=True, ondelete="cascade", required=True) 
    #accion correctiva
    action_corrective = fields.Html(
        string='Corrective Action',
        help='Describe corrective actions to do')
    #accion preventiva
    action_preventive = fields.Html(
        string='Preventive Action',
        help='Describe preventive actions to do')
    
    #en caso de error de function mod con / self.task_id
    def action_assign_to_me(self):
        self.ensure_one()
        return self.task_id.action_assign_to_me()
    
    def action_subtask(self):
        self.ensure_one()
        return self.task_id.action_subtask()
    
    def action_recurring_tasks(self):
        self.ensure_one()
        return self.task_id.action_recurring_tasks()
    
    def _message_get_suggested_recipients(self):
        self.ensure_one()
        return self.task_id._message_get_suggested_recipients()