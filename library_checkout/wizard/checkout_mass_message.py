from odoo import api, exceptions, fields, models
from odoo.fields import Command
import logging, pdb, ipdb



class CheckoutMassMessage(models.TransientModel):
    _name = "library.checkout.massmessage"
    _description = "Send Message to Borrowers"
    _logger = logging.getLogger(__name__)

    checkout_ids = fields.Many2many("library.checkout", string="Checkouts")
    message_subject = fields.Char()
    message_body = fields.Html()

    @api.model
    def default_get(self, field_names):
        defaults_dict = super().default_get(field_names)
        checkout_ids = self.env.context.get("active_ids", [])
        # Ensure checkout_ids is always a list
        if isinstance(checkout_ids, int):
            checkout_ids = [checkout_ids]
        if "checkout_ids" in field_names and checkout_ids:
            defaults_dict["checkout_ids"] = [Command.set(checkout_ids)]
        return defaults_dict

    def button_send(self):
        self.ensure_one()
        if not self.checkout_ids:
            raise exceptions.UserError(
                "No Checkouts were selected"
            )
        if not self.message_body:
            raise exceptions.UserError(
                "A message body is required"
            )
        if not self.message_body or not self.message_subject:
            raise exceptions.UserError("Message subject and body cannot be empty.")
        for checkout in self.checkout_ids:
            checkout.message_post(
                body=self.message_body,
                subject=self.message_subject,
                message_type="comment"
            )
            self._logger.debug(
                "Message on %d to followers: %s",
                checkout.id,
                checkout.message_follower_ids
            )
        self._logger.info(
            "Posted %d messages to the checkouts: %s",
            len(self.checkout_ids),
            str(self.checkout_ids)
        )
        return True
    