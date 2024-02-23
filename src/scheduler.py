import asyncio
from datetime import datetime, timedelta, timezone

import httpx
from db.session import async_session_factory
from services.rate_provider import get_rate_provider
from settings import rates_settings


async def main() -> None:
    while True:
        while True:
            # Calculate the next run time (6 AM or 6 PM UTC)
            now = datetime.now(timezone.utc)
            next_run = now.replace(hour=6, minute=0, second=0, microsecond=0)
            if now.hour >= 18:
                next_run += timedelta(days=1)
            elif now.hour >= 6:
                next_run = next_run.replace(hour=18)

            sleep_seconds = (next_run - now).total_seconds()

            print(f"Next update scheduled at {next_run.isoformat()}. Sleeping for {sleep_seconds} seconds.")
            await asyncio.sleep(sleep_seconds)

            async with httpx.AsyncClient() as client:
                data = await client.get(url=rates_settings.api_request_url)
                json_data = data.json()
                rate_provider = get_rate_provider()
                async with async_session_factory() as session:
                    await rate_provider().update_rates(session, json_data)


if __name__ == "__main__":
    asyncio.run(main())
