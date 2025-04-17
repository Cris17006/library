from odoo import fields, models, api, exceptions

class Checkout(models.Model):
    _name = "library.checkout"
    _description = "Checkout Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    # Text fields
    name = fields.Char(string="Title", tracking=True)

    # Numeric fields
    member_image = fields.Binary(related="user_id.image_128")
    avatar = fields.Binary(related="member_id.avatar")
    count_checkouts = fields.Integer(compute="_compute_count_checkouts", store=True)

    # Selection fields
    state = fields.Selection(related="stage_id.state", tracking=True)
    kanban_state = fields.Selection(
        [
            ("normal", "In Progress"),
            ("blocked", "Blocked"),
            ("done", "Ready for next stage")
        ],
        string="Kanban State",
        default="normal"
    )
    priority = fields.Selection(
        [
            ("0", "High"),
            ("1", "Very High"),
            ("2", "Critical")
        ],
        default="0"
    )

    # Color fields
    color = fields.Integer()

    

    # Default stage function
    @api.model
    def _default_stage_id(self):
        return self.env["library.checkout.stage"].search([("state", "=", "new")], limit=1)

    # Relational fields
    member_id = fields.Many2one('library.member', string="Member", required=True, tracking=True)
    user_id = fields.Many2one("res.users", string="Librarian", default=lambda s: s.env.user, tracking=True)
    request_date = fields.Date(default=fields.Date.today(), store=True, readonly=False, tracking=True)
    line_ids = fields.One2many("library.checkout.line", "checkout_id", string="Borrowed Books")
    library_book = fields.Many2one("library.book", string="Book", tracking=True)
    num_books = fields.Integer(string="Num. Books", compute="_compute_num_books", store=True, readonly=True)
    stage_id = fields.Many2one(
        "library.checkout.stage", 
        string="Stage", 
        default=_default_stage_id, 
        group_expand="_group_expand_stage_id", 
        tracking=True
    )
    image = fields.Binary(related='library_book.image', string="Image", store=True)

    # Date fields
    checkout_date = fields.Date(readonly=True, tracking=True)
    closed_date = fields.Date(readonly=True, tracking=True)

    @api.model
    def _group_expand_stage_id(self, stages, domain, order=None):
        return stages.search([], order=order or "sequence, name asc")

    @api.constrains("stage_id")
    def _check_valid_state_transition(self):
        for record in self:
            if record.stage_id.state in ("open", "close"):
                raise exceptions.UserError("State not allowed for new checkouts.")

    def write(self, vals):
        # Reset kanban state when changing stage
        if "stage_id" in vals and "kanban_state" not in vals:
            vals["kanban_state"] = "normal"
            
        Stage = self.env["library.checkout.stage"]
        old_states = {rec.id: rec.stage_id.state for rec in self if rec.stage_id}

        result = super().write(vals)

        if "stage_id" in vals:
            new_states = {
                rec.id: Stage.browse(vals["stage_id"]).state for rec in self if rec.stage_id
            }

            updates = {}
            for rec in self:
                if rec.id in old_states and rec.id in new_states:
                    if new_states[rec.id] == "open" and old_states[rec.id] != "open":
                        updates[rec.id] = {"checkout_date": fields.Date.today()}
                    elif new_states[rec.id] == "done" and old_states[rec.id] != "done":
                        updates[rec.id] = {"closed_date": fields.Date.today()}

            for rec_id, update_vals in updates.items():
                self.browse(rec_id).with_context(_checkout_write=True).write(update_vals)

        return result

    @api.onchange("member_id")
    def _compute_request_date_onchange(self):
        if self.request_date != fields.Date.today():
            self.request_date = fields.Date.today()
            return {
                "warning": {
                    "title": "Changed Request Date",
                    "message": "Request date changed to today."
                }
            }

    def button_done(self):
        done_stage = self.env["library.checkout.stage"].search([("state", "=", "done")], limit=1)
        self.write({"stage_id": done_stage.id})
        return True

    @api.depends("line_ids")
    def _compute_num_books(self):
        for checkout in self:
            checkout.num_books = len(checkout.line_ids)

    @api.depends("member_id")
    def _compute_count_checkouts(self):
        checkout_data = self.env["library.checkout"].read_group(
            [("member_id", "in", self.mapped("member_id").ids), ("state", "not in", ["done", "cancel"])],
            ["member_id"],
            ["member_id"]
        )
        count_map = {data["member_id"][0]: data["member_id_count"] for data in checkout_data}

        for checkout in self:
            checkout.count_checkouts = count_map.get(checkout.member_id.id, 0)
