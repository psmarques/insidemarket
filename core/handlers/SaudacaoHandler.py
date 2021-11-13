from core.services.usuarioService import UsuarioService
from core.services.grupoService import GrupoService
from core.services.comandoService import ComandoCacheService
from core.services.saudacaoService import SaudacaoService
from core.handlers.Handler import AbstractHandler

class SaudacaoHandler(AbstractHandler):

    cmdBus: ComandoCacheService
    saudacao: SaudacaoService

    def handle(self, command: str, chatid: str, json_telegram: any):

        self.cmdBus = ComandoCacheService()
        self.saudacao = SaudacaoService()

        newmember = self.cmdBus.recuperarComandoEntrada(json_telegram)
        leftmember = self.cmdBus.recuperarComandoSaida(json_telegram)
        
        if len(newmember) > 0 or len(leftmember) > 0:
            msg = self.saudacao.saudar(newmember, leftmember)
            return msg
        
        return super().handle(command, chatid, json_telegram)


    # def ValidarMensagemEvento(json_telegram, command, chatid, chattype, userFirstName, userName):
    #         cmdBus = ComandoCacheBus()
    #         newmember = cmdBus.recuperarComandoEntrada(json_telegram)
    #         leftmember = cmdBus.recuperarComandoSaida(json_telegram)

    #         #print(json_telegram)

    #         if len(newmember) > 0 or len(leftmember) > 0:
    #             msg = SaudacaoBus().saudar(newmember, leftmember)
    #             send(chatid, msg)
    #             return 1
            
    #         if command.startswith('/') == False:
    #             return 1

    #         #setar o chat no grupo ou privado
    #         if chattype == 'group' or chattype == 'supergroup':
    #             chatid = json_telegram['message']['chat']['id']
    #             title = json_telegram['message']['chat']['title']
    #             GrupoBus().salvarGrupo(chatid, title)

    #         if len(userFirstName) > 0:
    #             UsuarioBus().salvarUsuario(userName, userFirstName)
            
    #         return 0