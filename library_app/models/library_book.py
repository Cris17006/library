from odoo import fields, models, api
from odoo.exceptions import ValidationError
import requests
import base64
from datetime import datetime

class Book(models.Model):
    _name="library.book"
    _description="Book"

    #String fields
    name = fields.Char("Title", default=None, help="Book cover title.", readonly=False, copy=False, groups="")

    synopsis = fields.Text("Synopsis", help = "Synopsis of book.", index = True)

    isbn = fields.Char("ISBN")
    book_type = fields.Selection(
        [
            ("paper", "Paperback"),
            ("hard", "Hardcover"),
            ("electronic", "Electronic"),
            ("other", "Other")
        ],
    "Type")
    notes = fields.Text("Internal Notes")
    descr = fields.Html("Description")

    #Numeric fields
    copies = fields.Integer(default=1)
    avg_rating = fields.Float("Average Rating", (3, 2))
    price = fields.Monetary("Price", "currency_id")

    #Price helper
    currency_id = fields.Many2one("res.currency")

    #Date and time fields
    date_published = fields.Date()
    last_borrow_date = fields.Datetime(
        "Last Borrowed On",
        default = lambda self: fields.Datetime.now()
    )

    #Other fields
    active = fields.Boolean("Active?", default=True)
    image = fields.Binary("Cover")

    #Relational fields
    publisher_id = fields.Many2one("res.partner", string="Publisher")
    author_ids = fields.Many2many("res.partner", string="Authors")
    publisher_country_id = fields.Many2one(
        "res.country", string="Publisher Country",
        compute="_compute_publisher_country",
        inverse="_inverse_publisher_country",
        search="_search_publisher_country",
    )
    category_id = fields.Many2one(
        "library.book.category",
        string="Category",
        ondelete="set null"
    )

    main_category_id = fields.Many2one(
        "library.book.category",
        string="Main Category (Padre)",
        ondelete="set null"
    )


    @api.depends("publisher_id.country_id")
    def _compute_publisher_country(self):
        for book in self:
            book.publisher_country_id = book.publisher_id.country_id

    def _inverse_publisher_country(self):
        for book in self:
            book.publisher_country_id = book.publisher_id.country_id

    def _search_publisher_country(self, operator, value):
        return [
            ("publisher_id.country_id", operator, value)
        ]

    #Check if ISBN is correct
    def _check_isbn(self):
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 13:
            ponderations = [1, 3] * 6
            terms = [a * b for a, b in zip(digits[:12], ponderations)]
            remain = sum(terms) % 10
            check = 10 - remain if remain != 0 else 0
            return digits[-1] == check

    def button_check_isbn(self):
        for book in self:
            if not book.isbn:
                raise ValidationError("Please provide an ISBN for %s" %book.name)
            if book.isbn and not book._check_isbn():
                raise ValidationError("%s ISBN is invalid" %book.isbn)
        return True

    @api.constrains("isbn")
    def _constrain_isbn_valid(self):
        for book in self:
            if book.isbn and not book._check_isbn():
                raise ValidationError(
                    "%s is an invalid ISBN" % book.isbn
                )

    def _default_last_borrow_date(self):
        return fields.Datetime.now()

    last_borrow_date = fields.Datetime(
        "Last Borrowed On",
        default=_default_last_borrow_date,
    )
    
    @api.onchange('isbn')
    def _obtener_libro(self):
        for record in self:

            # Limpia el isbn de espacios a principio y a final y elimina los guiones
            new_isbn = str(record.isbn).replace('-', '').strip()

            # Variable con la url de conexión a a la API externa
            url_details = f"https://openlibrary.org/api/books?bibkeys=ISBN:{new_isbn}&jscmd=details&format=json"
            print('Buscando libro...')

            url_data = f"https://openlibrary.org/api/books?bibkeys=ISBN:{new_isbn}&jscmd=data&format=json"

            # Conexión a la API externa
            res_details = requests.get(url_details)
            res_data = requests.get(url_data)

            # Obtiene la imagen del libro (Formato Mediano)
            print("IMAGEN AQUI")

            if res_data.status_code == 200:
                data = res_data.json().get(f'ISBN:{new_isbn}', {})
                try:
                    cover = data.get('cover', {})
                    medium_image = cover.get('medium', '')
                    print("Imagen (medium):", medium_image)

                    if medium_image:
                        # Descarga la imagen
                        image_response = requests.get(medium_image)
                        if image_response.status_code == 200:
                            self.image = base64.b64encode(image_response.content)
                            print(self.image)
                        else:
                            print("No se pudo descargar la imagen:", image_response.status_code)
                    else:
                        print("No se encontró la URL de la imagen.")
                except Exception as e:
                    print("Error al procesar la imagen:", e)
            else:
                print(f"Error en la respuesta: {res_data.status_code}")



            # Si se obtiene permiso del servidor se realizan las operaciones establecidas
            if res_details.status_code == 200:
                data = res_details.json().get(f'ISBN:{new_isbn}', {})
                details = data.get('details', {})

                #Obtención del título
                record.name = details.get('title', '').upper()

                # Obtención de autores
                authors = details.get('authors', [])
                print(authors)
                Author = self.env['res.partner']
                author_ids = []

                if authors:
                    try:
                        for author in authors:
                            name = author.get('name', '')
                            if name:
                                # Busca si ya existe el autor
                                existing_author = Author.search([('name', '=', name)], limit=1)
                                if not existing_author:
                                    existing_author = Author.create({'name': name})
                                author_ids.append(existing_author.id)

                            record.author_ids = [(6, 0, author_ids)]
                    except Exception as e:
                        print("Error al procesar autores", e)
                else:
                    print("No se ha encontrado ningún autor válido en 'autors'")
                
                    

                # Obtención de Publicaciones
                publishers = details.get('publishers', [])
                print("Publishers data:", publishers)
                Publisher = self.env['res.partner']

                if publishers:
                    try:
                        publisher_id = False
                        for publisher_name in publishers:
                            name = publisher_name if isinstance(publisher_name, str) else ''
                            if name and not '':
                                existing_publisher = Publisher.search([('name', '=', name)], limit=1)
                                if not existing_publisher:
                                    existing_publisher = Publisher.create({'name': name})
                                publisher_id = existing_publisher.id
                                break  # Salir del bucle para solo coger el primer registro
                            print("Se ha encontrado un nombre:", publisher_id)
                        record.publisher_id = publisher_id
                    except Exception as e:
                        print("Error procesando publicadores", e)
                else:
                    print("No se ha encontrado un publicante válido")
                
                

                
                created = details.get("created", {})
                date_iso = created.get("value")

                if date_iso:
                    try:
                        date_iso = date_iso.replace('Z', '')
                        fecha_obj = datetime.fromisoformat(date_iso)
                        # Da formato a la fecha para que Odoo pueda procesarla en el campo published_date
                        record.date_published = fecha_obj.strftime("%Y-%m-%d")
                        print("Fecha asignada:", record.date_published)
                    except Exception as e:
                        print("Error procesando la fecha:", e)
                else:
                    print("No se encontró una fecha válida")
                
                # Hace petición a json works para obtener la categoría de los libros
                # works = details.get('works', [])
                # if works:
                #     work_key = works[0].get('key')
                #     if work_key:
                #         work_url = f"https://openlibrary.org{work_key}.json"
                #         response = requests.get(work_url)
                #         if response.status_code == 200:
                #             work_data = response.json()
                #             print(work_data)
                #             subjects = work_data.get('subjects', [])
                #             print('Categorías encontradas:', subjects)
                #             # Aquí puedes continuar con tu lógica para crear y asignar categorías
                #         else:
                #             print(f"Error al obtener los detalles del libro: {response.status_code}")
                #     else:
                #         print("No se encontró la clave del libro.")
                # else:
                #     print("No se encontraron libros relacionados.")

                #Obtiene JSON de works
                works = details.get('works', [])
                
                if works:
                    work_key = works[0].get('key')
                    
                    if work_key:
                        work_url = f"https://openlibrary.org{work_key}.json"
                        response = requests.get(work_url)
                        if response.status_code == 200:
                            work_data = response.json()

                            # Obtiene la descripción del libro
                            try:
                                description = work_data.get('description', '')
                                value = description.get('value', '')
                                print(value)
                                self.synopsis = value
                            except Exception as e:
                                print("Error al obtener la descripción del libro", e)

                            
                    else:
                        print("No se ha podido encontrar una key")

