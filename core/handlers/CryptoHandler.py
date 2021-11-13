from core.handlers.Handler import AbstractHandler
from core.services.cryptoService import CryptoService

class CryptoHandler(AbstractHandler):

    bus: CryptoService

    def handle(self, command: str, chatid: str, json_telegram: any):
        
        self.bus = CryptoService()

        if(command.upper().startswith("/CRYPTO")):
            return self.bus.listar2(command)

        return super().handle(command, chatid, json_telegram)