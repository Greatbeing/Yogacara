# 📦 安装指南

## 系统要求

- **Python**: 3.9 或更高版本
- **操作系统**: Linux, macOS, Windows

## 安装方式

### 方式一：PyPI安装（推荐）

```bash
pip install yogacara
```

### 方式二：从源码安装

```bash
# 克隆仓库
git clone https://github.com/Greatbeing/Yogacara.git
cd Yogacara

# 安装依赖
pip install -e .
```

### 方式三：开发模式安装

```bash
git clone https://github.com/Greatbeing/Yogacara.git
cd Yogacara

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest
```

## 依赖项

Yogacara依赖以下核心库：

| 依赖 | 版本 | 用途 |
|------|------|------|
| `pydantic` | ≥2.0 | 数据验证与模型 |
| `typing-extensions` | ≥4.0 | 类型扩展 |

## 验证安装

```python
import yogacara
print(yogacara.__version__)
```

## 常见问题

### Q: 为什么需要Python 3.9+？

A: Yogacara使用了pydantic v2，它需要Python 3.9或更高版本。

### Q: 安装失败怎么办？

A: 尝试升级pip：
```bash
pip install --upgrade pip
pip install yogacara
```

### Q: 如何卸载？

```bash
pip uninstall yogacara
```
