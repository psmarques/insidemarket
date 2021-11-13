from core.models import Feriado
from core.models import Interacao

import sys

class FeriadoService:

    def processarFeriado(self, command):
        out = 'Montagem incorreta de subcomandos...'
        #/feriado add /teste Testar o Que?
        #/feriado alt /teste Testar o Que Novamente?
        #/feriado del /teste

        try:
            arr = command.split(' ')
            acao = arr[1]

            if acao.upper() == 'LST':
                out = 'Listagem:\n'
                lst = Feriado.objects.all()

                for item in lst:
                    out = out + item.nome + ' - ' + item.data.isoformat()  + '\n'

            else: 
                cmd = arr[2]
                lst = Feriado.objects.filter(nome = cmd)

            if len(lst) > 0 and acao.upper() == 'DEL':
                c = lst[0]
                c.delete()
                out = 'Ok'
            
            elif len(lst) < 1 and acao.upper() == 'ADD':
                s = command.replace(acao, '')
                s = s.replace('/fferiado', '')
                s = s.replace(cmd, '')
                s = s.replace('  ', '')
                s = s.replace(' ', '')

                o = Feriado(nome = cmd, data = s)
                o.save()
                out = 'Ok'

        except:
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}', type, value, traceback)

            out = out + ' -> 1'

        return out
