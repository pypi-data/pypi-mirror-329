from __future__ import annotations

import queue
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Iterable, TypeVar, overload


def on_error(exc: Exception):
    print(
        "--------------------------------------------------\n" +
        "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)) +
        "\n--------------------------------------------------"
    )


class Task:
    """Basic task."""

    event_type = threading.Event

    def __init__(self, target: Callable | None = None, *, args: Iterable = (), kwds: dict | None = None):
        self.target = target
        self.args = args
        self.kwargs = kwds if kwds else {}
        self.result = None
        self.exc = None
        self.finished = self.event_type()

    def __call__(self):
        try:
            self.result = self.run()
        except Exception as exc:
            self.exc = exc
            on_error(exc)
        finally:
            self.finished.set()

    def run(self) -> Any:
        if self.target is None:
            return None
        return self.target(*self.args, **self.kwargs)

    def wait(self, timeout: float | None = None):
        return self.finished.wait(timeout=timeout)

    def set_default(self, default):
        self.result = default

    @property
    def noerror(self):
        """Not error."""
        return self.exc is None


class TaskRunner:
    """The threading safe unified execution.

    Usage:
    ```
    with TaskRunner() as tr:
        tr.submit(print, args=("Ln1: Hello World",))
        tr.put(lambda: print("Ln1: Hello World"))
    ```

    ```
    tr = TaskRunner()
    @tr.putter
    def test():
        pass
    test()
    tr.close()
    tr.join()
    ```
    """
    def __init__(self):
        self.queue: queue.Queue[Callable | None] = queue.Queue()
        self.thr = threading.Thread(target=self.mainloop, daemon=True)
        self.started = False
        self.alive = threading.Event()
        self.ended = threading.Event()
        self.ended.set()

    def __enter__(self):
        if not self.started:
            self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        self.ended.wait()

    def run(self):
        while self.alive.is_set():
            task = self.queue.get()
            if task is None:
                self.alive.clear()
                break
            task()

    def mainloop(self):
        self.run()
        self.ended.set()

    def start(self):
        """Start the threading."""
        self.started = True
        self.ended.clear()
        self.alive.set()
        self.thr.start()

    def close(self):
        """TaskRunner will closed after all task terminated."""
        self.queue.put(None)

    def stop(self):
        """TaskRunner will closed after current task terminated."""
        self.alive.clear()
        self.close()

    def join(self):
        """Wait the TaskRunner terminated."""
        self.ended.wait()

    def put(self, func: Callable[[], Any]):
        """Put a callable to queue."""
        def wrapper():
            try:
                func()
            except Exception as exc:
                on_error(exc)

        self.queue.put(wrapper)

    def putter(self, func: Callable):
        """A decorator of `.put`."""
        return lambda *a, **kwa: self.put(lambda: func(*a, **kwa))

    def submit(self, func: Callable, args: Iterable = (), kwds: dict | None = None, *, default=None, handler=Task):
        """Put a Task to queue."""
        task = handler(func, args=args, kwds=kwds)
        if default is not None:
            task.result = default
        self.queue.put(task)
        return task

    Handler = TypeVar('Handler', bound=Task)

    @overload
    def submitter(self, *, default=None, handler: type[Handler] = Task) -> Callable[[Callable], Callable[..., Handler]]:
        ...

    @overload
    def submitter(self, func: Callable, *, default=None, handler: type[Handler] = Task) -> Callable[..., Handler]:
        ...

    def submitter(self, func=None, *, default=None, handler=Task) -> Any:
        """A decorator of `.run`."""
        if func is None:
            return lambda f: self.submitter(f, default=default, handler=handler)
        return lambda *a, **kwa: self.submit(func, a, kwa, default=default, handler=handler)

    def proxy(self, *, default=None, handler=Task):
        def get_func(func: Callable):
            def wrapper(*args, **kwds):
                task = self.submit(func, args=args, kwds=kwds, default=default, handler=handler)
                task.wait()
                return task.result

            return wrapper

        return get_func


class ThreadTaskRunner(TaskRunner):
    def __init__(self):
        super().__init__()
        self.thread_count = 4

    def run(self):
        with ThreadPoolExecutor(self.thread_count) as pool:
            while self.alive.is_set():
                task = self.queue.get()
                if task is None:
                    self.alive.clear()
                    break
                pool.submit(task)
