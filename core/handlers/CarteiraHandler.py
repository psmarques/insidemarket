import json
from core.services.comandoService import ComandoCacheService
from core.services.carteiriaService import CarteiraService
from core.handlers.Handler import AbstractHandler

class CarteiraHandler(AbstractHandler):

    cmdBus: ComandoCacheService
    bus: CarteiraService

    def handle(self, command: str, chatid: str, json_telegram: any):

        self.cmdBus = ComandoCacheService()
        self.bus = CarteiraService()
        userFirstName = self.cmdBus.recuperarComandoUsuario(json_telegram)
        userName = self.cmdBus.recuperarComandoUserName(json_telegram)

        if command.upper().startswith("/CARTEIRA"):
            msg = self.bus.consultarCarteira(command, chatid, userFirstName, userName)
            return msg
        
        return super().handle(command, chatid, json_telegram)