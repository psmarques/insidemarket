from requests import Request, Session
from core.constant import CRYPTOKEY, CRYPTOURL, CRYPTOURL2

import requests
import json
import sys
import re

class CryptoService:

    url = CRYPTOURL
    api = CRYPTOKEY
    url2 = CRYPTOURL2


    def listar2(self, command):
        ret = ''
        try:
            lst = command.split(' ')
            dst = 'USD'

            if(len(lst) < 2 or len(lst) > 2):
                ret = 'Subcomando inválido'
                return ret

            rsp = requests.get(self.url2.format(lst[1].upper(), dst, self.api), timeout = 45)
            jrsp = json.loads(rsp.text)
            
            print(rsp.text)
            print(jrsp)

            ret += 'Papel: ' + lst[1].upper() + '\n'
            ret += 'Preço: ' + jrsp['DISPLAY']['PRICE'] + '\n'
            ret += 'Abertura: ' + jrsp['DISPLAY']['OPEN24HOUR'] + '\n'
            ret += 'Mínima: ' + jrsp['DISPLAY']['LOW24HOUR'] + '\n'
            ret += 'Máxima: ' + jrsp['DISPLAY']['HIGH24HOUR'] + '\n'
            ret += 'Variação: ' + jrsp['DISPLAY']['CHANGEPCT24HOUR'] + '%\n'
            ret += 'Volume: ' + jrsp['DISPLAY']['VOLUME24HOUR'] + ' (24h)\n'
            ret += 'Mercado: ' + jrsp['DISPLAY']['LASTMARKET'] + '\n'

        except:
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}', type, value, traceback)
            ret = 'Falha ao buscar dados'

        return ret

    def listar(self, command):
        ret = ''
        try:
            lst = command.split(' ')
            dst = 'USD'

            if(len(lst) < 2 or len(lst) > 2):
                ret = 'Subcomando inválido'
                return ret

            rsp = requests.get(self.url.format(lst[1].upper(), dst, self.api), timeout = 45)
            
            ret += 'Papel: ' + lst[1].upper() + '\n'
            ret += self.stripChars(rsp.text)

            #jrsp = json.loads(rsp.text)
            #if jrsp['Response'] == 'Success':
            #    ret += 'Preço: ' + 
            #    ret += 'Minima 30 dias: ' + 
            #    ret += 'Máxima 30 dias: ' +
            #print(jrsp)
            
            #ret += 'Preço: ' + jrsp['DISPLAY']['USD']['PRICE'] + '\n'
            #ret += 'Abertura: ' + jrsp['DISPLAY']['USD']['OPENDAY'] + '\n'
            #ret += 'Máxima: ' + jrsp['DISPLAY']['USD']['HIGHDAY'] + '\n'
            #ret += 'Mínima: ' + jrsp['DISPLAY']['USD']['LOWDAY'] + '\n'
            #ret += 'Volume: ' + jrsp['DISPLAY']['USD']['TOTALVOLUME24H'] + '\n'

            #ret = rsp.text
            #ret = lst[1] + ': ' + self.stripChars(rsp.text)

        except:
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}', type, value, traceback)
            ret = 'Falha ao buscar dados'

        return ret

    #def obterMinimaMaxima(self, jrsp, tipo):
    #    preco = ''
    #    minima = ''
    #    maxima = ''#
    #
    #    for i=0 to len(jrsp[Data]):
    #        preco = jrsp[Data][i][]


    def processarComando(self, command):

        ret = self.listar2(command)
        return ret



    def stripChars(self, data):
        p = self.striphtml(data)
        p = p.replace('\n', '')
        p = p.replace(':', ' ')
        p = p.replace('"', '')
        p = p.strip(' ')
        p = p.strip('/')
        p = p.strip('{')
        p = p.strip('}')
        
        return p

    def striphtml(self, data):
        pdata = '<td' + data
        p = re.compile(r'<.*?>')
        st = p.sub(' ', pdata)
        st = st.replace('  ', '')
        st = st.replace('&nbsp;', ' ')
        st = st.replace('\n', ' ')
        st = st.replace('  ', ' ')
        st = st.strip('/')
        st = st.replace('<td', '')
        return st