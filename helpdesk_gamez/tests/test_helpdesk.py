from odoo.exceptions import ValidationError
from odoo.tests import common

class TestHelpdesk(common.TransactionCase):

    def setUp(self):
        super(TestHelpdesk, self).setUp()

        self.ticket = self.env["helpdesk.ticket"].create({
            'name':'Test ticket'
        })
        self.user_id = self.ref('base.user_admin')

    def test_01_ticket(self):
        print('test 01: igualar el nombre a')
        self.assertEqual(self.ticket.name, "Test ticket")
    
    #def test_02_ticket(self): /no tira mirarlo
    #    print('test 02: comprobar id')
    #    self.assertEqual(self.ticket.user_id.id, self.env['res.user'])
    #    self.ticket.user_id = self.user_id
    #    self.assertEqual(self.ticket.user_id.id, self.user_id)

    def test_03_ticket(self):
        print('test 03: comprobacion por boolean')
        self.assertFalse(self.ticket.name == "asdskdja ticket")
    
    def test_04_ticket(self):
        print('test 04: comprobacion de raise Exception')
        self.ticket.time = 2
        self.ticket.time = 0

        with self.assertRaises(ValidationError), self.cr.savepoint():
            self.ticket.time = -7