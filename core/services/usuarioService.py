from core.models import UsuarioChat
from core.models import BlackList

import sys

class UsuarioService:

    def processarBlackList(self, command):
        out = 'Montagem incorreta de subcomandos...'
        #/feriado add /teste Testar o Que?
        #/feriado alt /teste Testar o Que Novamente?
        #/feriado del /teste

        try:
            arr = command.split(' ')
            acao = arr[1]

            if acao.upper() == 'LST':
                out = 'Listagem:\n'
                lst = BlackList.objects.all()

                for item in lst:
                    out = out + item.nome + ' - ' + item.usuarioid + '\n'

            else: 
                cmd = arr[2]
                lst = BlackList.objects.filter(nome = cmd)

            if len(lst) > 0 and acao.upper() == 'DEL':
                c = lst[0]
                c.delete()
                out = 'Ok'
            
            elif len(lst) < 1 and acao.upper() == 'ADD':
                s = command.replace(acao, '')
                s = s.replace('/iignorar', '')
                s = s.replace(cmd, '')
                s = s.replace('  ', '')
                s = s.replace(' ', '')

                o = BlackList(nome = cmd, usuarioid = s)
                o.save()
                out = 'Ok'

        except:
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}', type, value, traceback)

            out = out + ' -> 1'

        return out


    def processarUsuario(self, command):
        out = 'Montagem incorreta de subcomandos...'
        #/feriado add /teste Testar o Que?
        #/feriado alt /teste Testar o Que Novamente?
        #/feriado del /teste

        try:
            arr = command.split(' ')
            acao = arr[1]

            if acao.upper() == 'LST':
                out = 'Listagem:\n'
                lst = UsuarioChat.objects.all()

                for item in lst:
                    out = out + item.usuario + ' - ' + item.usuario_id  + '\n'

            else: 
                cmd = arr[2]
                lst = UsuarioChat.objects.filter(usuario = cmd)

            if len(lst) > 0 and acao.upper() == 'DEL':
                c = lst[0]
                c.delete()
                out = 'Ok'
            
            elif len(lst) < 1 and acao.upper() == 'ADD':
                s = command.replace(acao, '')
                s = s.replace('/uusario', '')
                s = s.replace(cmd, '')
                s = s.replace('  ', '')
                s = s.replace(' ', '')

                o = UsuarioChat(usuario = cmd, usuario_id = s)
                o.save()
                out = 'Ok'

        except:
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}', type, value, traceback)

            out = out + ' -> 1'

        return out


    def salvarUsuario(self, idusuario, nome):
        try:
            usu = UsuarioChat.objects.get(usuario_id = idusuario)

        except:
            usu = UsuarioChat(usuario = nome, usuario_id = idusuario)
            usu.save()


    def validarUsuario(self, pidgrupo):
        lst = BlackList.objects.filter(usuarioid = pidgrupo)

        if len(lst) > 0:
            return False

        return True