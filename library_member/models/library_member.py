from odoo import fields, models, api

class Member(models.Model):
    _name = "library.member"
    _description = "Library Member"
    _inherit = {"mail.thread", "mail.activity.mixin"}

    name = fields.Char("Name", index=True)
    email = fields.Char("Email", required = True)
    avatar = fields.Binary("Avatar")
    card_number = fields.Char()
    phone = fields.Char(string="Phone")
    partner_id = fields.Many2one(
        "res.partner",
        ondelete="cascade",
        required=False,
    )
    user_id = fields.Many2one("res.users", string="User")  # Asocia el usuario

    @api.model
    def create(self, vals):
        if "partner_id" not in vals or not vals["partner_id"]:
            partner_vals = {
                "name": vals.get("name", "Nuevo Miembro"),
                "email": vals.get("email", ""),
                "image_1920": vals.get("avatar", False)
            }
            new_partner = self.env["res.partner"].create(partner_vals)
            vals["partner_id"] = new_partner.id

        if "user_id" not in vals and self.env.user.id:
            vals["user_id"] = self.env.user.id

        return super(Member, self).create(vals)
