import asyncio

import httpx


async def main() -> None:
    while True:
        async with httpx.AsyncClient() as client:
            pass
        pass


if __name__ == "__main__":
    asyncio.run(main())
