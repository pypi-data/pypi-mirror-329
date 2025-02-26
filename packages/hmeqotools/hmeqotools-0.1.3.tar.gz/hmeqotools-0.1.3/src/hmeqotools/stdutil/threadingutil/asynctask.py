from __future__ import annotations

import asyncio
import threading
from typing import Coroutine


class AsyncTaskCenter:
    def __init__(self, event_loop: asyncio.AbstractEventLoop | None = None):
        self.loop = event_loop or asyncio.new_event_loop()

    def run(self):
        self.loop.run_forever()

    def start(self):
        threading.Thread(target=self.loop.run_forever).start()

    def close(self):
        self.put(self.loop.stop)

    def put(self, task):
        if not isinstance(task, Coroutine):

            async def make_task(__task):
                __task()

            task = make_task(task)
        asyncio.run_coroutine_threadsafe(task, self.loop)
