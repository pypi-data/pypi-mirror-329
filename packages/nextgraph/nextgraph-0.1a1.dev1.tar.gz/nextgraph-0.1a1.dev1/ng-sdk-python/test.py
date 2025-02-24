import asyncio
from nextgraph import rust_sleep

async def main():
    foo = {
        "foo": 3,
    }
    await rust_sleep(foo)

asyncio.run(main())