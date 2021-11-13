from core.services.RequestService import RequestService
from core.services.comandoService import ComandoCacheService
from core.handlers.Handler import AbstractHandler
from core.services.b3DadosService import b3DadosService
from datetime import datetime

class PapelHandler(AbstractHandler):

    bus: b3DadosService
    cmd: ComandoCacheService

    def handle(self, command: str, chatid: str, json_telegram: any):
        
        self.bus = b3DadosService()
        self.cmd = ComandoCacheService()

        #Cotação de Ativos - B3
        if(command.upper().startswith("/COTACAO ") or command.upper().startswith("/COTAÇÃO ")):
            output = self.cmd.recuperarComando(command, 300)
            if(len(output) > 0):
                return output

            output = self.bus.consultarAtivoB3(command)
            self.cmd.salvarComando(command, output)
            return output
        
        elif(command.upper().startswith('/DIVIDENDOS')):
            output = self.bus.dividendos(command)
            return output

        elif(command.upper().startswith("/GRAFICO ") or command.upper().startswith("/GRÁFICO ")):
            atv = command.upper().replace("/GRAFICO ", "").replace("/GRÁFICO ", "")
            buf = self.bus.gerarGrafico(atv)
            RequestService().sendImageBinary(chatid, buf)
            return None

        elif(command.upper().startswith("/GRAFICOADR ")):
            atv = command.upper().replace("/GRAFICOADR ", "")
            RequestService().sendImageUrl(chatid, 'https://stockcharts.com/c-sc/sc?s={0}&p=D&b=5&g=0&i=t0002165039c&r={1}'.format(atv, datetime.now().timestamp() ))
            return None

        #ADR e Outros
        elif(command.upper().startswith("/ADR ")):
            return self.bus.consultarAdr(command)

        #Proximo
        return super().handle(command, chatid, json_telegram)