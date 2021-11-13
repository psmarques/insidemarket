from core.constant import TOKEN, URLANIMATION, URLMESSAGE
import yfinance as yf
import requests
import sys
import pandas as pd
import mplfinance as mpf
import io

class RequestService:

    def send(self, chat_id:str, message:str):
        
        if message.upper().strip().startswith("HTTP://") or message.strip().upper().startswith("HTTPS://"):
            self.sendAnimation(chat_id, message)
        elif message.startswith("grafico:"):
            self.sendImage(chat_id, message)
        else:
            self.sendMessage(chat_id, message)


    def sendMessage(self, chat_id:str, message:str):
        url = URLMESSAGE.format(TOKEN)

        print(message)
        data1 = {'chat_id': chat_id, 'text' : message.strip(), 'parse_mode': 'html'}

        try:
            r = requests.post(url, data=data1, timeout=5)
            print(r.content)
        except:
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}'.format(type, value, traceback))
            print('{0}: {1}'.format(traceback.tb_next.tb_frame, traceback.tb_next.tb_lineno))
            return 0

        return 1


    def sendAnimation(self, chat_id:str, message:str):
        urlGif = URLANIMATION.format(TOKEN)
        data2 = {'chat_id': chat_id, 'animation': message.strip()}

        try:
            r = requests.post(urlGif, data = data2, timeout=5)
            print(r.content)
        except:
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}'.format(type, value, traceback))
            print('{0}: {1}'.format(traceback.tb_next.tb_frame, traceback.tb_next.tb_lineno))


        return 1

    def sendImageUrl(self, chat_id:str, imageUrl:str):
        urlGif = URLANIMATION.format(TOKEN)
        urlGif = urlGif.replace('/sendAnimation', '/sendPhoto')
        urlGif = urlGif + '?chat_id=' + str(chat_id)

        data2 = {'photo': imageUrl}

        try:
            r = requests.post(urlGif, data = data2, timeout=5)
            print(r)
        
        except:
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}'.format(type, value, traceback))
            print('{0}: {1}'.format(traceback.tb_next.tb_frame, traceback.tb_next.tb_lineno))
 
    def sendImageBinary(self, chat_id:str, buf:any):

        urlGif = URLANIMATION.format(TOKEN)
        urlGif = urlGif.replace('/sendAnimation', '/sendPhoto')
        urlGif = urlGif + '?chat_id=' + str(chat_id)

        data2 = {'caption': ''}

        #d = yf.download(tickers='ITSA4.SA', mav=(9, 21), period = '6mo', interval = '1d', rounding= True)
        #fig = go.Figure()
        #fig.add_trace(go.Candlestick())
        #fig.add_trace(go.Candlestick(x=d.index,open = d['Open'], high=d['High'], low=d['Low'], close=d['Close'], name = 'market data'))

        #img_bytes = fig.to_image(format="png")

        #mc = mpf.make_marketcolors(base_mpf_style='nightclouds',edge='#505050',wick='#505050',volume='silver')
        #s  = mpf.make_mpf_style(base_mpl_style='seaborn',marketcolors=mc)

        #buf = io.BytesIO()
        #mpf.plot(d, type='candle', savefig=buf, style=s)
        #buf.seek(0)     


        #hdrs = {'Content-Type': 'multipart/form-data'}
        #data2 = {'chat_id': chat_id, 'photo': 'file1', 'file1': open('C:/Users/psmar/OneDrive/Imagens/Teste.jpg', 'rb'), 'caption': 'Teste'}
        #data2 = {'photo': image[8:], 'caption': 'Grafico'}

        try:
            #aim = requests.get('https://images.dog.ceo//breeds//husky//n02110185_8216.jpg')

            requests.post(urlGif, data=data2, files={ 'photo': buf }, timeout=5)


            #requests.post(urlGif, data=data2, files={ 'photo': open('C:/Users/psmar/OneDrive/Imagens/Teste.jpg', 'rb') }, timeout=5)
            #requests.post(urlGif, data=data2, files={ 'photo': aim.content }, timeout=5)
            
            #r = requests.post(urlGif, data = data2, headers=hdrs, timeout=5)
            #print(r.content)

            #data = {"chat_id": chat_id, "caption": 'grafico'}
            #with open('C:/Users/psmar/OneDrive/Imagens/Teste.jpg', "rb") as image_file:
            #    ret = requests.post(urlGif, data=data, files={"photo": image_file})

        except:
            type, value, traceback = sys.exc_info()
            print('Error: {0} {1} {2}'.format(type, value, traceback))
            print('{0}: {1}'.format(traceback.tb_next.tb_frame, traceback.tb_next.tb_lineno))


        return 1

