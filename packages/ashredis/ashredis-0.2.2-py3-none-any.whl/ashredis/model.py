from __future__ import annotations
from typing import Any, Type
from time import time
from datetime import timedelta

import redis.asyncio as async_redis
import functools
import json


def with_redis_connection(func: Callable[..., Coroutine]) -> Callable[..., Coroutine]:
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        is_wraps_connection = None
        if not self._redis:
            is_wraps_connection = True
            self._redis = await async_redis.Redis(**self._connection_params)
        try:
            result = await func(self, *args, **kwargs)
            return result
        finally:
            if is_wraps_connection is not None:
                await self._redis.aclose()
                self._redis = None
    return wrapper


class RedisObject:
    def __init__(self, host: str, port: int, password: str, db: int, key: str | int = None):
        self._connection_params = {
            "host": host,
            "port": port,
            "password": password,
            "db": db,
            "decode_responses": True
        }
        self.key = key
        self._redis = None
        self._data = {}
        self._fields = {}

        self.__parse_fields()
        self.__parse_configure()


    async def __aenter__(self):
        self._redis = await async_redis.Redis(**self._connection_params).__aenter__()
        return self


    async def __aexit__(self, *args):
        await self._redis.__aexit__(*args)


    @classmethod
    def typed_property(cls, key_name: str, data_type: Type):
        def getter(self) -> Any:
            data = self._data.get(key_name)
            if data is None:
                return None
            elif data_type == bool:
                return bool(data)
            elif data_type in (dict, list):
                return json.loads(data)
            return data

        def setter(self, value: Any):
            if value is None:
                self._data[key_name] = None
            elif data_type == bool:
                self._data[key_name] = int(value)
            elif data_type in (dict, list):
                self._data[key_name] = json.dumps(value)
            elif isinstance(value, data_type):
                self._data[key_name] = value
            else:
                raise TypeError(
                    f"Field '{key_name}' expected type {data_type.__name__}, "
                    f"but got value '{value}' of type {type(value).__name__}."
                )

        return property(getter, setter)


    def __parse_fields(self):
        if not hasattr(self, "__annotations__"):
            return

        for field_name, field_type in self.__annotations__.items():
            self._fields[field_name] = field_type
            setattr(self.__class__, field_name, self.typed_property(field_name, field_type))


    def __parse_configure(self):
        if not hasattr(self, '__category__'):
            raise AttributeError(f"{self.__class__.__name__} must define '__category__' attribute.")

        if self.key is None:
            self.key = getattr(self, '__default_key__', None)


    def __converted_data(self, key: str, value: str):
        type_mapping = {
            int: int,
            float: float,
            list: json.loads,
            dict: json.loads,
            bool: lambda x: bool(int(x)),
        }

        value_type = self._fields[key]
        value = type_mapping.get(value_type, lambda x: x)(value)
        setattr(self, key, value)


    async def __get_all_keys(self, offset: int = None, limit: int = None) -> list:
        all_keys = []
        cursor = 0
        while True:
            cursor, keys = await self._redis.scan(cursor, match=f"{self.__category__}:*")
            all_keys.extend(keys)
            if cursor == 0:
                break

        return all_keys[offset:][:limit]


    def copy_data(self, category: RedisObject):
        self._data = category._data


    @with_redis_connection
    async def load(self, key: str | int = None) -> bool:
        self.key = key or self.key
        if self.key is None:
            raise ValueError("key does not exist")

        result = await self._redis.hgetall(name=f"{self.__category__}:{self.key}")

        for key, value in result.items():
            self.__converted_data(key=key, value=value)

        if self._data:
            return True


    @with_redis_connection
    async def load_all(self, offset: int = None, limit: int = None) -> list:
        all_keys = await self.__get_all_keys(offset=offset, limit=limit)
        categories = []

        for key in all_keys:
            result = await self._redis.hgetall(name=key)
            key = key.split(":")[-1]

            item = type(self)()
            item.key = int(key) if key.isdigit() else key
            for k, v in result.items():
                item.__converted_data(key=k, value=v)

            categories.append(item)

        return categories


    @with_redis_connection
    async def load_for_time(
            self, ts_field: str, range_day: int = 0, range_hour: int = 0, range_min: int = 0, range_sec: int = 0,
            range_ms: int = 0, offset: int = None, limit: int = None, reverse_sorted: bool = False) -> list:
        time_delta = timedelta(
            days=range_day, hours=range_hour, minutes=range_min, seconds=range_sec, milliseconds=range_ms)
        ts_by_range = int(time() * 1000) - int(time_delta.total_seconds() * 1000)
        all_keys = await self.__get_all_keys()
        categories = []

        for key in all_keys:
            result = await self._redis.hgetall(name=key)
            key = key.split(":")[-1]

            item = type(self)()
            item.key = int(key) if key.isdigit() else key
            for k, v in result.items():
                item.__converted_data(key=k, value=v)

            ts = item._data.get(ts_field)
            if ts and ts > ts_by_range:
                categories.append(item)

        sorted_categories = sorted(categories, key=lambda i: i._data[ts_field], reverse=not reverse_sorted)
        return sorted_categories[offset:][:limit]


    @with_redis_connection
    async def load_sorted(self, sort_field: str, reverse_sorted: bool = False, offset: int = None, limit: int = None):
        all_keys = await self.__get_all_keys()
        categories = []

        for key in all_keys:
            result = await self._redis.hgetall(name=key)
            key = key.split(":")[-1]

            item = type(self)()
            item.key = int(key) if key.isdigit() else key
            for k, v in result.items():
                item.__converted_data(key=k, value=v)

            if sort_field in item._data:
                categories.append(item)

        sorted_categories = sorted(categories, key=lambda i: i._data[sort_field], reverse=not reverse_sorted)
        return sorted_categories[offset:][:limit]


    @with_redis_connection
    async def save(self, key: str | int = None, ttl_day: int = 0, ttl_hour: int = 0, ttl_min: int = 0, ttl_sec: int = 0):
        self.key = key or self.key
        if self.key is None:
            raise ValueError("key does not exist")

        hash_key = f"{self.__category__}:{self.key}"

        data_to_store = {key: value for key, value in self._data.items() if value is not None}
        if data_to_store:
            await self._redis.hset(name=hash_key, mapping=data_to_store)

        fields_to_remove = [key for key, value in self._data.items() if value is None]
        if fields_to_remove:
            await self._redis.hdel(hash_key, *fields_to_remove)

        time_delta = timedelta(days=ttl_day, hours=ttl_hour, minutes=ttl_min, seconds=ttl_sec)
        ttl_seconds = int(time_delta.total_seconds())
        if ttl_seconds:
            await self._redis.expire(name=hash_key, time=ttl_seconds)


    @with_redis_connection
    async def delete(self, key: str | int = None) -> bool:
        self.key = key or self.key
        if self.key is None:
            raise ValueError("key does not exist")

        result = await self._redis.delete(f"{self.__category__}:{self.key}")
        if result:
            return True


    @with_redis_connection
    async def get_ttl(self, key: str | int = None) -> int:
        self.key = key or self.key
        if self.key is None:
            raise ValueError("key does not exist")

        ttl = await self._redis.ttl(f"{self.__category__}:{self.key}")
        if ttl != -2:
            return ttl
