import asyncio
from typing import Mapping
from datetime import datetime
from tzlocal import get_localzone
from Osdental.ServicesBus.TaskQueue import task_queue
from Osdental.Utils.Code import APP_ERROR
from Osdental.Utils.Message import EXCEPTION_MSG

class OSDException(Exception):
    """ Base class for all custom exceptions. """
    def __init__(self, message:str=EXCEPTION_MSG, error:str=None, status_code:str=APP_ERROR, headers: Mapping[str,str] | None = None):
        super().__init__(message)
        self.message = message
        self.error = error
        self.headers = headers
        self.status_code = status_code
        self.local_tz = get_localzone()
        asyncio.create_task(self.send_to_service_bus())

    async def send_to_service_bus(self) -> None:
        """ Method to send a message to the Service Bus. """
        if self.headers:
            message_json = {
                'idMessageLog': self.headers.get('Idmessagelog'),
                'type': 'ERROR',
                'dateExecution': datetime.now(self.local_tz).strftime('%Y-%m-%d %H:%M:%S'),
                'httpResponseCode': self.status_code,
                'messageOut': '*',
                'errorProducer': self.error if self.error else '*',
                'auditLog': 'MESSAGE_LOG_INTERNAL'
            }
            asyncio.create_task(task_queue.enqueue(message_json))

class UnauthorizedException(OSDException):
    pass

class RequestDataException(OSDException):
    pass

class DatabaseException(OSDException):
    pass

class RSAEncryptException(OSDException):
    pass

class AESEncryptException(OSDException):
    pass

class JWTokenException(OSDException):
    pass

class HttpClientException(OSDException):
    pass

class AzureException(OSDException):
    pass

class RedisException(OSDException):
    pass