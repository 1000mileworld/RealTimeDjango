from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json
from random import randint
#from time import sleep
from asyncio import sleep
from . import alpaca
 
import nest_asyncio

class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):        
        await self.accept()
        # for i in range(100):
        #     await self.send(json.dumps({'message': randint(1,100)}))
        #     await sleep(1) 

        # bars = alpaca.getBars('AAPL','2022-01-17','2022-01-21')
        # for bar in bars:
        #     await self.send(json.dumps({'message': bar.c}))
        #     await sleep(1)

        # runs into connection error ~45s after streaming
        # nest_asyncio.apply() #prevent error: event loop is already running
        # symbols = ['AAPL']
        # await alpaca.streamQuote(symbols,self.quote_callback)
    
        while alpaca.isOpen():
            quote = alpaca.getQuote('AAPL')
            await self.send(json.dumps({
                'bid': quote.bidprice,
                'ask': quote.askprice,
                }))
            await sleep(1)

    # async def quote_callback(self,q):
    #     await self.send(json.dumps({'message': q.bid_price}))
    #     await sleep(0.2)
        #print(q.symbol + ' bid price: ' + str(q.bid_price))