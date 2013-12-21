from decimal import Decimal
import requests
import json
import base64
import hmac
import hashlib
import time
import types


__all__ = ['Bitfinex']


BITFINEX = 'api.bitfinex.com/'
DECIMAL_KEYS = set(['amount', 'ask', 'available', 'bid', 'executed_amount', 'high', 'last_price', 'low', 'mid', 'original_amount', 'price', 'remaining_amount', 'timestamp', 'volume'])


def decimalize(obj, keys):
    if isinstance(obj, types.ListType):
        return [decimalize(xs, keys) for xs in obj]
    if not isinstance(obj, types.DictType):
        return obj
    #print obj
    def to_decimal(k, val):
        if val == None:
            return None
        if isinstance(val, types.ListType):
            return [decimalize(ys, keys) for ys in val]
        if k in keys:
            return Decimal(val)
        return val
    return { k: to_decimal(k, obj[k]) for k in obj }


def undecimalize(obj):
    if isinstance(obj, types.ListType):
        return map(undecimalize, obj)
    if not isinstance(obj, types.DictType):
        return obj
    #print obj
    def from_decimal(val):
        if isinstance(val, Decimal):
            return str(val)
        return val
    return { k: from_decimal(obj[k]) for k in obj }


class Bitfinex(object):
    def ticker(self, symbol="btcusd"):
        r = requests.get("https://"+BITFINEX+"/v1/ticker/"+symbol, verify=False)
        return decimalize(r.json(), DECIMAL_KEYS)


    def today(self, symbol="btcusd"):
        r = requests.get("https://"+BITFINEX+"/v1/today/"+symbol, verify=False)
        return decimalize(r.json(), DECIMAL_KEYS)


    def book(self, payload, symbol="btcusd"):
        headers = self._prepare_payload(False, payload)
        r = requests.get("https://"+BITFINEX+"/v1/book/"+symbol, headers=headers, verify=False)
        return decimalize(r.json(), DECIMAL_KEYS)


    def trades(self, payload, symbol="btcusd"):
        headers = self._prepare_payload(False, payload)
        r = requests.get("https://"+BITFINEX+"/v1/trades/"+symbol, headers=headers, verify=False)
        return decimalize(r.json(), DECIMAL_KEYS)


    def symbols(self):
        r = requests.get("https://"+BITFINEX+"/v1/symbols", verify=False)
        return decimalize(r.json(), DECIMAL_KEYS)


    def order_new(self, payload):
        payload["request"] = "/v1/order/new"
        payload["nonce"] = str(long(time.time() * 100000))
        headers = self._prepare_payload(True, payload)
        r = requests.post("https://"+BITFINEX+"/v1/order/new", headers=headers, verify=False)
        return decimalize(r.json(), DECIMAL_KEYS)


    def order_cancel(self, payload):
        payload["request"] = "/v1/order/cancel"
        payload["nonce"] = str(long(time.time() * 100000))
        headers = self._prepare_payload(True, payload)
        r = requests.post("https://"+BITFINEX+"/v1/order/cancel", headers=headers, verify=False)
        return decimalize(r.json(), DECIMAL_KEYS)


    def order_status(self, payload):
        payload["request"] = "/v1/order/status"
        payload["nonce"] = str(long(time.time() * 100000))
        headers = self._prepare_payload(True, payload)
        r = requests.get("https://"+BITFINEX+"/v1/order/status", headers=headers, verify=False)
        return decimalize(r.json(), DECIMAL_KEYS)


    def orders(self):
        payload = {}
        payload["request"] = "/v1/orders"
        payload["nonce"] = str(long(time.time() * 100000))
        headers = self._prepare_payload(True, payload)
        r = requests.get("https://"+BITFINEX+"/v1/orders", headers=headers, verify=False)
        return decimalize(r.json(), DECIMAL_KEYS)


    def balances(self):
        payload = {}
        payload["request"] = "/v1/balances"
        payload["nonce"] = str(long(time.time() * 100000))
        headers = self._prepare_payload(True, payload)
        r = requests.get("https://"+BITFINEX+"/v1/balances", headers=headers, verify=False)
        return decimalize(r.json(), DECIMAL_KEYS)




    # Private
    def _prepare_payload(self, should_sign, d):
        j = json.dumps(undecimalize(d))
        data = base64.standard_b64encode(j)


        if should_sign:
            h = hmac.new(self.secret, data, hashlib.sha384)
            signature = h.hexdigest()


            return {
                "X-BFX-APIKEY": self.key,
                "X-BFX-SIGNATURE": signature,
                "X-BFX-PAYLOAD": data,
            }
        else:
            return {
                "X-BFX-PAYLOAD": data,
            }