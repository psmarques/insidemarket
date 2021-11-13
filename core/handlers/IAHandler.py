from core.services.noticiaService import NoticiaService
from core.ia.iaService import iaService
import requests
from core.services.comandoService import ComandoCacheService
from core.handlers.Handler import AbstractHandler
from core.services.b3DadosService import b3DadosService

class IAHandler(AbstractHandler):

    bus: b3DadosService
    cmd: ComandoCacheService
    iaHelp: iaService

    def handle(self, command: str, chatid: str, json_telegram: any):
        
        self.bus = b3DadosService()
        self.cmd = ComandoCacheService()
        rmsg = self.cmd.recuperarReplyMessage(json_telegram)
        txt = ''

        if len(rmsg) > 1:
            self.iaHelp = iaService()
            
            txt = '' + self.iaHelp.response(command)
            txt2 = txt.replace(' ', '')

            if(txt2 == 'ajustewin'):
                txt = b3DadosService().consultarAjuste('/ajuste')
            elif(txt2 == 'ajustewdo'):
                txt = b3DadosService().consultarAjuste('/ajuste wdo')
            elif(txt2 == 'noticias'):
                txt = NoticiaService().consultarCalendario()
        
            return txt
        
        if command.upper().startswith("/APRENDER"):
            self.iaHelp = iaService()
            
            txt = command.lower().replace('/aprender ', '')
            output = self.iaHelp.aprender(txt)

            return output

        #Proximo
        return super().handle(command, chatid, json_telegram)