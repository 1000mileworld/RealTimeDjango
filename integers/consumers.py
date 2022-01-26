from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from random import randint
from time import sleep

 
class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'number_data'

        #join group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        
        self.accept()
        #self.sourceData()
        
    
    def disconnect(self, close_code):
        # Leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'int_message',
                'message': message
            }
        )

    def int_message(self,event):
        #message = event['message']
        #message = str(randint(1,100))
        message = '7' #open 2 instances at same time, both should change
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    # def sourceData(self):
    #     for i in range(1000):
    #         self.send(json.dumps({'message': randint(1,100)}))
    #         sleep(1) 