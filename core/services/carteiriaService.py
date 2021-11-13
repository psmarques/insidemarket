
from core.services.RequestService import RequestService
from core import models
from core.models import Carteira
from core.services.b3DadosService import b3DadosService
from core.services.papelService import PapelService

import multiprocessing
import datetime
import time
import requests
import sys
import json
import re

class CarteiraService:

    def consultarCarteira(self, command, chat_id, usuario, usuario_id):

        parms = command.split(' ')
        erro = 'Subcomando invalido, utilize /carteira para verificar'
        out = ''
        #out = str(chat_id) + ' -> ' + 'usuario:' + usuario + '\n'
        out = out + 'Para Adicionar um Papel:\n/carteira adicionar [papel] [valor compra] [valor stop] [valor profit] [situacao]\n'
        out = out + 'Ex: /carteira adicionar VALE3 33,55 30,95 39,10 COMPRADO\n'
        out = out + 'Para Modificar um Papel:\n'
        out = out + 'Ex: /carteira alterar VALE3 33,55, 30,45 37 ENCERRADO\n'
        out = out + 'Para Remover um Papel:\n'
        out = out + 'Ex: /carteira deletar VALE3\n'
        out = out + 'Para Listar os Papeis:\n'
        out = out + 'Ex: /carteira listar'
        
        #validar tudo isso aqui
        if len(parms) > 1:
            if parms[1] != 'adicionar' and parms[1] != 'deletar' and parms[1] != 'alterar' and parms[1] != 'listar':
                out = erro
            elif parms[1] == 'deletar' and len(parms) != 3:
                out = erro
            elif parms[1] == 'adicionar' and len(parms) != 7:
                out = erro
            elif parms[1] == 'alterar' and len(parms) != 7:
                out = erro
            elif parms[1] == 'listar' and len(parms) != 2:
                out = erro

            #Tudo Certo, vamos...
            else:
                
                if(parms[1] == 'listar'):
                    out = self.listarCarteira(chat_id)

                elif parms[1] == 'adicionar' or parms[1] == 'alterar':
                    resConsulta = b3DadosService().consultarAtivoB3('/cotação ' + parms[2])
                    papel = b3DadosService().recuperarPapel(parms[2])

                    if not resConsulta.startswith('Falha'):
                        out = self.adicionarCarteira(chat_id, parms[2], parms[3], parms[4], parms[5], parms[6], usuario, usuario_id, papel)
                        out = out
                    else:
                        out = 'Papel invalido!!!'

                elif parms[1] == 'deletar':
                    self.deletarCarteira(chat_id, parms[2])
                    out = 'Comando executado'
                            


        return out

    def adicionarCarteira(self, grupo_id, ppapel, compra, stoploss, takeprofit, psituacao, pusuario, pusuario_id, papel: models.Papel):
        dt = datetime.datetime.now()
        lst = Carteira.objects.filter(chat_id = grupo_id, papel = ppapel.upper())
        lstAll = Carteira.objects.filter(chat_id = grupo_id)
        ppcompra = float(compra.replace(',', '.'))
        pdirecao = 'UP'

        if lstAll != None and lstAll.count() > 3:
            return 'No plano gratuito você só pode adicionar 3 papéis!'

        if ppcompra >= papel.valor:
            pdirecao = 'UP'
        else:
            pdirecao = 'DOWN'

        if len(lst) > 0:
            obj = lst[0]
            obj.valor_compra = ppcompra
            obj.valor_stop = stoploss.replace(',', '.')
            obj.valor_tprofit = takeprofit.replace(',', '.')
            obj.situacao = psituacao
            obj.usuario = pusuario
            obj.usuario_id = pusuario_id
            obj.direcao = pdirecao

            obj.save()
            return 'Papel alterado'
        else:
            ob = Carteira(chat_id = grupo_id, papel = ppapel.upper(), valor_compra = compra.replace(',', '.'), valor_stop = stoploss.replace(',', '.'), valor_tprofit = takeprofit.replace(',', '.'), resultado = 0, situacao = psituacao, usuario = pusuario, usuario_id = pusuario_id, direcao = pdirecao)
            ob.save()
            return 'Papel adicionado'

    def deletarCarteira(self, grupo_id, ppapel):
        lst = Carteira.objects.filter(chat_id = grupo_id, papel = ppapel.upper())

        if len(lst) > 0:
            ob = lst[0]
            ob.delete()

    def listarCarteira(self, grupo_id):
        
        b3svc = b3DadosService()
        ret = ''
        lst = Carteira.objects.filter(chat_id = grupo_id)

        if(len(lst) > 0):
            
            for x in lst:
                ativo = PapelService().recuperarPapel(x.papel)
                dt = datetime.datetime.now(datetime.timezone.utc)
                result:float = 0

                if ativo is None:
                    b3svc.consultarAtivoB3("/cotacao " + x.papel)
                    ativo = b3svc.papelAtual
                else:
                    dt2 = dt - ativo.datahora
                    
                    if(dt2.total_seconds() > 900):
                        b3svc.consultarAtivoB3("/cotacao " + x.papel)
                        ativo = b3svc.papelAtual
                    

                result = x.resultado

                if x.situacao.upper() == 'GATILHO':
                    result = 0

                elif x.situacao.upper() == 'STOP' or x.situacao.upper() == 'GAIN':
                    result = x.resultado
                
                elif x.situacao.upper() == 'COMPRADO':
                    result = (float(ativo.valor)/float(x.valor_compra) - 1) * 100

                ret = ret + '-----------\n'
                ret = ret + '[' + x.papel + ']\t - Prc: ' + str(ativo.valor) + '\n'  
                ret = ret + 'Cpr: ' + str(x.valor_compra) + ' / Stp: ' + str(x.valor_stop) + ' / Gain: ' + str(x.valor_tprofit) + '\n'
                ret = ret + 'Sit: ' + x.situacao.upper() + ' / Res: ' + ("{0:.2f}".format(float(result))) + '%\n'

        else:
            ret = 'Nenhum papel foi adicionado, digite /carteira para verificar os comandos'

        return ret

    def atualizarCarteiras(self):
        lst = Carteira.objects.all()
        b3Svc = b3DadosService()
        papSvc = PapelService()
        reqSvc = RequestService()
        
        if(len(lst) > 0):

            for x in lst:
                try:
                    ativo = papSvc.recuperarPapel(x.papel)

                    if ativo != None:
                        dt = datetime.datetime.now(datetime.timezone.utc)
                        dt2 = dt - ativo.datahora
                        secs = dt2.total_seconds()

                        if(secs > 900):
                            b3Svc.consultarAtivoB3('/cotacao ' + x.papel)
                            ativo = papSvc.recuperarPapel(x.papel)
                    else:
                        r = b3Svc.consultarAtivoB3('/cotacao ' + x.papel)
                        print(r)
                        ativo = b3Svc.papelAtual

                    if x.situacao.upper() == 'GATILHO':
                        if (ativo.valor >= x.valor_compra or ativo.valor_maxima >= x.valor_compra) and x.direcao == 'UP':
                            x.situacao = 'COMPRADO'
                            x.save()
                            reqSvc.send(x.chat_id, '@' + x.usuario_id + ' ' + x.papel + ' Acionou gatilho de compra!!!')
                            
                        elif (ativo.valor <= x.valor_compra or ativo.valor_minima <= x.valor_compra) and x.direcao == 'DOWN':
                            x.situacao = 'COMPRADO'
                            x.save()
                            reqSvc.send(x.chat_id, '@' + x.usuario_id + ' ' + x.papel + ' Acionou gatilho de compra!!!')
                    
                    elif x.situacao.upper() == 'COMPRADO':
                        if ativo.valor <= x.valor_stop or ativo.valor_minima <= x.valor_stop:
                            x.situacao = 'STOP'
                            x.resultado = (x.valor_stop / x.valor_compra - 1) * 100
                            x.save()
                            reqSvc.send(x.chat_id, '@' + x.usuario_id + ' ' + x.papel +  ' Acionou StopLoss!!!')

                        elif ativo.valor >= x.valor_tprofit or ativo.valor_maxima >= x.valor_tprofit:
                            x.situacao = 'GAIN'
                            x.resultado = (x.valor_tprofit / x.valor_compra - 1) * 100
                            x.save()
                            reqSvc.send(x.chat_id, '@' + x.usuario_id + ' ' + x.papel + ' Acionou o Take Profit!!!')
                except:
                    print("Erro ao atualizar as carteiras")
                    return ''
