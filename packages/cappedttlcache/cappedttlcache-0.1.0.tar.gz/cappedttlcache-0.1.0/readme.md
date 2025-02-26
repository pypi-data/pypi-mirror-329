
# CappedTTLCache

这是一个用于管理和缓存数据的 Python 模块。该模块支持通用缓存数据存储，具有最大条目数和条目有效时间的限制。

## 特性

- 支持设置最大缓存条目数
- 支持设置缓存条目的有效时间（TTL）
- 自动删除过期条目
- 支持获取当前存储的所有缓存条目
- 支持根据标识符获取特定的缓存条目
- 支持获取当前存储中的缓存条目数量
- 支持注册和注销监听器，以便在数据更新时执行特定操作

## 安装

确保你已经安装了 Python 3.7 或更高版本

## 使用说明

### 1. 导入模块

首先，导入 `CappedTTLCache` 类：

```python
from CappedTTLCache import CappedTTLCache  # 假设你的模块名为 CappedTTLCache.py
```

### 2. 创建缓存实例

创建一个 `CappedTTLCache` 实例，指定最大条目数和缓存条目的有效时间（以秒为单位）：

```python
cache = CappedTTLCache(max_items=5, ttl_seconds=10)
```

### 3. 添加缓存条目

使用 `add_item` 方法添加一个新的缓存条目到存储中：

```python
await cache.add_item("item1", "这是第一个缓存条目")
```

### 4. 获取缓存条目

使用 `get_items` 方法获取当前存储的所有缓存条目，可以选择性地按相反顺序排序和限制返回的条目数量：

```python
items = cache.get_items(reverse=True, count=3)
print(items)
```

### 5. 根据标识符获取特定的缓存条目

使用 `get_item` 方法s：

```python
items = cache.get_item(key="item1")
print(items)
```

### 6. 获取缓存条目数量

使用 `get_count` 方法获取当前存储中的缓存条目数量：

```python
count = cache.get_count()
print(f"当前缓存条目数量: {count}")
```

### 7. 移除缓存条目

使用 `remove_item` 方法从存储中移除一个指定标识的缓存条目：

```python
cache.remove_item("item1")
```

### 8. 注册监听器

定义一个异步函数作为监听器，当缓存更新时，该函数将被调用：

```python
async def cache_update_listener():
    print("缓存数据已更新！")
```

使用 `register_listener` 方法将监听器添加到 `CappedTTLCache` 实例中：

```python
cache.register_listener(cache_update_listener)
```

### 9. 注销监听器

如果不再需要某个监听器，可以使用 `unregister_listener` 方法将其移除：

```python
cache.unregister_listener(cache_update_listener)
```

### 10. 示例代码

以下是一个完整的示例，演示了如何使用 `CappedTTLCache`：

```python
import asyncio
from CappedTTLCache import CappedTTLCache

async def cache_update_listener():
    print("缓存数据已更新！")

async def main():
    # 创建缓存实例
    cache = CappedTTLCache(max_items=5, ttl_seconds=10)

    # 注册监听器
    cache.register_listener(cache_update_listener)

    # 添加缓存条目
    await cache.add_item("item1", "这是第一个缓存条目")
    await cache.add_item("item2", "这是第二个缓存条目")

    # 获取缓存条目
    items = cache.get_items()
    print("当前缓存条目:", items)

    # 获取缓存条目数量
    count = cache.get_count()
    print(f"当前缓存条目数量: {count}")

    # 等待一段时间后查看缓存条目
    await asyncio.sleep(5)
    items = cache.get_items()
    print("5秒后缓存条目:", items)

    # 等待超过缓存时间，查看缓存条目
    await asyncio.sleep(6)
    items = cache.get_items()
    print("超过TTL后的缓存条目:", items)

    # 注销监听器
    cache.unregister_listener(cache_update_listener)

# 运行示例
# asyncio.run(main())
```

## API 说明

### `CappedTTLCache(max_items: int, ttl_seconds: int)`

- **参数**:
  - `max_items`: 存储的最大条目数（整数）。
  - `ttl_seconds`: 缓存条目的有效时间（以秒为单位）。

### `