from core.services.comandoService import ComandoCacheService
from core.handlers.Handler import AbstractHandler
from core.services.b3DadosService import b3DadosService

class PapelVariacaoHandler(AbstractHandler):

    bus: b3DadosService
    cmd: ComandoCacheService

    def handle(self, command: str, chatid: str, json_telegram: any):
        
        self.bus = b3DadosService()
        self.cmd = ComandoCacheService()

        #Saldo
        if(command.upper().startswith("/RANKING")):
            output = self.cmd.recuperarComando(command, 300)
            if(len(output) > 0):
                return output

            output = self.bus.maioresAltasBaixas()
            self.cmd.salvarComando(command, output)
            return output

        #Proximo
        return super().handle(command, chatid, json_telegram)