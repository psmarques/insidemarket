from django.test import TestCase
import yfinance as yf

import io
# Create your tests here.

# function to add two numbers
def sumTwoNumbers(x:int, y:int):
    return x+y
    

msft = yf.Ticker('viia3.sa')
hst = msft.history('1y')

print(hst)

print(msft.dividends)
print("---------------------")
print(msft.actions)
print("---------------------")
print(msft.financials)
print("---------------------")
print(msft.major_holders)
print("---------------------")
print(msft.recommendations)
print("---------------------")
print(msft.calendar)

    

#print(msft.actions)
#print(msft.calendar)

#r = open("C:\\Users\\psmar\\OneDrive\\Imagens\\Teste.jpg", 'rb')
#print()
#print(r.read())
