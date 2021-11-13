#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.services.RequestService import RequestService
from core.services.carteiriaService import CarteiraService
from core.models import Carteira
from core.constant import TOKEN, URLANIMATION, URLMESSAGE

from core.services.b3DadosService import b3DadosService
from core.services.comandoService import ComandoCacheService
from core.services.papelService import PapelService

from core.handlers.Handler import Handler
from core.handlers.CryptoHandler import CryptoHandler
from core.handlers.AcessoHandler import AcessoHandler
from core.handlers.PapelHandler import PapelHandler
from core.handlers.PapelAjusteHandler import PapelAjusteHandler
from core.handlers.PapelSaldoHandler import PapelSaldoHandler
from core.handlers.PapelVolumeHandler import PapelVolumeHandler
from core.handlers.PapelVariacaoHandler import PapelVariacaoHandler
from core.handlers.NoticiasHandler import NoticiasHandler
from core.handlers.IAHandler import IAHandler
from core.handlers.SaudacaoHandler import SaudacaoHandler
from core.handlers.CarteiraHandler import CarteiraHandler
from core.handlers.ComandoCustomHandler import ComandoCustomHandler
from core.handlers.FeriadoHandler import FeriadoHandler

from datetime import timezone
from unidecode import unidecode

import datetime
import time
import requests
import sys

def processCommand(hand: Handler, command: str, chatid: str, json_telegram):
    result = hand.handle(command, chatid, json_telegram)
    return result

def proccess(json_telegram):
        output = ''

        reqSvc = RequestService()
        cmdSvc = ComandoCacheService()
        accessHand = AcessoHandler()
        cryptoHand = CryptoHandler()
        papelHand = PapelHandler()
        papelAjusteHand = PapelAjusteHandler()
        papelSaldoHand = PapelSaldoHandler()
        papelVariacaoHand = PapelVariacaoHandler()
        papelVolumeHand = PapelVolumeHandler()
        noticiaHand = NoticiasHandler()
        iaHand = IAHandler()
        saudacaoHand = SaudacaoHandler()
        carteiraHand = CarteiraHandler()
        feriadoHand = FeriadoHandler()
        ccmdHand = ComandoCustomHandler()

        chatid = cmdSvc.recuperarChatId(json_telegram)
        chattype = cmdSvc.recuperarChatType(json_telegram)
        command = cmdSvc.recuperarChatCommand(json_telegram)
        userName = cmdSvc.recuperarComandoUserName(json_telegram)
       
        print("User: {0}".format(userName))
        print("Command: {0} ".format(command))
        print("ChatType: {0}".format(chattype))
        print("ChatId: {0}".format(chatid))

        #chain responsibility principle
        accessHand.set_next(cryptoHand)\
            .set_next(saudacaoHand)\
            .set_next(papelHand)\
            .set_next(papelAjusteHand)\
            .set_next(papelSaldoHand)\
            .set_next(papelVariacaoHand)\
            .set_next(papelVolumeHand)\
            .set_next(noticiaHand)\
            .set_next(iaHand)\
            .set_next(carteiraHand)\
            .set_next(feriadoHand)\
            .set_next(ccmdHand)\
            .set_next(None)

        output = processCommand(accessHand, command, chatid, json_telegram)

        if output == None or len(output) < 1:
            return 'ok'

        #envia a msg            
        reqSvc.send(chatid, output)
        
        #limpar a mem
        del cryptoHand
        del saudacaoHand
        del papelAjusteHand
        del papelSaldoHand
        del papelVariacaoHand
        del papelVolumeHand
        del noticiaHand
        del iaHand
        del carteiraHand
        del feriadoHand
        del ccmdHand
        del reqSvc


#Atualizar as carteiras
def atualizarCarteira():
    CarteiraService().atualizarCarteiras()
