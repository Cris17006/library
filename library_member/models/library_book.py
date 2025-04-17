# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Book(models.Model):
    _inherit = "library.book"

    is_available = fields.Boolean("Is Available?", default=True)
    isbn = fields.Char(help="Use a valid ISBN-13 or ISBN-10.")
    publisher_id = fields.Many2one('res.partner', string="Publisher", index=True)
    name = fields.Char("Title", required=True)

    def _check_isbn(self):
        self.ensure_one()
        
        digits = [int(x) for x in self.isbn if x.isdigit()]

        if len(digits) == 10:
            ponderators = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            total = sum(a * b for a, b in zip(digits[:9], ponderators))
            check = total % 11
            return digits[-1] == check
        else:
            return super()._check_isbn()
