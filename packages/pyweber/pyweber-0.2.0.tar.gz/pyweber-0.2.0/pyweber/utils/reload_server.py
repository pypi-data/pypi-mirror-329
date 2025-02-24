import websockets
import threading
import asyncio
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ReloadServer:
    def __init__(self, port: int = 5555, event = None):
        self.__websocket_clients: set[websockets.WebSocketClientProtocol] = set()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.port = port
        self.event = event
    
    async def send_reload(self):
        if self.__websocket_clients:
            for client in self.__websocket_clients:
                try:
                    if client.open:
                        await client.send('reload')
                    
                    else:
                        print("Conexão WebSocket fechada, não foi possível enviar reload.")
                
                except Exception as e:
                    print(f'Erro ao enviar reload para o cliente: {e}')
    
    async def websocket_handler(self, websocket: websockets.WebSocketClientProtocol, _):
        self.__websocket_clients.add(websocket)

        try:
            await websocket.wait_closed()
        
        finally:
            self.__websocket_clients.remove(websocket)
    
    async def start(self, host: str = 'localhost', port: int = 8765):
        try:
            server = await websockets.serve(self.websocket_handler, host, port)
            await server.wait_closed()
        
        except:
            pass
    
    def run(self, host: str = 'localhost', port: int = 8765):
        server_thread = threading.Thread(target=self.loop.run_until_complete, args=(self.start(host, port),))
        server_thread.daemon = True
        server_thread.start()

        watchdog = WatchdogFiles(self)
        asyncio.run(watchdog.start())

class WatchdogFiles:
    def __init__(self, reload_server: ReloadServer):
        self.event_handler = ReloadHandler(reload_server)
        self.observer = Observer()
    
    async def start(self):
        self.observer.schedule(self.event_handler, path='.', recursive=True)
        self.observer.start()

        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, reload_server: ReloadServer):
        self.__file_extensions: list[str] = ['.py', '.html', '.css', '.js']
        self.__reload_server = reload_server
        self.last_time = 0

    def on_modified(self, event):
        if any(event.src_path.endswith(ext) for ext in self.__file_extensions):

            if time.time() - self.last_time > 1:
                if event.src_path.endswith('.py'):
                    print("♻️ Reiniciando servidor...")
                    self.__reload_server.event()
                
            asyncio.run(self.__reload_server.send_reload())
            self.last_time = time.time()