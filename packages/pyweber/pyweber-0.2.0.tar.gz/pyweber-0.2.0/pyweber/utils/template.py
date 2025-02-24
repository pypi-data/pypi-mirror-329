import os
from ..utils.enums import ContentTypes
from ..utils.static_files import PING_TEMPLATE, PAGE_NOT_FOUND_TEMPLATE, UPLOAD_CODE_TEMPLATE

class Template:
    def __init__(self, template: str):
        self.__template = template
    
    @property
    def __render_template(self):
        if self.__template.endswith('.html'):
            template_path = os.path.join('templates', self.__template)
            if os.path.exists(template_path):
                with open(template_path, 'r', encoding='utf-8') as file:
                    html = file.read()
                
                return html
            
            else:
                raise FileNotFoundError(f"Please include {self.__template} in template's folder")
        else:
            return self.__template

class StaticTemplate:
    @staticmethod
    def add_reload_code(template: str):
        return template.replace('</body>', UPLOAD_CODE_TEMPLATE)
    
    @staticmethod
    def add_ping_code(template: str):
        return template.replace('</body>', PING_TEMPLATE)
    
    @staticmethod
    def error_template() -> str:
        content = PAGE_NOT_FOUND_TEMPLATE
        return content

class RequestFiles:
    def __init__(self, path: str):
        self.path = path
        self.extention = self.path.split('.')[-1].lower().strip()
        self.content_text_types = [val.name for i, val in enumerate(ContentTypes) if i < 4]
        self.content_byte_types = [val.name for i, val in enumerate(ContentTypes) if i >= 4]
    
    @property
    def read_file(self) -> str | bytes:
        read_mode = 'r'
        enconding = 'utf-8'

        if self.extention in self.content_byte_types:
            read_mode = 'rb'
            enconding = None
        
        try:
            with open(self.path, read_mode, encoding=enconding) as file:
                return file.read()
        
        except:
            return ""