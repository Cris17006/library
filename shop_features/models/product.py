from odoo import api, fields, models
import logging
import unicodedata
import base64
import requests
import time
import re
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
_key = "z5s6ww3mepk2z3l4fx7pi4bfcemp1u"

class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    
    # Se sobreescribe el método create para validar antes de crear
    @api.model
    def create(self, vals):
        # Validar productos duplicados en la base de datos
        if 'name' in vals and vals['name']:
            producto_existente = self.env['product.template'].search([('name', '=', vals['name'])], limit=1)
            if producto_existente:
                raise UserError(f"El producto ya existe en la base de datos. No se creará un duplicado.")
        return super(ProductTemplate, self).create(vals)

    @api.onchange('barcode')
    def _generate_product(self):
        if not self.name:

            for record in self:
                if not record.barcode:
                    continue

                barcode = record.barcode
                url_product = f'https://api.barcodelookup.com/v3/products?barcode={barcode}&formatted=y&key={_key}'
                _logger.info(f"Consultando API con URL: {url_product}")

                
                try:
                    response = requests.get(url_product, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
                    _logger.info(f"Status code recibido: {response.status_code}")

                    
                    if response.status_code == 404:
                        raise UserError(f"El producto con código de barras '{record.barcode}' no existe en la base de datos externa.")
                    if response.status_code != 200:
                        raise UserError(f"Error al buscar el producto. Código de respuesta: {response.status_code}")

                    data = response.json()
                    if not data or not data.get('products'):
                        raise UserError(f"No se encontraron datos para el producto con código de barras '{record.barcode}'")

                    
                    product_data = data.get('products', [{}])[0]

                    # Asignar nombre y descripción
                    record.name = product_data.get('title', '')
                    record.description_sale = product_data.get('description', '')
                    record.description = product_data.get('description', '')

                    # Asignar precios
                    try:
                        price = float(product_data.get('price', 0.0))
                        record.list_price = price * 1.4
                        record.standard_price = price
                    except (ValueError, TypeError):
                        _logger.warning(f"No se pudo convertir el precio: {product_data.get('price')}")

                    # Asignar imagen
                    images = product_data.get('images', [])
                    if images and isinstance(images, list):
                        image_url = images[0]
                        imagen_bytes = obtener_imagen(image_url)
                        if imagen_bytes:
                            record.image_1920 = base64.b64encode(imagen_bytes)
                            _logger.info("Imagen cargada correctamente.")
                        else:
                            _logger.warning("No se pudo obtener la imagen.")
                    else:
                        _logger.warning("El producto no contiene imágenes.")

                    # Asignar categorías
                    category_path = product_data.get('category', '')
                    category_names = [cat.strip() for cat in category_path.split('>') if cat.strip()]
                    parent_category = None

                    for name in category_names:
                        category = self.env['product.category'].search([
                            ('name', '=', name),
                            ('parent_id', '=', parent_category.id if parent_category else False)
                        ], limit=1)

                        if not category:
                            category = self.env['product.category'].create({
                                'name': name,
                                'parent_id': parent_category.id if parent_category else False
                            })

                        parent_category = category

                    # Asignar la categoría final al producto
                    if parent_category:
                        record.categ_id = parent_category

                    # Asignar código de referencia
                    if not record.default_code:
                        count = 0
                        first_char_categ = record.categ_id.name[0] if record.categ_id else 'X'
                        first_char_name = record.name[0] if record.name else 'Y'
                        code = first_char_categ + first_char_name + "-" + str(count)

                        exists = self.env["product.template"].search([('default_code', '=', code)])
                        if exists:
                            obtain_code = exists.default_code
                            count = int(re.sub(r'\D', '', obtain_code))
                            count += 1
                            record.default_code = f"{first_char_categ}{first_char_name}-{count}"
                        else:
                            record.default_code = code
                    else:
                        _logger.info(f"El producto ya tiene código de referencia: {record.default_code}")
                    
                   # Asignar precio de coste (solo de tiendas en EUR)
                    precio_minimo = 0.0
                    stores = product_data.get('stores', [])

                    # Filtramos precios válidos y que estén en euros
                    precios_eur = [
                        float(store.get('price')) for store in stores
                        if store.get('price') and (store.get('currency') == 'EUR')
                    ]

                    if precios_eur:
                        precio_minimo = min(precios_eur)
                        record.standard_price = precio_minimo

                        # Asignar precio de venta con margen del 60%
                        record.list_price = round(precio_minimo * 1.6, 2)

                        

                except requests.exceptions.RequestException as e:
                    _logger.error(f"Error de conexión: {str(e)}")
                    raise UserError(f"Error de conexión al buscar el producto: {str(e)}")
                except Exception as e:
                    _logger.error(f"Error inesperado: {str(e)}")
                    raise UserError(f"Error inesperado al procesar el producto: {str(e)}")
                    

def quitar_acentos(texto):
    # Elimina acentos del texto para normalizar URLs o búsquedas.
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')

def obtener_imagen(url, max_reintentos=5):
    # Descarga la imagen desde una URL
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    espera = 1
    for intento in range(max_reintentos):
        try:
            respuesta = session.get(url, allow_redirects=True, timeout=10)
            if respuesta.status_code == 200:
                return respuesta.content
            elif respuesta.status_code == 429:
                _logger.warning(f"[{intento+1}] Demasiadas solicitudes. Esperando {espera}s antes de reintentar...")
                time.sleep(espera)
                espera *= 2
            else:
                _logger.error(f"Error {respuesta.status_code} al obtener la imagen desde {url}")
                break
        except requests.RequestException as e:
            _logger.error(f"Error de red al obtener imagen: {e}")
            time.sleep(espera)
            espera *= 2
    return None