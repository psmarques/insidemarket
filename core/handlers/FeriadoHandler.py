from core.handlers.Handler import AbstractHandler
from core.services.feriadoService import FeriadoService

class FeriadoHandler(AbstractHandler):

    bus: FeriadoService

    def handle(self, command: str, chatid: str, json_telegram: any):
        
        self.bus = FeriadoService()

        if(command.upper().startswith("/FFERIADO")):
            return self.bus.processarFeriado(command)

        return super().handle(command, chatid, json_telegram)