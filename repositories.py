from proxybroker import Broker

import requests
import asyncio
import random

from constants import (
    PROXY_JUDGES,
    PROXY_PROVIDERS,
    PROXY_TYPES,
    PROXY_COUNTRIES,
    )
from helper import report

class ProxyApi:
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    
    #@report('REQUESTING PROXY')
    def get(
        self,
        limit: int =10,
        judges: list = PROXY_JUDGES,
        providers: list = PROXY_PROVIDERS,
        types: list = PROXY_TYPES,
        countries: list =PROXY_COUNTRIES,
        ):

        proxies = asyncio.Queue()
        broker = Broker(proxies, judges=judges, providers=providers)
        
        async def show(proxies):
            p = []
            while True:
                proxy = await proxies.get()
                if proxy is None: break
                p.append("{}:{}".format(proxy.host, proxy.port))
            return p
        
        tasks = asyncio.gather(broker.find(types=types, countries=countries, limit=limit), show(proxies))
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(tasks)[1]


#@report('REQUESTING NAME')
class NameApi:
    def new(self):
        return requests.get('https://gerador-nomes.herokuapp.com/nome/aleatorio').json()


#@report('REQUESTING QUOTE')
class MussumApi:
    def quote(self):
        return requests.get('https://mipsum.herokuapp.com/frases/random').json()['frase']


