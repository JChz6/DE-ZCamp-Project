# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


'''class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass


def serialize_price(value):
    return f'£ {str(value)}'''

class BookItem(scrapy.Item):
    pass
    '''url = scrapy.Field()
    title = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    num_reviews = scrapy.Field()
    stars = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()'''

class DepaItem(scrapy.Item):
    pass
    '''titulo = scrapy.Field()
    precio = scrapy.Field()
    longitud_x = scrapy.Field()
    latitud_y = scrapy.Field()
    tamaño_m2 = scrapy.Field()
    habitaciones = scrapy.Field()
    banios = scrapy.Field()
    direccion = scrapy.Field()
    descripcion = scrapy.Field()
    caracteristicas = scrapy.Field()
    url = scrapy.Field()'''

class CasaItem(scrapy.Item):
    pass
    '''titulo = scrapy.Field()
    precio = scrapy.Field()
    longitud_x = scrapy.Field()
    latitud_y = scrapy.Field()
    tamaño_m2 = scrapy.Field()
    habitaciones = scrapy.Field()
    banios = scrapy.Field()
    direccion = scrapy.Field()
    descripcion = scrapy.Field()
    caracteristicas = scrapy.Field()
    url = scrapy.Field()'''