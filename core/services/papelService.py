
from core.models import Papel
from datetime import timezone

import datetime
import time
import requests
import sys
import json
import re

class PapelService:

    
    def recuperarPapel(self, ppapel):

        try:
            qry = Papel.objects.filter(papel = ppapel.upper())

            if len(qry) > 0:
                obj = qry[0]
                dt = datetime.datetime.now(timezone.utc)
                dt2 = dt - obj.datahora
                secs = dt2.total_seconds()
                print("\n\n\n{0} / Tempo no cache: {1}".format(obj.papel, str(secs)))

                return obj

        except:
            print('\n\n\nError ao recuperar Papel...')
            type, value, traceback = sys.exc_info()
            print('\n\n\nError: {0} {1} {2}', type, value)

        return None

    def salvarPapel(self, ppapel, ppreco, ppreco_anterior):
        try:
            dt = datetime.datetime.now()
            cmd = Papel.objects.filter(papel = ppapel.upper())
            
            if len(cmd) > 0:
                obj = cmd[0]

                obj.valor = ppreco
                obj.valor_anterior = ppreco_anterior
                obj.datahora = dt
                obj.save()

                print('\n\n\nPapel Atualizado no Cache' + obj.papel)
            else:
                obj = Papel(papel = ppapel.upper(), valor = ppreco, valor_anterior = ppreco_anterior, datahora = dt)
                obj.save()
                print('\n\n\Papel Criado no Cache' + obj.papel)

        except:
            print('\n\n\n')
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}', type, value)
            print('\n\n\n')

        return