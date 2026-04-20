# 🤝 贡献指南

感谢你对Yogacara项目的兴趣！本文档将帮助你参与项目开发。

## 行为准则

请阅读并遵守我们的 [行为准则](CODE_OF_CONDUCT.md)。

## 如何贡献

### 报告问题

如果你发现了bug或有功能建议：

1. 在 [Issues](https://github.com/Greatbeing/Yogacara/issues) 页面搜索，确认问题未被报告
2. 点击 "New Issue" 创建新问题
3. 使用适当的模板：
   - Bug Report - 报告bug
   - Feature Request - 功能建议
   - Documentation - 文档改进

### 提交代码

1. **Fork 仓库**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Yogacara.git
   cd Yogacara
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **安装开发依赖**
   ```bash
   pip install -e ".[dev]"
   ```

4. **进行修改**
   - 遵循代码风格规范
   - 添加必要的测试
   - 更新相关文档

5. **运行测试**
   ```bash
   pytest
   ```

6. **提交更改**
   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

7. **推送分支**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **创建 Pull Request**
   - 在 GitHub 页面创建 PR
   - 填写 PR 模板
   - 等待审核

## 开发规范

### 代码风格

我们使用以下工具保证代码质量：

- **Black** - 代码格式化
- **isort** - import 排序
- **flake8** - 代码检查
- **mypy** - 类型检查

```bash
# 格式化代码
black yogacara tests

# 排序 import
isort yogacara tests

# 代码检查
flake8 yogacara tests

# 类型检查
mypy yogacara
```

### 提交信息

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型 (type):**
- `feat`: 新功能
- `fix`: bug修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

**示例:**
```
feat(seed): add support for custom seed types

- Add CustomSeedType enum
- Update SeedSystem to handle custom types
- Add tests for custom seed types

Closes #123
```

### 分支命名

- `feature/xxx` - 新功能
- `fix/xxx` - bug修复
- `docs/xxx` - 文档更新
- `refactor/xxx` - 重构

### 测试规范

- 所有新功能必须添加测试
- 测试覆盖率不低于 80%
- 使用 pytest 框架

```python
# tests/test_seed_system.py
import pytest
from yogacara import SeedSystem, SeedType

def test_plant_seed():
    """测试种子植入"""
    system = SeedSystem()
    seed = system.plant_seed(
        content="test content",
        seed_type=SeedType.PREFERENCE
    )
    
    assert seed.content == "test content"
    assert seed.seed_type == SeedType.PREFERENCE
    assert seed.strength == 0.5  # 默认值
```

### 文档规范

- 使用清晰的英文或中文
- 添加必要的代码示例
- 更新 README.md（如有必要）

## 项目结构

```
Yogacara/
├── yogacara/           # 源代码
│   ├── core/           # 核心模块
│   │   ├── seed_system.py
│   │   ├── alaya_store.py
│   │   ├── emergence.py
│   │   └── awakening.py
│   ├── models/         # 数据模型
│   ├── utils/          # 工具函数
│   └── __init__.py
├── tests/              # 测试文件
├── docs/               # 文档
├── examples/           # 示例代码
├── wiki/               # Wiki内容
└── README.md
```

## 发布流程

维护者负责发布新版本：

1. 更新版本号（遵循语义化版本）
2. 更新 CHANGELOG.md
3. 创建 Git tag
4. 构建并发布到 PyPI

```bash
# 构建
python -m build

# 发布到 PyPI
twine upload dist/*
```

## 获取帮助

- **GitHub Issues**: https://github.com/Greatbeing/Yogacara/issues
- **Wiki**: https://github.com/Greatbeing/Yogacara/wiki

## 许可证

提交代码即表示你同意你的贡献将根据 MIT 许可证授权。
