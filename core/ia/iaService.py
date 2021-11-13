import random
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from core.models import Conversa
#from nltk.corpus import wordnet, stopwords
from random import choice

import sys

class iaService:
    bot = None
    trainer = None

    conversaDefault = ['Oi', 'Olá', 
                       'Tudo bem?', 'Tudo ótimo e você?', 
                       'Vou bem e você?', 'Melhor impossível', 
                       'Você gosta do seu criador?', 'Adoro ele',
                       'Ajuste do indice?', 'ajustewin',
                       'Ajsute do dolar?', 'ajustewdo',
                       'Noticias de hoje?', 'noticias']

    stopwords = ['?', '!']

    respostaDefault = ['Ainda não sei muito sobre este assunto mas você pode me ensinar...', 'Hummm não posso opinar sobre isso...', 'Meu conhecimento no momento está limitado, você gostaria de me explicar melhor?', 'Que tal mudarmos de assunto? posso buscar as cotações das ações e até mesmo de criptomoedas... utilize /help para saber mais']

    def __init__(self, *args, **kwargs):
        self.bot = ChatBot('Garcom Bot')
        self.trainer = ListTrainer(self.bot)

    def aprender(self, ppergunta):
        ar = ppergunta.split('?')
        ret = 'Houve uma falha'

        if ppergunta.find('?') < 0 or len(ar) < 2:
            return 'Pergunta mal formada, utilize: Pergunta? respota'
        
        try:
            per = Conversa.objects.filter(pergunta = ar[0])
            
            if len(per) > 0:
                obj = per[0]
                obj.pergunta = ar[0]
                obj.resposta = ar[1]
                obj.save()

                ret = 'Obrigado, me atualizei sobre: ' + str(ar[0])
                obj = None
            else:
                obj = Conversa(pergunta = str(ar[0]), resposta = str(ar[1]))
                obj.save()
                obj = None

                ret = 'Obrigado, aprendi sobre: ' + ar[0]

            self.treinar()

        except:
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}'.format(type, value, traceback))

        return ret

    def treinar(self):
        lst = []
        cvs = Conversa.objects.all()
        
        for item in self.conversaDefault:
            lst.append(str(item))

        for item in cvs:
            lst.append(str(item.pergunta))
            lst.append(str(item.resposta))
            #lst.insert([item.pergunta, item.resposta])

        print("****")
        print("treinando...")
        print(lst)

        #self.bot = ChatBot('Garcom Bot')
        #self.trainer = ListTrainer(self.bot)
        self.trainer.train(lst)
        print("****")
        lst = None

    def response(self, question):

        txt = question.lower()
        ret = ''

        res = self.bot.get_response(txt)

        if float(res.confidence) > 0.4:      
            ret = res.text
        else:
            ret = random.choice(self.respostaDefault)

        self.bot = None
        return ret
