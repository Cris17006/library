from odoo import http
from odoo.http import route
from odoo.http import request
from odoo.addons.portal.controllers import portal

class CustomerPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super(CustomerPortal, self)._prepare_home_portal_values(counters)
        
        if "book_checkout_count" in counters:
            count = request.env["library.checkout"].search_count([])
            values["book_checkout_count"] = count
        return values

    @route (["/my/book-checkouts", "/my/book-checkouts/page/<int:page>"], auth = "user", website = True)
    def my_book_checkouts(self,page=1, **kw):
        Checkout = request.env["library.checkout"]
        domain = []

        # Prepare pager data
        checkout_count = Checkout.search_count(domain)

        pager_data = portal.pager(
            url = "/my/book_checkouts",
            total = checkout_count,
            page = page,
            step = self._items_per_page
        )

        # Recordset according to pager and domain filter
        checkouts = Checkout.search(
            domain,
            limit = self._items_per_page,
            offset = pager_data["offset"]
        )

        # Prepare template values and render
        values = self._prepare_portal_layout_values()
        values.update(
            {
                "checkouts": checkouts,
                "page_name": "book-checkouts",
                "default_url": "/my/book-checkouts",
                "pager": pager_data
            }
        )

        return request.render(
            "library_portal.my_book_checkouts",
            values
        )

    @http.route(['/my/book-checkout/<model("library.checkout"):doc>'], type='http', auth="user", website=True)
    def portal_book_checkout(self, doc, **kw):
        return request.render("library_portal.book_checkout", {
            'doc': doc,
        })

    @http.route(['/my/modify-member/<model("library.member"):member_id>'], type='http', auth="user", website=True)
    def portal_modify_member(self, member_id, **kw):
        return request.render("library_portal.modify_member", {
            'member_id': member_id,
        })

    @http.route(['/modify/member-info'], type='http', auth="user", website=True, methods=['POST'])
    def modify_member_info(self, **post):
        member_id = int(post.get('member_id', 0))

        if member_id:
            member = request.env['library.member'].browse(member_id)
            # Update member information
            values = {
                'name': post.get('Name'),
                'email': post.get('email'),
                'card_number': post.get('card_number'),
                'phone': post.get('phone'),
            }
            member.write(values)

        return request.redirect('/my/book-checkouts')
    
    @http.route(['/my/modify-checkout/<model("library.checkout"):checkout_id>'], type='http', auth="user", website=True)
    def portal_modify_checkout(self, checkout_id, **kw):
        return request.render("library_portal.modify_checkout", {
            'checkout_id': checkout_id,
        })


    @http.route(['/modify/checkout-info'], type='http', auth="user", website=True, methods=['POST'])
    def modify_checkout_info(self, **post):
        checkout_id = int(post.get('checkout_id', 0))

        if checkout_id:
            checkout = request.env['library.checkout'].browse(checkout_id)
            # Update checkout information
            values = {
                'name': post.get('name'),
                'priority': post.get('priority'),
                'request_date': post.get('request_date'),
            }
            
            checkout.write(values)
        return request.redirect('/my/book-checkouts')

    @http.route('/my/checkout_books', type='http', auth='user', website=True)
    def portal_my_book_checkouts(self, **kw):

        user = request.env['library.member'].email

        member = request.env['library.member'].sudo().search([('partner_id.email', '=', user)], limit = 1)

        if member:
            # Buscar los préstamos del miembro
            checkouts = request.env['library.checkout'].sudo().search([('member_id', '=', member.id)])
            
        return request.render(
            "library_portal.modify_checkout_books", {
                'checkouts': checkouts,
            }
        )




   


