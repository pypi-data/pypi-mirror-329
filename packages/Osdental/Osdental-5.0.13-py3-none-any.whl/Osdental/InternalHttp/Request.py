import os
import asyncio
from json import dumps
from datetime import datetime
from fastapi import Request
from dotenv import load_dotenv
from tzlocal import get_localzone
from Osdental.ServicesBus.TaskQueue import task_queue

load_dotenv()

class CustomRequest:

    def __init__(self, request: Request):
        self.request = request
        self.local_tz = get_localzone()
        asyncio.create_task(self.send_to_service_bus())

    async def send_to_service_bus(self) -> None:
        message_in = await self.request.json()  
        message_json = {
            'idMessageLog': self.request.headers.get('Idmessagelog'),
            'type': 'REQUEST',
            'environment': os.getenv('ENVIRONMENT'),
            'dateExecution': datetime.now(self.local_tz).strftime('%Y-%m-%d %H:%M:%S'),
            'header': dumps(dict(self.request.headers)),
            'microServiceUrl': str(self.request.url),
            'microServiceName': os.getenv('MICROSERVICE_NAME'),
            'microServiceVersion': os.getenv('MICROSERVICE_VERSION'),
            'serviceName': message_in.get('operationName'),
            'machineNameUser': self.request.headers.get('Machinenameuser'),
            'ipUser': self.request.headers.get('Ipuser'),
            'userName': self.request.headers.get('Username'),
            'localitation': self.request.headers.get('Localitation'),
            'httpMethod': self.request.method,
            'httpResponseCode': '*',
            'messageIn': dumps(message_in) if isinstance(message_in, dict) else message_in,
            'messageOut': '*',
            'errorProducer': '*',
            'auditLog': 'MESSAGE_LOG_INTERNAL'
        }
        asyncio.create_task(task_queue.enqueue(message_json))