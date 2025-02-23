import os
import asyncio
from dotenv import load_dotenv
from Osdental.ServicesBus.ServicesBus import ServicesBus

load_dotenv()

class TaskQueue:
    """Queue to manage tasks in order and asynchronously."""

    def __init__(self):
        self.conn_str = os.getenv('CONNECTION_STRING')
        self.queue_name = os.getenv('QUEUE')
        self.service_bus = ServicesBus(self.conn_str, self.queue_name)
        self.queue = asyncio.Queue()
        

    def start_processing(self):
        """Start processing tasks in the background."""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.create_task(self.process_tasks())


    async def enqueue(self, message: dict):
        """Add a task to the queue."""
        await self.queue.put(message)


    async def process_tasks(self):
        """Process tasks from the queue in order."""
        while True:
            message = await self.queue.get()
            try:
                await self.service_bus.send_message(message)
            except Exception as e:
                print(f'Message queuing error: {e}')
            finally:
                self.queue.task_done()


task_queue = TaskQueue()
task_queue.start_processing()