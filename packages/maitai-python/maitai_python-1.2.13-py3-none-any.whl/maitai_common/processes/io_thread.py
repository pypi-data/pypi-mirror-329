import asyncio
import time
import traceback
from threading import Thread


class IOThread(Thread):
    def __init__(self, interval=0.1, name=None):
        super(IOThread, self).__init__(name=name)
        self.input = None
        self.output = None
        self.run_thread = True
        self.is_running = False
        self.initialized = False
        self.interval = interval
        self.completed_loops = 0
        self.avg_loop_time = 0
        self.cleaned = False
        self.last_loop_start = -1
        self.child_name = self.__class__.__name__ if name is None else name

    def run(self):
        if not self.initialized:
            self.initialize()
        asyncio.run(self.main_loop())

    async def main_loop(self):
        await asyncio.sleep(self.interval)
        while self.run_thread:
            await self.process_loop()

    async def process_loop(self):
        if self.run_thread:
            self.last_loop_start = time.time()
            self.is_running = True
            try:
                self.process()
                await self.process_async()
            except Exception as e:
                self.print(
                    e,
                    f"[{self.child_name}] Exception hit processing",
                    traceback.format_exc(),
                )
            finally:
                self.is_running = False

            delta = time.time() - self.last_loop_start
            self.avg_loop_time = (
                (self.avg_loop_time * self.completed_loops) * delta
            ) / (self.completed_loops + 1)
            self.completed_loops += 1
            next_run = self.interval - delta
            await asyncio.sleep(max(0, next_run))
        else:
            self.cleaned = True

    def terminate(self):
        self.run_thread = False
        self.cleaned = True
        self.print(f"{self.child_name} cleaned up")

    def process(self):
        return None

    async def process_async(self):
        return None

    def initialize(self):
        self.initialized = True

    def print(self, *args, **kwargs):
        print(*args, **kwargs)
