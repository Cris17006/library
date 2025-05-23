from odoo import fields, models

class CheckoutStages(models.Model):
    _name = "library.checkout.stage"
    _description = "Checkout Stage"
    _order = "sequence"

    name = fields.Char()
    sequence = fields.Integer(default=10)
    fold = fields.Boolean()
    active = fields.Boolean(default = True)
    state = fields.Selection(
        [
            ("new", "Requested"),
            ("open", "Borrowed"),
            ("done", "Completed"),
            ("cancel", "Canceled")
        ], default = "new"
    )