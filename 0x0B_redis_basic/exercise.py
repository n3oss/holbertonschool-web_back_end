#!/usr/bin/env python3
"""Redis basic exercise: Cache class."""
from functools import wraps
from typing import Any, Callable, Optional, Union, cast
import uuid
import redis


def count_calls(method: Callable) -> Callable:
    """Count how many times a method is called using Redis."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Store the history of inputs and outputs for a method."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(inputs_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, str(output))
        return output
    return wrapper


def replay(method: Callable) -> None:
    """Display the call history of a method."""
    # Access the Redis instance from the bound method's self
    redis_client = method.__self__._redis
    qualname = method.__qualname__

    count = int(redis_client.get(qualname) or 0)
    print(f"{qualname} was called {count} times:")

    inputs = redis_client.lrange(f"{qualname}:inputs", 0, -1)
    outputs = redis_client.lrange(f"{qualname}:outputs", 0, -1)

    for inp, out in zip(inputs, outputs):
        input_str = inp.decode("utf-8")
        output_str = out.decode("utf-8")
        print(f"{qualname}(*{input_str}) -> {output_str}")


class Cache:
    """Simple Redis-backed cache."""

    def __init__(self) -> None:
        """Initialize Redis client and flush existing data."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data under a random key and return the key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self,
        key: str,
        fn: Optional[Callable[[bytes], Union[str, bytes, int, float]]] = None,
    ) -> Union[str, bytes, int, float, None]:
        """Retrieve data by key and optionally convert it with fn."""
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is None:
            return value
        return fn(value)

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve a UTF-8 decoded string value by key."""
        return cast(Optional[str], self.get(key, fn=lambda d: d.decode("utf-8")))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve an integer value by key."""
        return cast(Optional[int], self.get(key, fn=int))
