import functools
import time
from typing import Any, Callable, Optional, TypeVar

C = TypeVar("C", bound=Callable)


def async_timed_cache(seconds: int, maxsize: Optional[int] = None) -> Callable[[C], C]:
    def wrapper_cache(func: C) -> C:
        cache: dict[str, Any] = {}
        setattr(func, "__lifetime", seconds)
        setattr(func, "__expiration", time.time() + getattr(func, "__lifetime"))

        @functools.wraps(func)
        async def wrapped_func(*args, **kwargs):
            key = str(args) + str(kwargs)

            if time.time() >= getattr(func, "__expiration"):
                cache.clear()
                setattr(func, "__expiration", time.time() + getattr(func, "__lifetime"))

            if key in cache:
                # Move the item to the end to mark it as recently used
                cache[key] = cache.pop(key)
                return cache[key]

            result = await func(*args, **kwargs)

            if maxsize is not None and len(cache) >= maxsize:
                # Remove the least recently used item (first item in the dict)
                cache.pop(next(iter(cache)))

            cache[key] = result
            return result

        def clear_cache():
            cache.clear()
            setattr(func, "__expiration", time.time() + getattr(func, "__lifetime"))

        setattr(wrapped_func, "clear_cache", clear_cache)
        return wrapped_func  # type: ignore

    return wrapper_cache
