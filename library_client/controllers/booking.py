from odoo import http
from odoo.http import request, route

class Booking(http.Controller):
    
    @http.route("/library/books/login_booking")
    def booking(self, **kw):
        return request.render("library_client.login_booking")