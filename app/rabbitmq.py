import asyncio

from aio_pika import connect_robust, Message, Exchange


class RabbitMQClient:
    def __init__(self, login, password, host, queues):
        self.login = login
        self.password = password
        self.host = host
        self.queues = queues

    async def connect(self):
        connection = await connect_robust(
            f"amqp://{self.login}:{self.password}@{self.host}"
        )
        channel = await connection.channel()
        return connection, channel

    async def listen(self):
        tasks = []
        for (queue_name, handler) in self.queues:
            connection, channel = await self.connect()
            await channel.declare_queue(queue_name, durable=True, exclusive=False, auto_delete=False)
            queue = await channel.get_queue(queue_name)
            task = asyncio.create_task(queue.consume(handler))
            tasks.append(task)
        await asyncio.gather(*tasks)
