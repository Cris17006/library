from odoo import http
from odoo.http import request, route

class Main(http.Controller):

    @http.route("/library/catalog", auth = "public", website = True)
    def catalog(self, **kwargs):
        Book = http.request.env["library.book"]
        books = Book.sudo().search([])
        return http.request.render(
            "library_portal.book_catalog_card", {"books": books},
        )

    @http.route(['/book/<model("library.book"):book>'], type='http', auth="public", website=True)
    def book_info(self, book, **kw):
        return request.render("library_portal.book_info", {
            'book_id': book,
        })

    @http.route(['/book_catalog'], type='http', auth="public", website=True)
    def book_catalog(self, q=None, **kwargs):
        domain = []
        if q:
            domain += ['|', ('name', 'ilike', q), ('isbn', 'ilike', q)]
        
        books = request.env['library.book'].sudo().search(domain)
        return request.render("library_portal.book_catalog_card", {
            'books': books,
            'q': q,
        })

    @http.route(['/book/<int:book_id>'], type='http', auth="public", website=True)
    def book_detail(self, book_id):
        book = request.env['library.book'].sudo().browse(book_id)
        return request.render("library_portal.book_info", {
            'book_id': book,
        })
