import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

from .asyncio import run_in_executor
from .utils import DummyStopIteration, next_without_stop_iteration


async def prefetch_iterator(iterator):
    with ThreadPoolExecutor(1) as p:
        iterator = iter(iterator)
        prefetched = run_in_executor(p, next_without_stop_iteration, iterator)
        while True:
            try:
                ret = await prefetched
            except DummyStopIteration:
                break
            prefetched = run_in_executor(p, next_without_stop_iteration, iterator)
            yield ret


async def rate_limit_iterator(aiterator, iters_per_second):
    start = time.time()
    i = 0
    async for it in aiterator:
        yield it
        await asyncio.sleep((i / iters_per_second) - (time.time() - start))
        i += 1
