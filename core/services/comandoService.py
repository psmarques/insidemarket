#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.services.grupoService import GrupoService
from core.models import ComandoCache
from core.models import Interacao
from core.constant import NOMEBOT

from datetime import timezone

import datetime
import time
import requests
import sys
import json
import re

class ComandoCacheService:

    def recuperarComando(self, cmd, tempoCache):

        try:
            print("qry")
            qry = ComandoCache.objects.filter(comando = cmd)
            print("qry")

            if len(qry) > 0:
                obj = qry[0]
                dt = datetime.datetime.now(timezone.utc)
                dt2 = dt - obj.datahora
                secs = dt2.total_seconds()
                print('\n\n\nTempo no cache: ' + str(secs))

                if (secs > tempoCache or (obj != None and obj.saida != None and str(obj.saida).startswith("Falha "))):
                    return ''

                return obj.saida

        except:
            print('\n\n\nError ao recuperar...')
            type, value, traceback = sys.exc_info()
            print('\n\n\nError: {0} {1} {2}'.format(type, value, traceback))

        return ''

    def salvarComando(self, cmmd, saida):
        try:
            dt = datetime.datetime.now()
            cmd = ComandoCache.objects.filter(comando = cmmd)
            
            if len(cmd) > 0:
                obj = cmd[0]
                obj.saida = saida
                obj.datahora = dt
                obj.save()
                print('\n\n\nComando Atualizado no Cache' + obj.comando)
            else:
                obj = ComandoCache(comando = cmmd, saida = saida, datahora = dt)
                obj.save()
                print('\n\n\nComando Criado no Cache' + obj.comando)

        except:
            print('\n\n\n')
            type, value, traceback = sys.exc_info()
            print('\n\n\nError: {0} {1} {2}'.format(type, value, traceback))
            print('\n\n\n')

        return

    def processarComandos(self, command):
        out = 'Montagem incorreta de subcomandos...'
        #/ccmd add /teste Testar o Que?
        #/ccmd alt /teste Testar o Que Novamente?
        #/ccmd del /teste

        try:
            arr = command.split(' ')
            acao = arr[1]
            cmd = ''

            if acao.upper() == 'LST':
                out = 'Listagem:\n'
                lst = Interacao.objects.all()

                for item in lst:
                    out = out + ' - ' + item.comando + '\n'

            else: 
                cmd = arr[2]      
                lst = Interacao.objects.filter(comando = cmd)          

            if len(lst) > 0 and acao.upper() == 'DEL':
                c = lst[0]
                c.delete()
                out = 'Ok'
            
            elif len(lst) < 1 and acao.upper() == 'ADD':
                s = command.replace(acao, '')
                s = s.replace('/ccmd', '')
                s = s.replace(cmd, '')
                s = s.replace('  ', '')
                o = Interacao(comando = cmd, saida = s.strip(), code = '.', ativo = True)
                o.save()
                out = 'Ok'

        except:
            print('\n\n\n')
            type, value, traceback = sys.exc_info()
            print('\n\n\nError: {0} {1} {2}'.format(type, value, traceback))
            print('\n\n\n')

        return out

    def recuperarComandoCustom(self, json_telegram):
        ret = 'Comando nao localizado'
        print("Buscando os comandos cadastrados")

        try:
            command = json_telegram['message']['text']

            interacao = Interacao.objects.get(comando = command, ativo = True)
            if interacao != None:
                ret = interacao.saida
            elif str(command).upper().startswith('/SSAIRGRUPO '):
                gs = GrupoService()
                s = str(command).split(' ')
                ret = gs.sairGrupo(s[1])

        except:
            type, value, traceback = sys.exc_info()
            print('\n\n\nError: {0} {1} {2}'.format(type, value, traceback.tb_frame))
        
        return ret


    def recuperarComandoEntrada(self, json_telegram):
        ret = ''

        try:
            ret = str(json_telegram['message']['new_chat_participant']['first_name'])
        except:
            ret = ''
        
        return ret

    def recuperarComandoSaida(self, json_telegram):
        ret = ''

        try:
            ret = str(json_telegram['message']['left_chat_member']['first_name'])
        except:
            ret = ''
        
        return ret

    def recuperarComandoUsuario(self, json_telegram):
        ret = ''

        try:
            ret = str(json_telegram['message']['from']['first_name'])
        except:
            ret = ''
        
        return ret

    def recuperarComandoUserName(self, json_telegram):
        ret = ''

        try:
            ret = str(json_telegram['message']['from']['username'])
        except:
            ret = ''
        
        return ret

    def recuperarChatId(self, json_telegram):
        ret = ''

        try:
            ret = json_telegram['message']['chat']['id']

        except:
            type, value, traceback = sys.exc_info()
            print('\n\n\nError: {0} {1} {2}'.format(type, value, traceback))

        return ret


    def recuperarChatType(self, json_telegram):
        ret = ''

        try:
            ret = json_telegram['message']['chat']['type']
        except:
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}', type, value, traceback)

        return ret


    def recuperarChatCommand(self, json_telegram):
        ret = ''

        try:
            ret = json_telegram['message']['text']
            ret = ret.replace("@jjarvisb3_bot ", "")
            ret = ret.replace("@insidemarket ", "")
            ret = ret.replace("@jjarvisb3_bot", "")
            ret = ret.replace("@insidemarket", "")
        except:
            type, value, traceback = sys.exc_info()
            print('\n\n\nError: {0} {1} {2}'.format(type, value, traceback))

        return ret


    def recuperarReplyMessage(self, json_telegram):
        ret = ''
        msg = ''

        try:
            msg = json_telegram['message']['text']
            
            if json_telegram['message'].get('reply_to_message', False):
                fr = json_telegram['message']['reply_to_message']['from']['username']
            else:
                fr = ''

            if fr == 'insidemarket_bot' or fr == 'jjarvisb3_bot' or fr == 'garcomb3_bot':
                ret = msg

        except:
            type, value, traceback = sys.exc_info()
            print('\n\n\nError: {0} {1} {2}'.format(type, value, traceback))

        if msg.lower().startswith('garcom ') or msg.lower().startswith('garçom ') or msg.lower().startswith('garcom, ') or msg.lower().startswith('garçom, '):
            return msg
        

        return ret
