import json
from typing import Dict
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from Osdental.Utils.Message import UNEXPECTED_ERROR

class ServicesBus:

    def __init__(self, conn_str:str, queue_name:str):
        self.conn_str = conn_str
        self.queue_name = queue_name


    async def send_message(self, message:Dict[str,str] | str) -> None:
        """Method to send a message to the Service Bus."""
        try:
            data = json.dumps(message) if isinstance(message, dict) else message
            async with ServiceBusClient.from_connection_string(self.conn_str) as servicebus_client:
                async with servicebus_client.get_queue_sender(queue_name=self.queue_name) as sender:
                    message = ServiceBusMessage(data)
                    await sender.send_messages(message)

        except Exception as e:
            raise ValueError(f'{UNEXPECTED_ERROR}: {str(e)}')
