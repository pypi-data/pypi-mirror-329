import socket
import select
import threading
from datetime import datetime
from http.server import HTTPServer
from ..utils.enums import ContentTypes
from ..utils.router import Router
from ..utils.reload_server import ReloadServer, MyHandler
from ..utils.template import Template, RequestFiles, StaticTemplate

class Server:
    def __init__(self, router: Router):
        self.__router = router
        self.__routes: dict[str, Template] = self.__router._Router__routes
        self.__connections: list[socket.socket] = []
        self.__reload: bool = False
    
    @property
    def __curr_time(self) -> str:
        return datetime.now().strftime("[%H:%M:%S]")
    
    def add_code_to_template(self, template: str) -> str:
        if self.__reload:
            template = StaticTemplate.add_reload_code(
                template=template
            )

        template = StaticTemplate.add_ping_code(
            template=template
        )

        return template
    
    def handle_ping(self, request: str) -> bytes:
        return self.serve_file(request=request, template="")
    
    def handle_static_files(self, request: str) -> bytes:
        return self.serve_file(
            request=request,
            template=RequestFiles(
                path=request.split(' ')[1][1:]
            ).read_file
        )
    
    def handle_route(self, request: str) -> bytes:
        try:
            return self.serve_file(
                request=request,
                template=self.add_code_to_template(
                    template=self.__routes[request.split(' ')[1]]._Template__render_template
                )
            )

        except KeyError:
            return self.serve_file(
                request=request,
                template=self.add_code_to_template(
                    template=StaticTemplate.error_template()
                )
            )

    def get_template(self, request: str) -> bytes:
        route: str = request.split(' ')[1]

        if route == '/ping':
            return self.handle_ping(request=request)
        
        elif '.' in route:
            return self.handle_static_files(request=request)
        
        else:
            return self.handle_route(request=request)
    
    def serve_file(self, request: str, template: str | bytes) -> bytes:
        route: str = request.split(' ')[1]
        content_type: ContentTypes = ContentTypes.html
        
        if '.' in route:
            extension: str = route.split('.')[-1].strip()

            if not template:
                response_code = "404 Not Found"
            
            else:
                response_code = "200 OK"

                try:
                    content_type = getattr(ContentTypes, extension)

                except:
                    print(f'Extensão {extension} não disponível para processamento')
        
        else:
            if route == '/ping' or route in self.__routes:
                response_code = "200 OK"
            
            else:
                response_code = "404 Not Found"
        
        file_content: str | bytes = template
        if not isinstance(file_content, bytes):
            file_content: bytes = file_content.encode()

        length: int = len(file_content)

        response: str = f"HTTP/1.1 {response_code}\r\n"
        response += f"Content-Type: {content_type.value}; charset=UTF-8\r\n"
        response += f"Content-Length: {length}\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response = response.encode() + file_content

        if '/ping' not in request:
            print(f'{self.__curr_time} - {request.split('\n')[0].strip()} {response_code}')
        
        return response

    def handle_client(self, client_socket: socket.socket) -> None:
        """Função para lidar com uma conexão recebida."""
        try:
            request: str = client_socket.recv(1024).decode()
            if request:
                response: bytes = self.get_template(request)
                client_socket.sendall(response)
        
        except BlockingIOError:
            pass

        # except Exception as e:
        #     print(f"Erro ao processar cliente: {e}")

        finally:
            if client_socket in self.__connections:
                self.__connections.remove(client_socket)
            
            client_socket.close()

    def create_server(self, host: str = 'localhost', port: int = 5555, route: str = '/') -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
            socket_server.bind((host, port))
            socket_server.listen(5)

            # Url to get the site
            url: str = f'http://{host}:{port}{route}'
            print(url)

            while True:
                try:
                    rlist, _, _ = select.select([socket_server] + self.__connections, [], [], 1)

                    for socket_client in rlist:
                        if socket_client is socket_server:
                            socket_client, _ = socket_server.accept()
                            self.__connections.append(socket_client)

                            threading.Thread(target=self.handle_client, args=(socket_client,), daemon=True).start()
                
                except Exception as e:
                    continue
                
                except KeyboardInterrupt:
                    print('Servidor deslidado')
                    break
    
    def run(self, route: str = '/', port: int = 5555, reload: bool = True):
        self.__reload = reload
        if self.__reload:
            reload_server = ReloadServer()
            server = HTTPServer(("localhost", port+1), MyHandler)
            threading.Thread(target=reload_server.run, daemon=True).start()
            threading.Thread(target=server.serve_forever, daemon=True).start()
        
        self.create_server(route=route, port=port)