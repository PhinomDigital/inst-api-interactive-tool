import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import hashlib
import hmac
import json
import base64
import requests
import time

class InstrumentsRequest:
    def endpoint(self):
        return '/instruments'
class PriceRequest:
    def endpoint(self):
        return '/price'
class PositionsRequest:
    def endpoint(self):
        return '/positions'
class OrdersRequest:
    def endpoint(self):
        return '/orders'
class OrderRequest:
    def endpoint(self):
        return '/order'
class ClientReqClass:
    def __init__(self,url='https://ins.phinom-digital.dev',
                 key = '',
                 secret = ''):
        self.headers = {
            'ApiKey': key,
            'X-hmac-key': '',
            'X-hmac-client-id': 'id',
            'x-hmac-nounce': '',
            'Content-Type': 'application/json',
            'accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',

        }
        self.url = url
        self.secret = secret
        self.err = None

    def update_headers(self,):
        nonce = int(time.time())
        sign = ''
        try:
            sign = self.get_kraken_signature(nonce, self.secret)
        except:
            pass
        self.headers['x-hmac-nounce'] = str(nonce)
        self.headers['X-hmac-key'] = sign

        pass

    def get(self,method,params):
        self.update_headers()
        response = requests.request("GET", self.url+method, headers=self.headers, params = params,verify=False )
        if response.ok == False:
            self.err = 'Error:'+response.text
            return None
        y = json.loads(response.text)
        return y
    def post(self,method,payload):
        self.update_headers()
        response = requests.post(url=self.url+method, headers=self.headers,data=payload,verify=False )
        if response.ok == False:
            self.err = 'Error:'+response.text
            return None
        y = json.loads(response.text)
        return y
    def delete(self,method,params):
        self.update_headers()
        response = requests.request("DELETE", self.url+method, headers=self.headers, params = params,verify=False )
        if response.ok == False:
            self.err = 'Error:'+response.text
            return None
        y = json.loads(response.text)
        return y

    def get_kraken_signature(self,nonce, secret):
        mac = hmac.new(secret.encode(), (str(nonce)).encode(), hashlib.sha256)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()
class PhDAPI:
    def __init__(self,api_key,secret,url):
        self.api_key = api_key
        self.secret = secret
        self.url = url
        self.client = ClientReqClass(self.url,self.api_key,self.secret)
        pass
    def instruments(self,symbol,option_type):
        req = InstrumentsRequest()
        res = self.client.get(req.endpoint(),params = {'assetId':symbol,'optionType':option_type})
        if res is None:
            return None
        df = pd.DataFrame(res)
        return df
    def post_order(self,product_id,quantity,price,side):
        req = OrderRequest()
        data = {
            'productId': product_id,
            'quantity': quantity,
            'price': price,
            'side': side
        }
        res = self.client.post(req.endpoint(),payload=json.dumps(data))
        if res is None:
            return None
        df = pd.DataFrame([res])
        return df
    def delete_order(self,order_id):
        req = OrderRequest()
        params={'orderId':order_id}
        res = self.client.delete(req.endpoint(),params=params)
        if res is None:
            return None
        df = pd.DataFrame([res])
        return df
    def orders(self,product_id,is_active,start_time,end_time,limit):
        req = OrdersRequest()
        params = {  'ProductId':product_id,
                    'IsActive':is_active,
                    'StartTime':start_time,
                    'EndTime':end_time,
                    'Limit':limit,}
        res = self.client.get(req.endpoint(),params=params)
        df = pd.DataFrame(res)
        return df
    def price(self,product_id):
        req = PriceRequest()
        params = {'ProductId':product_id}
        res = self.client.get(req.endpoint(),params = params)
        if res is None:
            return None
        df = pd.DataFrame([res])
        return df
    def positions(self,product_id):
        req = PositionsRequest()
        params = {'ProductId':product_id}
        res = self.client.get(req.endpoint(),params = params)
        if res is None:
            return None
        df = pd.DataFrame(res)
        return df