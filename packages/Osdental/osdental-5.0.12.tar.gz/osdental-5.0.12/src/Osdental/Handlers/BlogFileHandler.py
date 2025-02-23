import base64
from Osdental.BlobStorage.Storage import BlobStorage

class BlobFileHandler:

    def __init__(self):
        self.blob_storage = BlobStorage()

    async def get_file_base64(self, file_path:str, file_name:str = None, type:str = None, size:float = None, url:str = None, ext:str = None, mime_type:str = None):
        file_bytes = await self.blob_storage.get_file(file_path) 
        return {
            'name': file_name,
            'type': type,
            'size': size,
            'ext': ext,
            'base64': base64.b64encode(file_bytes).decode('utf-8'),
            'url': url,
            'mimeType': mime_type
        }