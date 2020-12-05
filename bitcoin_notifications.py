import requests
import json
import sys

"""gets the bitcoin price. On sucess it returns the price else it return None"""
def get_bitcoin_price(api_key):
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key,
  }
  r = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest', headers=headers)
  datas = r.json() 
  #checking the status code
  if r.status_code == requests.codes.ok:   
    #datas has two keys, so specify the key we want to get the price
    for key in datas['data']:  
      value_price = key['quote']['USD']['price']
      break
    return value_price
  return None

"""makes apost call to IFTTP returns True on sucess """
def send_IFTTP_alert(event_name, key):
  bitcoin_price_crossed = f"https://maker.ifttt.com/trigger/{event_name}/with/key/{key}"
  m = requests.post(bitcoin_price_crossed)
  #checking the status code
  if m.status_code == requests.codes.ok:
    return True
  return False

#checking for 4 valid arguments such as program name, api_key, event_name, key 
#here "sys.argv" is a list  
if len(sys.argv) == 4:  
  api_key = sys.argv[1]
  event_name = sys.argv[2]
  key = sys.argv[3]

  result = get_bitcoin_price(api_key)
  if result > 10000:
    print(result)
    send_IFTTP_alert(event_name, key)
else:
  print("enter valid arguments")
