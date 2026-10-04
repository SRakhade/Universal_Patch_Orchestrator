import asyncio
import logging
from redis.asyncio import Redis
from packages.common.settings import settings

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("upo.worker")

async def run():
    redis = Redis.from_url(settings.redis_url, decode_responses=True)
    log.info("Universal Patch Orchestrator worker started")
    while True:
        await redis.set("upo:worker:heartbeat", "alive", ex=30)
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(run())
