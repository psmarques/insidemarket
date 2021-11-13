from core.services.comandoService import ComandoCacheService
from core.services.noticiaService import NoticiaService
from core.handlers.Handler import AbstractHandler
from core.services.noticiaService import NoticiaService

class NoticiasHandler(AbstractHandler):

    bus: NoticiaService
    cmd: ComandoCacheService

    def handle(self, command: str, chatid: str, json_telegram: any):
        
        self.bus = NoticiaService()
        self.cmd = ComandoCacheService()

        if(command.upper().startswith("/NOTICIA") or command.upper().startswith("/CALENDARIO") or command.upper().startswith("/CALENDÁRIO")):
            output = self.cmd.recuperarComando(command, 900)
            if(len(output) > 0):
                return output

            output = self.bus.consultarCalendario()
            self.cmd.salvarComando(command, output)
            return output

        return super().handle(command, chatid, json_telegram)