"""
Usage:

```
@require_lock
def test():
    global n
    for _ in range(1000000):
        n += 1

@require_lock
def test2():
    test()

n = 0

thr1 = threading.Thread(target=test)
thr2 = threading.Thread(target=test2)
thr1.start()
thr2.start()
thr1.join()
thr2.join()

print(n)
```
"""

from __future__ import annotations

import threading
from typing import Any, Callable, Literal, Protocol, TypeVar, overload

GLOBAL_LOCK = threading.RLock()

AnyFunc = TypeVar('AnyFunc', bound=Callable)


class LockProtocol(Protocol):
    def acquire(self, blocking=True, timeout=-1) -> bool | Literal[1]:
        ...

    def release(self) -> None:
        ...


@overload
def lock_required(func: AnyFunc, lock: LockProtocol = GLOBAL_LOCK) -> AnyFunc:
    ...


@overload
def lock_required(func=None, lock: LockProtocol = GLOBAL_LOCK) -> Callable[[AnyFunc], AnyFunc]:
    ...


def lock_required(func: AnyFunc | None = None,
                  lock: LockProtocol = GLOBAL_LOCK) -> AnyFunc | Callable[[AnyFunc], AnyFunc]:
    if func is None:

        def get_func(__func: AnyFunc):
            return lock_required(__func)

        return get_func

    def wrapper(*args, **kwds) -> Any:
        lock.acquire()
        try:
            result = func(*args, **kwds)
        except Exception:
            result = None
        finally:
            lock.release()
        return result

    wrapper.__name__ = func.__name__
    return wrapper
