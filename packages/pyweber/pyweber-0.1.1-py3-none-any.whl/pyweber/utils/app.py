from ..utils.server import Server
from ..utils.router import Router

class run:
    def __init__(
        self,
        target,
        route: str = '/',
        port: int = 5555,
        reload: bool = True
    ):
        self.target = target
        self.route = route
        self.router = Router()
        self.port = port
        self.reload = reload
        self.__run()
    
    def __run(self):
        self.target(self.router)
        app = Server(router=self.router)
        app.run(route=self.route, port=self.port, reload=self.reload)