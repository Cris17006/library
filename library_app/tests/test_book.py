from odoo.tests.common import TrsnsactionCase

class TestBook(TransactionCase):

    def setUp(self, *args, **kwargs):
        result = super().setUp(*args, **kwargs)
        user_admin = self.env.ref('base.user_admin')
        self.env = self.env(user=user_admin)
        self.book = self.env['library.book'].create({
            'name': "Odoo Development Essentials",
            'isbn': '879-1-78439-279-6'
        })

    def test_book_crate(self):
        "New Books are active by default"
        self.assertEqual(
            self.book.active, True
        )

    def test_check_isbn(self):
        "Check valid ISBN"
        self.assertTrue(
            self.book1._check_isbn()
        )