# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter

from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.files import GCSFilesStore
import json
#from scrapy.http.request import Request

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


'''class CustomFileNamePipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        return [Request(x, meta={'file_name': item["file_name"]})
                for x in item.get('file_urls', [])]

    def file_path(self, request, response=None, info=None):
        return request.meta['file_name']'''

'''class GCSFilesStoreJSON(GCSFilesStore):
    CREDENTIALS = {
        "type": "service_account",
        "project_id": 'COPY FROM CREDENTIALS FILE',
        "private_key_id": "COPY FROM CREDENTIALS FILE",
        "private_key": "COPY FROM CREDENTIALS FILE",
        "client_email": "COPY FROM CREDENTIALS FILE",
        "client_id": "COPY FROM CREDENTIALS FILE",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "COPY FROM CREDENTIALS FILE"
    }
    def __init__(self, uri):
        from google.cloud import storage
        CREDENTIALS_FILE = 'E:/DE-Zoomcamp/project/credentials/tf_creds.json'  # Ruta completa al archivo de credenciales
        #with open(CREDENTIALS_FILE) as f:
            #credentials = json.load(f)
        client = storage.Client.from_service_account_info(CREDENTIALS_FILE)
        bucket, prefix = uri[5:].split('/', 1)
        self.bucket = client.bucket(bucket)
        self.prefix = prefix

class GCSFilePipeline(FilesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        super(GCSFilePipeline, self).__init__(store_uri,download_func,settings)'''


    
class CasascraperPipeline:
    pass