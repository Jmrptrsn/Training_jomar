import asyncio

async def wait_before_retry(seconds=2):
    await asyncio.sleep(seconds)
