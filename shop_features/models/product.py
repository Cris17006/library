from odoo import api, fields, models
import logging
import unicodedata
import base64
import requests
import time
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

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

class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    # Sobrescribimos el método create para validar antes de crear
    @api.model
    def create(self, vals):
        # Validar productos duplicados en la base de datos
        if 'name' in vals:
            producto_existente = self.env['product.template'].search([('name', '=', vals['name'])], limit=1)
            if producto_existente:
                raise UserError(f"El producto '{vals['name']}' ya existe en la base de datos. No se creará un duplicado.")
        return super(ProductTemplate, self).create(vals)
    
    def generate_product(self):
        # Genera información del producto a través de una API externa, en este caso una fake shop api 
        for record in self:
                    
            # Generamos el slug para la API
            slug = quitar_acentos(record.name.strip().lower().replace(' ', '-'))
            url_product = f'https://api.escuelajs.co/api/v1/products/slug/{slug}'
            
            try:
                # Realizamos la consulta a la API externa
                response = requests.get(url_product, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
                
                # Si no se encuentra el producto en la API se lanza un error
                if response.status_code == 404:
                    raise UserError(f"El producto '{record.name}' no existe en la base de datos externa. Slug: {slug}")
                
                # Si hay otro error HTTP que no sea 200 salta un error
                if response.status_code != 200:
                    raise UserError(f"Error al buscar el producto. Código de respuesta: {response.status_code}")
                
                # Se obtiene el json
                data = response.json()
                
                # Verificar si la respuesta está vacía o no contiene datos
                if not data:
                    raise UserError(f"No se encontraron datos para el producto '{record.name}'")
                
                # Generar la descripción del producto
                record.description_sale = data.get('description', '')
                
                # Actualizar precio si existe (Con margen de beneficio)
                if 'price' in data:
                    record.list_price = float(data.get('price', 0.0)) * 1.4
                    record.standard_price = float(data.get('price', 0.0))

                if 'description' in data:
                    record.description = data.get('description', '')
                
                # Procesar imagen si existe
                images = data.get('images', [])
                if images and isinstance(images, list):
                    image_url = images[0]  # Tomamos la primera imagen
                    imagen_bytes = obtener_imagen(image_url)
                    if imagen_bytes:
                        record.image_1920 = base64.b64encode(imagen_bytes)
                        _logger.info("Imagen del producto cargada correctamente.")
                    else:
                        _logger.warning("No se pudo obtener la imagen del producto.")
                else:
                    _logger.warning("El producto no contiene imágenes.")

                if 'category' in data:
                    details = data.get('category', {})
                    categ_name = details.get('name', '')
                    
                    # Buscar o crear la categoría padre
                    parent_category = self.env['product.category'].search([('name', '=', 'All')], limit=1)
                    if not parent_category:
                        parent_category = self.env['product.category'].create({'name': 'All'})

                    # Buscar o crear la subcategoría
                    category = self.env['product.category'].search([
                        ('name', '=', categ_name),
                        ('parent_id', '=', parent_category.id)
                    ], limit=1)

                    if not category:
                        category = self.env['product.category'].create({
                            'name': categ_name,
                            'parent_id': parent_category.id
                        })

                    # Asignar la categoría al registro
                    record.categ_id = category


                    
            except requests.exceptions.RequestException as e:
                # Error de conexión
                raise UserError(f"Error de conexión al consultar la API: {e}")
            except Exception as e:
                # Cualquier otro error
                _logger.error(f"Error al consultar la API para el producto '{slug}': {e}")
                raise UserError(f"Error al procesar el producto '{record.name}': {str(e)}")