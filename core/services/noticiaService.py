from requests.api import request
from core.constant import NOTICIASURL
from core.constant import CALENDARIORSS
from xml.dom import minidom
from dateutil import tz
from datetime import datetime

import requests
import re
import html
import html.parser

class NoticiaService:


    def consultarCalendario(self):
        out = requests.get(CALENDARIORSS)
        r = ''

        xmldoc = minidom.parseString(out.text)
        items = xmldoc.getElementsByTagName('item')

        for item in items:
            i = 0
            noticia = ''
            datahora = ''

            for a in item.childNodes:

                if(len(a.childNodes) > 0):
                    #titulo
                    if i == 1:
                        noticia = noticia + str(a.childNodes[0].data) + "\n"

                    #data
                    elif i % 5 == 0:
                        datahora = a.childNodes[0].data
                        #print(a.childNodes[0].data)
                    
                    #conteudo
                    elif i % 7 == 0:
                        d = a.childNodes[0].data
                        tmp = d.split('<tr>')

                        dados = tmp[2].split('<td>')
                        #print(self.cleanhtml(dados[0]))
                        noticia = noticia + 'At: ' + self.cleanhtml(dados[1]) + ' / ' + self.dateConvert(datahora) + '\n'
                        #print(self.cleanhtml(dados[2]))
                        noticia = noticia + 'Prev: ' + self.cleanhtml(dados[3])
                        #print(self.cleanhtml(dados[3]))
                        noticia = noticia + ' / Cons: ' + self.cleanhtml(dados[4])
                        #print(self.cleanhtml(dados[4]))
                        noticia = noticia + ' / Act: ' + self.cleanhtml(dados[5]) + '\n\n'

                        if str(dados[2]).find('sprite-medium-impact') > 0 or str(dados[2]).find('sprite-high-impact') > 0:
                            r = r + noticia    

                i = i+1

        return r

    def stripChars(self, data):
        p = self.striphtml(data)
        p = p.replace('\n', '')
        p = p.strip(' ')
        p = p.strip('/')

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
        st = st.replace('&lt;', '')
        st = st.replace('tr&gt;', '')
        st = st.replace('/th&gt;', '')
        st = st.replace('th&gt;', '')
        st = st.replace('&gt;', '')

        return st

    def cleanhtml(self, raw_html):

        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleanr2 = re.compile('https?\S+')
        cleantext = re.sub(cleanr, '', raw_html)
        cleantext = re.sub(cleanr2, '', cleantext)

        cleantext = cleantext.strip()
        cleantext = cleantext.strip(' ')
        cleantext = cleantext.replace('  ', '')
        cleantext = cleantext.replace("\t", "  ")
        cleantext = cleantext.replace("\n\n", "")
        #cleantext = cleantext.replace("\n\n", "")
        cleantext = cleantext.replace("\r\n\r\n", "")
        
        # cleantext = self.stripChars(cleantext)
        # cleantext = self.striphtml(cleantext)

        return cleantext

    def dateConvert(self, txt):

        #print "Date in GMT: {0}".format(txt)
        # Hardcode from and to time zones
        #datetime.tzinfo
        from_zone = tz.gettz('GMT')
        to_zone = tz.gettz('America/Sao_Paulo')
        # gmt = datetime.gmtnow()
        gmt = datetime.strptime(txt, '%a, %d %b %Y %H:%M GMT')
        # Tell the datetime object that it's in GMT time zone
        gmt = gmt.replace(tzinfo=from_zone)
        
        # Convert time zone
        eastern_time = str(gmt.astimezone(to_zone))
        
        # Check if its EST or EDT        
        if eastern_time[-6:] == "-03:00":
            print ("Date in US/Eastern: " +eastern_time.replace("-03:00"," EST"))
            eastern_time = eastern_time.replace("-03:00"," UTC(-3)")
        elif eastern_time[-6:] == "-02:00":
            print("Date in US/Eastern: " +eastern_time.replace("-02:00"," UTC(-2)"))
            eastern_time = eastern_time.replace("-03:00"," UTC(-3)")
        
        return eastern_time
        
        #return
