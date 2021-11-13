from core.services.comandoService import ComandoCacheService
from core.handlers.Handler import AbstractHandler
from core.services.b3DadosService import b3DadosService

class ComandoCustomHandler(AbstractHandler):

    bus: b3DadosService
    cmd: ComandoCacheService

    def handle(self, command: str, chatid: str, json_telegram: any):
        
        self.bus = b3DadosService()
        self.cmd = ComandoCacheService()

        #Cotação de Ativos - B3
        if(command.upper().startswith("/CCMD")):
            output = self.cmd.processarComandos(command)
            return output
        elif command.upper().startswith("/"):
            output = self.cmd.recuperarComandoCustom(json_telegram)
            return output

        #Proximo
        return super().handle(command, chatid, json_telegram)