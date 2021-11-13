from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from core import message
import json
import sys


# Create your views here.
@csrf_exempt
def event(requests):
   r = ''
   try:
      if requests.body:
         print(requests.body)
         json_telegram = json.loads(requests.body)
         message.proccess(json_telegram)
         r += 'ok'
		 
   except:
      r += 'fail'
      print('\n\n\nError ao processar a mensagem...')
      type, value, traceback = sys.exc_info()
      print('Error: {0} {1} {2}'.format(type, value, traceback))
      print('{0}: {1}'.format(traceback.tb_next.tb_frame, traceback.tb_next.tb_lineno))

   return HttpResponse('Result: {0}', r)

@csrf_exempt
def updatePaper(request):
   r = 'header: ' + str(request) + '\n'
   r = r + 'Result: '
   try:
      message.atualizarCarteira()
      r = r + 'ok'
   except:
      type, value, traceback = sys.exc_info()
      r = r + 'fail'
      print('\n\n\nError ao atualizar as carteiras...')
      print('Error: {0} {1} {2}'.format(type, value, traceback))
      print('{0}: {1}'.format(traceback.tb_next.tb_frame, traceback.tb_next.tb_lineno))

   return HttpResponse('Atualizacao: {0}'.format(r))
