import datetime
import io
import time
import requests
import sys
import json
import re
import string
import yfinance as yf
import pandas as pd
import mplfinance as mpf

from core.constant import URLAJUSTEB3
from core.constant import URLATIVOB3
from core.constant import URLVARIACAOB3
from core.constant import URLVARIACAOVOLB3
from pprint import pprint

from core.models import Papel

from datetime import timezone

class b3DadosService:

    papelAtual: Papel

    def maioresVol(self):
        ret = ''
        try:

            con = requests.get(URLVARIACAOVOLB3, timeout=45)
        
            jtxt = json.loads(con.text)
            atualizacao = jtxt['Msg']['dtTm']
            
            ret += "Mais Negociadas:\n"
            for item in jtxt['Volume']:
                ret += item['scty']['symb'] + " R$ " + ("{0:.2f}".format(float(item['pricVal']))) + " / Vol: " + self.human_format(item['grossAmt']) + "\n"

            ret += "Atualizacao: " + atualizacao

        except:
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}', type, value, traceback)

            ret = 'Falha ao buscar Dados...'

        return ret

    def maioresAltasBaixas(self):
        ret = ''
        try:

            con = requests.get(URLVARIACAOB3, timeout=45)
        
            jtxt = json.loads(con.text)
            atualizacao = jtxt['Msg']['dtTm']
            
            ret += "Maiores Altas:\n"
            for item in jtxt['SctyHghstIncrLst']:
                ret += item['symb'] + " " + ("{0:.2f}".format(float(item['SctyQtn']['prcFlcn']))) + "% / R$ " + str(item['SctyQtn']['curPrc']) + "\n"

            ret += "\nMaiores Baixas:\n"
            for item in jtxt['SctyHghstDrpLst']:
                ret += item['symb'] + " " + ("{0:.2f}".format(float(item['SctyQtn']['prcFlcn']))) + "% / R$ " + str(item['SctyQtn']['curPrc']) + "\n"


            ret += "Atualizacao: " + atualizacao

        except:
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}', type, value, traceback)

            ret = 'Falha ao buscar Dados...'

        return ret
    
    def consultarAjuste(self, command):
        ret = 'Falha ao buscar os dados'
        try:

            atv = command.upper().replace('/AJUSTE ', '')
            con = requests.get(URLAJUSTEB3, timeout=45)
            
            if atv.startswith('WDO'): 
                atv = 'WDO'
            elif atv.startswith('WIN'):
                atv = 'WIN'
            elif atv.startswith('BGI'):
                atv = 'BGI'
            elif atv.startswith('CCM'):
                atv = 'CCM'
            elif atv.startswith('IND'):
                atv = 'IND'
            elif atv.startswith('DOL'):
                atv = 'DOL'
            else:
                atv = 'WIN'
            
            st = con.text.split('<td')
            achou = False

            ix = 0
            texto = '==> '
            textoLinha1 = 'Codigo: '
            textoLinha2 = 'Ajuste Atual: '
            textoLinha3 = 'Ajuste Ant.: '
            textoLinha4 = 'Variacao: '

            for x in st:
                if ix == 10:
                    achou = False
                    break

                if x.find(atv) >= 0:
                    achou = True
                    t = x.replace('align="center">', '')
                    t = t.replace('  ', '')
                    t = t.replace('</td>', '')
                    t = t.replace('>', '')
                    t = t.replace('<td>', '')
                    t = t.replace('<td', '')
                    texto = texto + t + '\n'
                    continue
                
                if achou:
                    ix = ix + 1
                    t = x.replace(' align="right">','')
                    t = t.replace(' align="center">', '')
                    t = t.replace('</td>', '')
                    t = t.replace('<tr class="tabelaCounteudo2" >', '')
                    t = t.replace('>', '')
                    t = t.replace('<td', '')
                    
                    if ix == 1 or ix == 7:
                        textoLinha1 = textoLinha1 + t + ' / '
                    elif ix == 2 or ix == 8:
                        textoLinha3 = textoLinha3 + t + ' / '
                    elif ix == 3 or ix == 9:
                        textoLinha2 = textoLinha2 + t + ' / '
                    elif ix == 4 or ix == 10:
                        textoLinha4 = textoLinha4 + t + ' / '

            ret = self.stripChars(texto) + '\n' + self.stripChars(textoLinha1) + '\n' + self.stripChars(textoLinha2) + '\n' + self.stripChars(textoLinha3) + '\n' + self.stripChars(textoLinha4)

        except:
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}', type, value)
            ret = "Falha ao buscar dados"
        
        return ret

    def consultarAtivoB3(self, ativo):   
        ret = 'Falha ao buscar dados'
        hdrs = {"Referer":"https://www.msn.com/pt-br/dinheiro/stockdetails/fi-apnhoc", "Origin":"https://www.msn.com", "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36" }

        try:
            lst = ativo.split(' ')
            
            if len(lst) < 2:
                return 'Comando faltando o parametro'

            atv = lst[1]
            url = URLATIVOB3.format(atv.upper())
            
            if atv.upper() == 'IBOV':
                url = url.replace('56.1.IBOV.BSP', '56.10.IBOV')

            if atv.upper() == 'BOVA11':
                url = url.replace('56.1.BOVA11.BSP', '56.8.BOVA11')

            if atv.upper() == 'SPX':
                url = url.replace('56.1.SPX.BSP', 'spx')

            con = requests.get(url, timeout = 45, headers = hdrs)
            j = json.loads(con.text)

            ret = 'Papel: ' + j[0]['Quotes']['Eqsm'] + '\n'

            if atv.upper() == 'IBOV' or atv.upper() == 'BOVA11' or atv.upper() == 'SPX':
                ret = ret + 'Preco: ' + str(j[0]['Quotes']['Lp']) + '\n'
                ret = ret + 'Fech Ant: ' + str(j[0]['Quotes']['Pp']) + '\n'
                ret = ret + 'Variacao: ' + ("{0:.2f}".format(float(j[0]['Quotes']['Chp']))) + '%' + '\n'
                ret = ret + 'Variacao 1 Mes: ' + ("{0:.2f}".format(float(j[0]['Quotes']['PrCh1Mo']) / 1000)) + '%' + '\n'
                ret = ret + 'Variacao 3 Meses: ' + ("{0:.2f}".format(float(j[0]['Quotes']['PrCh3Mo']) / 1000)) + '%' + '\n'
                ret = ret + 'Variacao 6 Meses: ' + ("{0:.2f}".format(float(j[0]['Quotes']['PrCh6Mo']) / 1000)) + '%' + '\n'
                    
            else:
                ret = ret + 'Empresa: ' + j[0]['Quotes']['ShtName'] + '\n'
                ret = ret + 'Preco: R$ ' + str(j[0]['Quotes']['Lp']) + '\n'
                ret = ret + 'Fech Ant: R$ ' + str(j[0]['Quotes']['Pp']) + '\n'
                ret = ret + 'Max/Min: R$ ' + str(j[0]['Quotes']['Dh']) + ' / ' + str(j[0]['Quotes']['Dl']) + '\n'
                #ret = ret + 'Min: R$ ' + str(j[0]['Quotes']['Dl']) + '\n'
                ret = ret + 'Variacao: ' + ("{0:.2f}".format(float(j[0]['Quotes']['Chp']))) + '%' + '\n'
                ret = ret + 'Variacao 1 Mes: ' + ("{0:.2f}".format(float(j[0]['Quotes']['PrCh1Mo']))) + '%' + '\n'
                ret = ret + 'Variacao 3 Meses: ' + ("{0:.2f}".format(float(j[0]['Quotes']['PrCh3Mo']))) + '%' + '\n'
                ret = ret + 'Variacao 6 Meses: ' + ("{0:.2f}".format(float(j[0]['Quotes']['PrCh6Mo']))) + '%' + '\n'
                #ret = ret + 'Volume Med: ' + self.human_format(j[0]['Quotes']['V']) + '\n'

            ret = ret + 'Atualizacao: ' + str(j[0]['Quotes']['Ld']) + ' ' + str(j[0]['Quotes']['Lt'])

            self.salvarPapel(j[0]['Quotes']['Eqsm'], j[0]['Quotes']['Lp'], j[0]['Quotes']['Pp'], j[0]['Quotes']['Dh'], j[0]['Quotes']['Dl'])
            
            #se o papel mudou o ticker
            if(atv != j[0]['Quotes']['Eqsm']):
                self.salvarPapel(atv, j[0]['Quotes']['Lp'], j[0]['Quotes']['Pp'], j[0]['Quotes']['Dh'], j[0]['Quotes']['Dl'])

            self.papelAtual = Papel()
            self.papelAtual.valor = j[0]['Quotes']['Lp']
            self.papelAtual.valor_anterior = j[0]['Quotes']['Pp']
            self.papelAtual.valor_maxima = j[0]['Quotes']['Dh']
            self.papelAtual.valor_minima = j[0]['Quotes']['Dl']

        except:
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}', type, value)

        return ret

    def consultarAdr(self, ativo):   
        op = 'Falha ao buscar dados'
        hdrs = {"Referer":"https://www.msn.com/pt-br/dinheiro/stockdetails/fi-apnhoc", "Origin":"https://www.msn.com", "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36" }
        #print('---> Consultar Ativo: ' + ativo)

        try:
            atv = ativo.split(' ')[1]
            uurl = URLATIVOB3.replace('symbols=56.1.{0}.BSP', 'symbols=126.1.{0}.NYS')
            con = requests.get(uurl.format(atv.upper()), timeout = 45, headers = hdrs)

            j = json.loads(con.text)

            p1 = j[0]['Quotes']['Lp']
            p2 = j[0]['Quotes']['Pp']

            variacao = (p1/p2-1)*100

            op =      'Papel: ' + j[0]['Quotes']['Sym'] + '\n'
            op = op + 'Empresa: ' + j[0]['Quotes']['Cmp'] + '\n'
            op = op + 'Preco: ' + str(j[0]['Quotes']['Lp']) + '\n'
            op = op + 'Fech Ant: ' + str(j[0]['Quotes']['Pp']) + '\n'
            op = op + 'Max/Min: ' + str(j[0]['Quotes']['Dh']) + ' / ' + str(j[0]['Quotes']['Dl']) + '\n'
            op = op + 'Variacao: ' + ("{0:.2f}".format(float(j[0]['Quotes']['Chp']))) + '%' + '\n'
            op = op + 'Variacao 1 Mes: ' + ("{0:.2f}".format(float(j[0]['Quotes']['PrCh1Mo']))) + '%' + '\n'
            op = op + 'Variacao 3 Meses: ' + ("{0:.2f}".format(float(j[0]['Quotes']['PrCh3Mo']))) + '%' + '\n'
            op = op + 'Variacao 6 Meses: ' + ("{0:.2f}".format(float(j[0]['Quotes']['PrCh6Mo']))) + '%' + '\n'
            op = op + 'Atualizacao: ' + str(j[0]['Quotes']['Ld'])

        except:
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}'.format(type, value, traceback))

        return op

    def consultarSaldo(self):
        ret = 'IBOV (C)Qtd Perc / (V)Qtd Perc\n'
        try:

            con = requests.get("http://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-tipo-de-participante-ptBR.asp", timeout=45)
        
            txt = con.text
            ix = txt.index('MERCADO FUTURO DE IBOVESPA')

            ibov = txt[ix:]
            ix2 = ibov.index('Total Geral')
            nt = ibov[0:ix2]
            nt = nt.replace('</tr>', '--')
            #nt = nt.replace('</td>', '::')
            #nt = nt.replace('<td class="text-right">', '++')
            nt = nt.replace('  ', '')
            nt = nt.replace('<strong>', '((')
            nt = nt.replace('<TR>', '))')

            nt = self.striphtml(nt)
            nt = nt.replace('))', "\n")
            nt = nt.replace("((", "")
            nt = nt.replace("\t", "")
            nt = nt.replace('--', '')
            nt = nt.replace('  ', ' ')
            #nt = nt.replace('Contratos', '')
            #nt = nt.replace('Compra', '')
            #nt = nt.replace('Venda', '')
            #nt = nt.replace('%', '')
            #nt = nt.replace("Pessoa Jurídica Financeira", "\nPJ F: ")
            #nt = nt.replace(" Bancos", "Banc: ")
            #nt = nt.replace(" DTVM'S e Corretoras de Valores", "Corr:")
            #nt = nt.replace(" Investidor Institucional", "NAC: ")
            #nt = nt.replace(" Invest. Institucional Nacional", "NAC:")
            #nt = nt.replace(" Investidores Não Residente", "GRNG:")
            #nt = nt.replace(" Inv. Não Residente - Res", "GRNG")
            #nt = nt.replace(" Pessoa Jurídica Não Financeira", "PJ NF:")
            #nt = nt.replace(" Pessoa Física", "PF:")
            #nt = nt.replace("GRNG.2689", "GRNG: ")
            nt = nt.replace(":s", ":")
            nt = nt.replace('  ', '')
            nt = nt.strip()
            nt = nt.rstrip()
            nt = nt.lstrip()
            nt = nt.replace("  ", " ")

            print(nt)
            #ibov = self.striphtml(nt)

            ret += self.removeDuplicate(nt)

        except:
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}', type, value, traceback)

            ret = 'Falha ao buscar Dados...'

        return ret

    def recuperarPapel(self, ppapel):
            
            cmd = Papel.objects.filter(papel = ppapel.upper())
            
            if len(cmd) > 0:
                obj = cmd[0]
                return obj

            return None

    def salvarPapel(self, ppapel, ppreco, ppreco_anterior, vvalor_maxima, vvalor_minima):
        try:
            dt = datetime.datetime.now()
            cmd = Papel.objects.filter(papel = ppapel.upper())
            
            if len(cmd) > 0:
                obj = cmd[0]

                obj.valor = ppreco
                obj.valor_anterior = ppreco_anterior
                obj.valor_maxima = vvalor_maxima
                obj.valor_minima = vvalor_minima
                obj.datahora = dt
                obj.save()

                print('\n\n\nPapel Atualizado no Cache' + obj.papel)
            else:
                obj = Papel(papel = ppapel.upper(), valor = ppreco, valor_anterior = ppreco_anterior, valor_maxima = vvalor_maxima, valor_minima = vvalor_minima, datahora = dt)
                obj.save()
                print('\n\n\Papel Criado no Cache' + obj.papel)

        except:
            print('\n\n\n')
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}', type, value, traceback)
            print('\n\n\n')

        return

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
    
    def stripChars(self, data):
        
        p = self.striphtml(data)
        p = p.replace('\n', '')
        p = p.strip(' ')
        p = p.strip('/')

        return p

    def removeDuplicate(self, text):
        lines = ''

        for item in text.split("\n"):
            if lines.find(item) < 1:
                lines += item + "\n"
        
        return lines

    def human_format(self, num):
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0

        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'k', 'm', 'b', 't'][magnitude])

    def dividendos(self, command):

        atv = command.upper().replace('/DIVIDENDOS ', '')
        ret = None
        
        if len(atv) < 2:
            return 'Faltou o ticker'

        try:

            t = yf.Ticker(atv + '.SA')
            divs = t.dividends
            arr = []

            if t == None:
                return None

            ret = 'Ultimos 10 Dividendos de <b>{0}</b>: \n'.format(atv)

            i = 0
            for item in divs:

                idx = str(divs.index[i]).split(' ')[0]
                arr.append(idx + ' - R$ ' + str(item) + '\n')
                i += 1
            
            i = 0
            arr.reverse()
            for item in arr:
                
                if i >= 10:
                    break

                ret += item
                i += 1

        except:
            print('\n\n\n')
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}', type, value, traceback)
            print('\n\n\n')

        return ret

    def gerarGrafico(self, ativo:str):
        dt = datetime.datetime.now().date()
        d = yf.download(tickers='{0}.SA'.format(ativo), mav=(9, 21), period = '6mo', interval = '1d', rounding= True)

        if len(d) > 0:
            mc = mpf.make_marketcolors(base_mpf_style='nightclouds',edge='#505050',wick='#505050',volume='silver')
            s  = mpf.make_mpf_style(base_mpl_style='seaborn',marketcolors=mc)

            buf = io.BytesIO()
            mpf.plot(d, type='candle', ylabel=ativo + ' - ' + str(dt) , savefig=buf, style=s)
            buf.seek(0)

            return buf
        
        return None



