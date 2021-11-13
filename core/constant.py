import os

NOMEBOT = 'garcom'
TOKEN = os.environ.get("TOKEN")
URLMESSAGE = 'https://api.telegram.org/bot{0}/sendMessage'
URLANIMATION = 'https://api.telegram.org/bot{0}/sendAnimation'
URLLEAVECHAT = 'https://api.telegram.org/bot{0}/leaveChat'
URLAJUSTEB3 = 'http://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/Ajustes1.asp'
URLATIVOB3 = 'https://finance-services.msn.com/Market.svc/ChartAndQuotes?symbols=56.1.{0}.BSP&chartType=1d&isETF=false&iseod=False&lang=pt-BR&isCS=false&isVol=true&prime=true'
CODIGOMINI = 'www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/Ajustes1.asp'
URLVARIACAOB3 = 'http://cotacao.b3.com.br/mds/api/v1/InstrumentPriceFluctuation/ibov'
URLVARIACAOVOLB3 = 'http://cotacao.b3.com.br/mds/api/v1/InstrumentTradeVolume/vista'
NOTICIASURL = 'https://www.forexfactory.com/calendar.php'
CALENDARIORSS = 'https://www.myfxbook.com/rss/forex-economic-calendar-events'
ATIVOURL = 'https://api.iextrading.com/1.0/stock/{0}/batch?types=quote'

FIXERKEY = os.environ.get("FIXERKEY")
FIXERURL = 'http://data.fixer.io/api/'

CRYPTOURL = 'https://min-api.cryptocompare.com/data/price?fsym={0}&tsyms={1}&api={2}'
CRYPTOURL2 = 'https://min-api.cryptocompare.com/data/generateAvg?fsym={0}&tsym={1}&e=Kraken&api={2}'
CRYPTOKEY= os.environ.get("CRYPTOKEY")
