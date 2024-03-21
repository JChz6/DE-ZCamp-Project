import scrapy
import datetime
today = datetime.today()


'''cities = ['puno', 'moquegua', 'arequipa']

property_types = ['departamentos']
operations = ['venta', 'alquiler']'''


cities = ['loreto','moquegua','pasco','ancash','apurimac','arequipa','ayacucho','cajamarca','callao','cusco','ica','junin','la-libertad','lambayeque','lima','piura','puno','san-martin','tacna','tumbes','ucayali',
    
'loreto-departamento/list','moquegua-departamento/list','pasco-departamento/list','ancash-departamento/list','apurimac-departamento/list','arequipa-departamento/list','ayacucho-departamento/list','cajamarca-departamento/list','callao-departamento/list','cusco-departamento/list','ica-departamento/list','junin-departamento/list','la-libertad-departamento/list',
'lambayeque-departamento/list','lima-departamento/list','piura-departamento/list','puno-departamento/list','san-martin-departamento/list',
'tacna-departamento/list','tumbes-departamento/list','ucayali-departamento/list']

property_types = ['departamentos', 'casas-playa', 'casas-condominio', 'casas', 'oficinas', 'locales-comerciales', 'residenciales', 'terrenos']
operations = ['venta', 'alquiler']

class CasaspiderSpider(scrapy.Spider):
    name = "casaspider"
    allowed_domains = ["www.laencontre.com.pe"]

    def start_requests(self):
        for city in cities:
            for ptype in property_types:
                for operation in operations:
                    url = f"https://www.laencontre.com.pe/{operation}/{ptype}/{city}"
                    yield scrapy.Request(url, callback=self.parse, meta={'city': city, 'ptype': ptype, 'operation': operation})


    def parse(self, response):
        casas = response.css('li.serp-snippet')
        if casas:
            for casa in casas:
                relative_url = casa.css('h2 a').attrib['href']
                casa_url = "https://www.laencontre.com.pe" + relative_url
                yield scrapy.Request(casa_url, callback=self.parse_casa_page, meta=response.meta)

            #nextpage***********
            
            # Gets the current page number
            current_page = int(response.url.split('_')[-1]) if '_' in response.url else 1

            # Base URL and total number of pages
            base_url = response.url.rsplit('_', 1)[0]
            total_pages = 101

            # Makes requests for the next pages
            for page_num in range(current_page + 1, current_page + total_pages + 1):
                if page_num <= total_pages:
                    next_page_url = f'{base_url}/p_{page_num}'
                    yield response.follow(next_page_url, callback=self.parse, meta=response.meta)
                else:
                    break  # Stop crawling if total number of pages is reached


    #Defines the fields to scrape, which will be the columns of the tables
    def parse_casa_page(self, response):
        city = response.meta['city']
        ptype = response.meta['ptype']
        operacion = response.meta['operation']

        yield{
            'scraped_on': today,
            'city' : city,
            'property_type' : ptype,            
            'operation' : operacion,
            'name' : response.css('h1 ::text').get(),
            'price' : response.css('div.price h2 ::text').get(),            
            'longitude_x' : response.css('button.see-map').attrib['data-x'],
            'latitude_y' : response.css('button.see-map').attrib['data-y'],
            'size_m2' : response.css('li.dimensions ::text').get(),
            'rooms' : response.css('li.bedrooms ::text').get(),
            'bathrooms' : response.css('li.bathrooms ::text').get(),
            'adress' : response.css('span.location_info  ::text').get(),
            'description' : response.css('p.long_text  ::text').extract(),
            'specs' : response.css('ul.list ::text').extract() ,
            'url' : response.url
        }
    
    def load_to_gcs(self, request, response=None, info=None):
        pass