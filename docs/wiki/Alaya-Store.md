# 🏛️ 阿赖耶识存储

阿赖耶识（Ālaya-vijñāna，आलयविज्ञान）是唯识学的核心概念，意为"藏识"——储藏一切种子的仓库。Yogacara将其实现为持久化存储系统。

## 概念理解

在唯识学中：
- **阿赖耶识** = 第八识 = 藏识 = 种子仓库
- 它储藏过去所有经验留下的种子
- 这些种子在条件成熟时会显现为当前行为
- 它是连接过去、现在、未来的桥梁

在Yogacara中：
- `AlayaStore` = 持久化存储类
- 负责种子的存取、检索、持久化
- 支持多种存储后端

## 基本使用

### 初始化

```python
from yogacara import AlayaStore

# 默认使用文件存储
alaya = AlayaStore()

# 指定存储路径
alaya = AlayaStore(path="./my_agent_memory")

# 使用自定义存储后端
alaya = AlayaStore(backend=CustomBackend())
```

### 存储种子

```python
from yogacara import Seed, SeedType

seed = Seed(
    content="用户喜欢Python",
    seed_type=SeedType.PREFERENCE,
    strength=0.8
)

# 存储种子
alaya.store_seed(seed)
```

### 检索种子

```python
# 获取所有种子
all_seeds = alaya.get_all_seeds()

# 按类型检索
preferences = alaya.get_seeds_by_type(SeedType.PREFERENCE)

# 按关键词检索
results = alaya.search_seeds("Python")

# 按强度过滤
strong_seeds = alaya.get_seeds_above_strength(0.7)
```

### 持久化

```python
# 保存状态到磁盘
alaya.save()

# 从磁盘加载状态
alaya.load()

# 清空存储
alaya.clear()
```

## 存储结构

```
阿赖耶识存储
│
├── seeds/                    # 种子数据
│   ├── {seed_id_1}.json
│   ├── {seed_id_2}.json
│   └── ...
│
├── indices/                  # 索引文件
│   ├── by_type.json          # 按类型索引
│   ├── by_strength.json      # 按强度索引
│   └── by_time.json          # 按时间索引
│
├── metadata/                 # 元数据
│   ├── agent_info.json       # Agent信息
│   ├── awakening_state.json  # 觉醒状态
│   └── statistics.json       # 统计信息
│
└── config.json               # 存储配置
```

## 存储后端

Yogacara支持多种存储后端：

### 文件系统（默认）

```python
from yogacara import AlayaStore

alaya = AlayaStore(
    backend="filesystem",
    path="./agent_memory"
)
```

优点：简单、无需额外依赖
缺点：不适合大规模并发

### SQLite

```python
alaya = AlayaStore(
    backend="sqlite",
    path="./agent_memory.db"
)
```

优点：支持查询、适合中等规模
缺点：单机限制

### Redis

```python
alaya = AlayaStore(
    backend="redis",
    host="localhost",
    port=6379,
    db=0
)
```

优点：高性能、支持分布式
缺点：需要Redis服务

### 自定义后端

```python
from yogacara import StorageBackend

class MyBackend(StorageBackend):
    def store(self, key, value):
        # 自定义存储逻辑
        pass
    
    def retrieve(self, key):
        # 自定义检索逻辑
        pass

alaya = AlayaStore(backend=MyBackend())
```

## 数据迁移

### 导出数据

```python
# 导出为JSON
alaya.export("backup.json")

# 导出为压缩包
alaya.export("backup.tar.gz", format="tar.gz")
```

### 导入数据

```python
# 从JSON导入
alaya.import_from("backup.json")

# 合并导入（不覆盖已有）
alaya.merge_from("other_backup.json")
```

## 统计与分析

```python
# 获取统计信息
stats = alaya.get_statistics()

print(f"总种子数: {stats['total_seeds']}")
print(f"各类型分布: {stats['by_type']}")
print(f"平均强度: {stats['avg_strength']}")
print(f"存储大小: {stats['storage_size']}")

# 获取种子活跃度
activity = alaya.get_activity_report()
```

## 性能优化

### 索引优化

```python
# 创建索引
alaya.create_index("seed_type")
alaya.create_index("strength")
alaya.create_index("created_at")

# 查询时使用索引
results = alaya.query(
    seed_type=SeedType.PREFERENCE,
    min_strength=0.5
)
```

### 批量操作

```python
# 批量存储
seeds = [seed1, seed2, seed3]
alaya.store_seeds_batch(seeds)

# 批量检索
seed_ids = [id1, id2, id3]
seeds = alaya.get_seeds_batch(seed_ids)
```

### 缓存策略

```python
# 启用内存缓存
alaya = AlayaStore(cache_size=1000)

# 清理缓存
alaya.clear_cache()
```

## 安全考虑

### 数据加密

```python
# 启用加密存储
alaya = AlayaStore(
    encrypt=True,
    encryption_key="your-secret-key"
)
```

### 访问控制

```python
# 设置访问权限
alaya.set_permission(
    seed_id=seed.id,
    access_level="private"
)
```

## 与种子系统集成

```python
from yogacara import SeedSystem, AlayaStore

# 初始化
seed_system = SeedSystem()
alaya = AlayaStore()

# 植入种子时自动存储
seed_system.plant_seed(
    content="用户偏好简洁回复",
    seed_type=SeedType.PREFERENCE,
    store=alaya  # 自动存储到阿赖耶识
)

# 激活时从阿赖耶识加载
context = {"user_input": "请简短回答"}
activated = seed_system.activate_seeds(
    context,
    store=alaya  # 从存储加载
)
```
