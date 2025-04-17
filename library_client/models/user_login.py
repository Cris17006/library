from odoo import api, fields, models

class UserLogin(models.Model):
    _name = "library.user.login"
    _description = "User can login and create new checkouts"

    user = fields.Char("Email", required = True, default = "library@gmail.com")
    password = fields.Char("Password", required = True)