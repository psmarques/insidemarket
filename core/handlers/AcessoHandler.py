
import json
from core.services.usuarioService import UsuarioService
from core.services.grupoService import GrupoService
from core.handlers.Handler import AbstractHandler


class AcessoHandler(AbstractHandler):

    grpBus: GrupoService
    usrBus: UsuarioService

    def handle(self, command: str, chatid: str, json_telegram: any):
        
        self.grpBus = GrupoService()

        if(self.grpBus.validarAcessoGrupo(chatid) != True):
            if json_telegram['message']['chat'].get('type', False):
                if json_telegram['message']['chat']['type'] == 'private':
                    self.grpBus.salvarGrupo(chatid, json_telegram['message']['chat']['username'])
                else:
                    self.grpBus.salvarGrupo(chatid, json_telegram['message']['chat']['title'])

            print("Acesso não validado {0} - {1}", chatid, command)
            return "Usuário/Grupo não autorizado!!!\nEntre em contato com o criador @psmarqu3s"

        return super().handle(command, chatid, json_telegram)