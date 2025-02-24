import asyncio
import logging
import aio_pika
from contextlib import asynccontextmanager
from uuid import uuid4

from cattle_grid.dependencies.fastapi import Broker
from cattle_grid.model.account import EventType

logger = logging.getLogger(__name__)


@asynccontextmanager
async def queue_for_connection(connection, username: str, event_type: EventType):
    async with connection:
        routing_key = f"receive.{username}.{event_type.value}"

        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        exchange = await channel.declare_exchange(
            "amq.topic", aio_pika.ExchangeType.TOPIC, durable=True
        )

        queue = await channel.declare_queue(
            f"queue-{username}-{uuid4()}",
            durable=False,
            auto_delete=True,
        )
        await queue.bind(exchange, routing_key=routing_key)

        yield queue


async def enqueue_events(
    asyncio_queue, connection, username: str, event_type: EventType
):
    async with queue_for_connection(connection, username, event_type) as queue:
        async with queue.iterator() as iterator:
            try:
                async for message in iterator:
                    async with message.process():
                        message_body = message.body.decode()
                        await asyncio_queue.put(message_body)
            except Exception as e:
                logger.exception(e)


def get_message_streamer(broker: Broker, timeout: float = 5):
    if broker._connection is None:
        raise RuntimeError("Broker not connected")

    connection: aio_pika.RobustConnection = broker._connection

    async def stream_messages(username: str, event_type: EventType):
        queue = asyncio.Queue()
        task = asyncio.create_task(
            enqueue_events(queue, connection, username, event_type)
        )
        try:
            while True:
                try:
                    async with asyncio.timeout(timeout):
                        result = await queue.get()
                except TimeoutError:
                    logger.debug("Sending heartbeat")
                    result = None
                yield result
        except asyncio.CancelledError:
            logger.info("cancelling message queue for %s %s", username, event_type)
            task.cancel()

            try:
                await task
            except asyncio.CancelledError:
                pass
        except Exception as e:
            logger.exception(e)

    return stream_messages
