import requests
from core.models import Grupo
from core.constant import TOKEN
from core.constant import URLLEAVECHAT

import sys


class GrupoService:

    def salvarGrupo(self, idgrupo, nome):
        try:
            grupo = Grupo.objects.get(chat_id = idgrupo)

        except:
            grupo = Grupo(chat_id = idgrupo, nome = nome, ativo = True)
            grupo.save()

    def validarAcessoGrupo(self, pidgrupo):
        lst = Grupo.objects.filter(chat_id = pidgrupo)

        if len(lst) < 1:
            return False
        
        grp = lst[0]

        return grp.autorizado
    
    def sairGrupo(self, pidgrupo):
        url = URLLEAVECHAT.format(TOKEN)
        url = url + '&chat_id=' + pidgrupo

        print(url)

        try:
            r = requests.get(url)
            print(r)
            print(r.content)
            
            return str(r) + str(r.content)
        except:
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}'.format(type, value, traceback))
            print('{0}: {1}'.format(traceback.tb_next.tb_frame, traceback.tb_next.tb_lineno))

        return '-'
       
