import requests
import json

apikey = '151KH6WMYOWDMWO6'

def getstockprice(stockname):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}'.format(stockname, apikey)
    resp = requests.get(url = url)
    data = json.loads(resp.text)
    date = data['Meta Data']['3. Last Refreshed']

    newdata = data['Time Series (Daily)'][date]
    message = '*DAY:* %s\n*OPENING PRICE:* $%s\n*CLOSING PRICE:* $%s\n*HIGH:* $%s\n*LOW:* $%s\n*VOLUME SOLD:* %s' %(date, newdata["1. open"], newdata["4. close"], newdata["2. high"], newdata["3. low"], newdata["5. volume"])
    return message
