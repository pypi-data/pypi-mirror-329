import asyncio
from ssl import SSLContext
from typing import Any, Awaitable, Callable, List, Optional, Type, TypeVar

import nats
from nats.aio.client import Client, Subscription
from nats.aio.msg import Msg
from nats.errors import TimeoutError
from pydantic import BaseModel

from pjdev_message_broker.models import (
    ErrorMessage,
    Message,
    MessageBaseModel,
    MessageResponse,
)

T = TypeVar("T", bound=MessageBaseModel)

nc: Optional[Client] = None
subscriptions: List[Subscription] = []


async def init(servers: List[str], tls: Optional[SSLContext] = None) -> None:
    from loguru import logger

    global nc
    logger.info(f"Attempting to connect to nats server: {','.join(servers)}")
    nc = await nats.connect(servers, tls=tls)
    logger.success(f"Connected to nats server: {','.join(servers)}")


async def send_request(
    subject: str, payload: T, out_type: Type[BaseModel]
) -> MessageResponse:
    if nc:
        try:
            response = await nc.request(subject, payload.to_bytes(), timeout=10)
            return MessageResponse[out_type].model_validate_json(response.data.decode())
        except TimeoutError as e:
            logger.error("timed out waiting for reply")
            raise e

        except Exception as e:
            raise e


async def publish(subject: str, payload: T) -> MessageResponse[Message]:
    if nc:
        message = Message(value=True)
        try:
            await nc.publish(subject=subject, payload=payload.to_bytes())
            return MessageResponse(body=message)
        except Exception as e:
            message.value = False
            return MessageResponse(error=ErrorMessage.from_exception(e))


async def cleanup() -> None:
    await nc.drain()


async def subscribe(
    subject: str,
    queue: str,
    cb: Callable[[T], Awaitable[MessageResponse]],
    parsing_cb: Callable[[bytes], T],
) -> None:
    if nc is not None:
        sub = await nc.subscribe(
            subject=subject, queue=queue, cb=__cb_request_wrapper_async(cb, parsing_cb)
        )
        subscriptions.append(sub)


async def listen(
    subject: str, cb: Callable[[T], None], parsing_cb: Callable[[bytes], T]
) -> None:
    if nc:
        sub = await nc.subscribe(subject=subject, cb=__cb_wrapper(cb, parsing_cb))

        subscriptions.append(sub)


async def listen_async(
    subject: str, cb: Callable[[T], Awaitable[None]], parsing_cb: Callable[[bytes], T]
) -> None:
    if nc:
        sub = await nc.subscribe(subject=subject, cb=__cb_wrapper_async(cb, parsing_cb))

        subscriptions.append(sub)


def __cb_request_wrapper_async(
    cb: Callable[[T], Awaitable[MessageResponse]], parsing_cb: Callable[[bytes], T]
) -> Callable[[Msg], Any]:
    async def callback(msg: Msg) -> Any:
        payload = parsing_cb(msg.data)
        result = await cb(payload)

        reply_payload = result.to_bytes()

        await nc.publish(msg.reply, reply_payload)

    return callback


def __cb_wrapper(
    cb: Callable[[T], None], parsing_cb: Callable[[bytes], T]
) -> Callable[[Msg], Awaitable[None]]:
    async def callback(msg: Msg) -> None:
        return cb(parsing_cb(msg.data))

    return callback


def __cb_wrapper_async(
    cb: Callable[[T], Awaitable[None]], parsing_cb: Callable[[bytes], T]
) -> Callable[[Msg], Awaitable[None]]:
    async def callback(msg: Msg) -> None:
        return await cb(parsing_cb(msg.data))

    return callback


if __name__ == "__main__":
    from loguru import logger

    class DemoPayload(MessageBaseModel):
        msg: str

    async def demo_cb(payload: DemoPayload) -> bool:
        logger.info(f"Here's the payload: {payload.msg}")
        return True

    async def handle_request(subject: str, b: T) -> None:
        try:
            await send_request(subject, b)
        except Exception:
            pass
        finally:
            logger.info("finished request")

    async def main() -> None:
        await init([])

        subject = "demo.test"
        blocks = [DemoPayload(msg=f"Message {ndx}") for ndx in range(0, 100)]
        await subscribe(
            subject, "DEMO_Q1", demo_cb, lambda d: DemoPayload.model_validate_json(d)
        )
        tasks = [asyncio.create_task(handle_request(subject, b)) for b in blocks]
        try:
            await asyncio.gather(*tasks)
        finally:
            await cleanup()

    asyncio.run(main())
