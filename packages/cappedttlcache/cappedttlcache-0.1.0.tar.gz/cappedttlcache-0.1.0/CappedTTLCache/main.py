# -*- coding:utf-8 -*-
"""
@Created on : 2024/5/8 23:01
@Author: XDTEAM
@Des: 通用缓存数据存储
"""
import asyncio
from typing import Optional, Dict, Callable, Awaitable, List, TypeVar

CacheListener = Callable[[], Awaitable[None]]
_T = TypeVar("_T")


class CappedTTLCache:
    def __init__(self, max_items: int, ttl_seconds: int) -> None:
        """
        作用: 构造函数，初始化 CappedTTLCache 实例。
        参数:
            max_items (int): 存储的最大条目数。
            ttl_seconds (int): 缓存条目的有效时间（以秒为单位）。
        """
        self.max_items = max_items
        self.ttl_seconds = ttl_seconds
        self.cache: Dict[str, Dict] = {}
        self.last_refresh_time: Dict[str, float] = {}
        self.listeners: set[CacheListener] = set()

    async def add_item(self, key: str, value: _T) -> None:
        """
        作用: 添加一个新的缓存条目到存储中，并安排在一定时间后自动删除该条目。
        参数:
            key (str): 缓存条目的唯一标识符。
            value (_T): 要添加的缓存条目。
        """
        if key in self.cache:
            self.cache[key] = value  # 更新现有条目
        else:
            if len(self.cache) >= self.max_items:
                await self.prune_cache()  # 修剪缓存以保持最大条目数
            self.cache[key] = value
        self.last_refresh_time[key] = asyncio.get_event_loop().time()
        await self._notify_listeners()

        # 安排在一定时间后自动删除该条目
        asyncio.get_event_loop().call_later(self.ttl_seconds, self.remove_item, key)

    async def prune_cache(self) -> None:
        """
        作用: 如果缓存总数超出限制，删除最旧的缓存条目。
        """
        while len(self.cache) > self.max_items:
            oldest_key = min(self.last_refresh_time, key=self.last_refresh_time.get)
            self.remove_item(oldest_key)

    def get_item(self, key: str) -> Optional[_T]:
        """
        作用: 根据标识符获取特定的缓存条目。
        参数:
            key (str): 要获取的缓存条目的唯一标识符。
        返回值: 如果存在，返回缓存条目；否则返回 None。
        """
        return self.cache.get(key)

    def get_last_refresh_time(self, key: str) -> Optional[_T]:
        """
        作用: 根据标识符获取上一次更新时间。
        参数:
            key (str): 要获取的缓存条目的唯一标识符。
        返回值: 如果存在，返回更新时间；否则返回 None。
        """
        return self.last_refresh_time.get(key)

    def get_items(self, *, reverse: bool = False, count: int = 0) -> List[_T]:
        """
        作用: 获取当前存储的所有缓存条目，可以选择性地按相反顺序排序和限制返回的条目数量。
        参数:
            reverse (bool): 是否将条目按相反顺序排序，默认为 False。
            count (int): 返回的条目数量限制，默认为0，表示返回所有条目。
        返回值: 包含缓存条目的列表。
        """
        items = list(self.cache.items())
        items.sort(key=lambda x: self.last_refresh_time[x[0]], reverse=reverse)
        return items[-count:] if count else items

    def get_count(self) -> int:
        """
        作用: 获取当前存储中的缓存条目数量。
        返回值: 缓存条目数量的整数。
        """
        return len(self.cache)

    def remove_item(self, key: str) -> None:
        """
        作用: 从存储中移除一个指定标识的缓存条目。
        参数:
            key (str): 要移除的缓存条目的唯一标识符。
        """
        self.cache.pop(key, None)
        self.last_refresh_time.pop(key, None)

    def register_listener(self, listener: CacheListener) -> None:
        """
        作用: 注册一个新的缓存监听器，当缓存更新时，注册的监听器将被通知。
        参数:
            listener (CacheListener): 一个符合 CacheListener 签名的可调用对象。
        """
        self.listeners.add(listener)

    def unregister_listener(self, listener: CacheListener) -> None:
        """
        作用: 注销一个已经注册的缓存监听器。
        参数:
            listener (CacheListener): 要注销的监听器。
        """
        self.listeners.remove(listener)

    async def _notify_listeners(self) -> None:
        """
        作用: 异步通知所有注册的监听器，缓存已更新。
        """
        await asyncio.gather(
            *[listener() for listener in self.listeners], return_exceptions=True
        )