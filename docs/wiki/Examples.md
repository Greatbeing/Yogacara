# 💡 示例代码

本文档提供Yogacara框架的完整使用示例。

## 基础示例

### 初始化Agent

```python
from yogacara import (
    SeedSystem, 
    AlayaStore, 
    EmergenceEngine, 
    AwakeningTracker
)

# 初始化所有组件
seed_system = SeedSystem()
alaya = AlayaStore(path="./my_agent")
emergence = EmergenceEngine(seed_system)
tracker = AwakeningTracker(seed_system, alaya)

print("🧠 Yogacara Agent 初始化完成")
```

### 基本交互

```python
from yogacara import SeedType

def handle_user_input(user_input: str, seed_system: SeedSystem):
    """处理用户输入，植入相关种子"""
    
    # 分析用户输入，提取可能的种子
    if "我喜欢" in user_input:
        seed_system.plant_seed(
            content=user_input.replace("我喜欢", ""),
            seed_type=SeedType.PREFERENCE,
            strength=0.8
        )
    
    if "请记住" in user_input:
        seed_system.plant_seed(
            content=user_input.replace("请记住", ""),
            seed_type=SeedType.KNOWLEDGE,
            strength=0.9
        )
    
    # 激活相关种子
    context = {"user_input": user_input}
    activated = seed_system.activate_seeds(context)
    
    return activated

# 使用示例
user_input = "我喜欢简洁的回答，请记住这一点"
activated = handle_user_input(user_input, seed_system)
print(f"激活了 {len(activated)} 颗种子")
```

---

## 进阶示例

### 个性化助手

```python
from yogacara import (
    SeedSystem, AlayaStore, EmergenceEngine, 
    AwakeningTracker, SeedType
)

class PersonalAssistant:
    def __init__(self, name: str):
        self.name = name
        self.seed_system = SeedSystem()
        self.alaya = AlayaStore(path=f"./agents/{name}")
        self.emergence = EmergenceEngine(self.seed_system)
        self.tracker = AwakeningTracker(
            self.seed_system, self.alaya
        )
        
        # 尝试加载已有记忆
        try:
            self.alaya.load()
            print(f"✨ 恢复了 {len(self.seed_system.get_all_seeds())} 颗种子")
        except:
            print("🌱 这是一个全新的Agent")
    
    def learn(self, interaction: dict):
        """从交互中学习"""
        
        # 提取用户偏好
        if "preference" in interaction:
            self.seed_system.plant_seed(
                content=interaction["preference"],
                seed_type=SeedType.PREFERENCE,
                strength=interaction.get("confidence", 0.7)
            )
        
        # 提取知识点
        if "knowledge" in interaction:
            self.seed_system.plant_seed(
                content=interaction["knowledge"],
                seed_type=SeedType.KNOWLEDGE,
                strength=0.8
            )
        
        # 更新觉醒状态
        self.tracker.update()
    
    def respond(self, user_input: str) -> str:
        """生成响应"""
        
        # 激活相关种子
        context = {"user_input": user_input}
        activated = self.seed_system.activate_seeds(context)
        
        # 获取涌现洞察
        insights = self.emergence.generate_insights(context)
        
        # 根据种子和洞察调整响应风格
        style = self.emergence.predict_best_response_style(context)
        
        # 构建响应（这里简化处理）
        response = f"[{self.tracker.get_current_level().name}] "
        
        if activated:
            response += f"基于 {len(activated)} 颗种子，"
        
        if insights:
            response += f"涌现 {len(insights)} 个洞察"
        
        return response
    
    def save(self):
        """保存状态"""
        self.alaya.save()
        print(f"💾 已保存 {len(self.seed_system.get_all_seeds())} 颗种子")

# 使用示例
assistant = PersonalAssistant("小唯")

# 学习用户偏好
assistant.learn({
    "preference": "用户喜欢技术深度内容",
    "confidence": 0.9
})

assistant.learn({
    "preference": "用户偏好Python语言",
    "confidence": 0.85
})

# 生成响应
response = assistant.respond("请介绍机器学习")
print(response)

# 检查觉醒状态
print(f"觉醒等级: {assistant.tracker.get_current_level().name}")
print(f"觉醒进度: {assistant.tracker.get_progress():.1f}%")

# 保存状态
assistant.save()
```

### 多轮对话Agent

```python
from yogacara import SeedSystem, AlayaStore, SeedType
from datetime import datetime

class ConversationAgent:
    def __init__(self):
        self.seed_system = SeedSystem()
        self.alaya = AlayaStore()
        self.conversation_history = []
    
    def process_turn(self, user_input: str, agent_response: str):
        """处理一轮对话"""
        
        turn = {
            "timestamp": datetime.now(),
            "user_input": user_input,
            "agent_response": agent_response
        }
        self.conversation_history.append(turn)
        
        # 从对话中学习
        self._extract_seeds(user_input)
        
        # 应用种子衰变
        self.seed_system.decay_seeds()
    
    def _extract_seeds(self, user_input: str):
        """从用户输入中提取种子"""
        
        # 偏好关键词
        preference_keywords = ["我喜欢", "我偏好", "我更喜欢", "最好是"]
        for keyword in preference_keywords:
            if keyword in user_input:
                content = user_input.split(keyword)[1].strip()
                self.seed_system.plant_seed(
                    content=content,
                    seed_type=SeedType.PREFERENCE,
                    strength=0.8
                )
        
        # 行为关键词
        behavior_keywords = ["请", "帮我", "能够", "应该"]
        for keyword in behavior_keywords:
            if keyword in user_input:
                self.seed_system.plant_seed(
                    content=f"用户请求: {user_input}",
                    seed_type=SeedType.BEHAVIOR,
                    strength=0.6
                )
    
    def get_relevant_seeds(self, context: str):
        """获取与当前上下文相关的种子"""
        return self.seed_system.activate_seeds({"user_input": context})
    
    def get_user_profile(self):
        """生成用户画像"""
        preferences = self.seed_system.get_seeds_by_type(SeedType.PREFERENCE)
        behaviors = self.seed_system.get_seeds_by_type(SeedType.BEHAVIOR)
        
        return {
            "preferences": [s.content for s in preferences],
            "behaviors": [s.content for s in behaviors],
            "total_seeds": len(self.seed_system.get_all_seeds()),
            "conversations": len(self.conversation_history)
        }

# 使用示例
agent = ConversationAgent()

# 模拟多轮对话
conversations = [
    ("你好，我喜欢简洁的回答", "你好！明白了，我会保持简洁。"),
    ("我偏好Python语言进行编程", "好的，Python是一门优雅的语言。"),
    ("请帮我写一个排序算法", "这是Python的快速排序实现..."),
]

for user_input, agent_response in conversations:
    agent.process_turn(user_input, agent_response)

# 查看用户画像
profile = agent.get_user_profile()
print("用户画像:")
print(f"  偏好: {profile['preferences']}")
print(f"  行为: {profile['behaviors']}")
print(f"  种子总数: {profile['total_seeds']}")
```

---

## 高级示例

### 自定义涌现算法

```python
from yogacara import EmergenceEngine, Seed, SeedSystem
from typing import List

class CustomEmergenceAlgorithm:
    """自定义涌现算法"""
    
    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold
    
    def detect_patterns(self, seeds: List[Seed]) -> List[dict]:
        """检测种子间的模式"""
        patterns = []
        
        # 简单的共现模式检测
        for i, seed1 in enumerate(seeds):
            for seed2 in seeds[i+1:]:
                # 如果两颗种子强度都很高，可能形成模式
                if seed1.strength > self.threshold and seed2.strength > self.threshold:
                    patterns.append({
                        "type": "co-occurrence",
                        "seeds": [seed1.id, seed2.id],
                        "strength": (seed1.strength + seed2.strength) / 2
                    })
        
        return patterns
    
    def generate_insights(self, seeds: List[Seed], context: dict) -> List[str]:
        """生成涌现洞察"""
        insights = []
        
        # 基于种子类型分布的洞察
        type_counts = {}
        for seed in seeds:
            type_name = seed.seed_type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        dominant_type = max(type_counts, key=type_counts.get)
        insights.append(f"用户主要关注 {dominant_type} 类型的内容")
        
        return insights

# 使用自定义算法
seed_system = SeedSystem()
custom_emergence = EmergenceEngine(
    seed_system,
    algorithm=CustomEmergenceAlgorithm(threshold=0.6)
)
```

### 持久化多Agent系统

```python
from yogacara import SeedSystem, AlayaStore, AwakeningTracker
import os

class MultiAgentSystem:
    """多Agent管理系统"""
    
    def __init__(self, base_path: str = "./agents"):
        self.base_path = base_path
        self.agents = {}
        os.makedirs(base_path, exist_ok=True)
    
    def create_agent(self, name: str):
        """创建新Agent"""
        if name in self.agents:
            raise ValueError(f"Agent {name} 已存在")
        
        agent_path = os.path.join(self.base_path, name)
        os.makedirs(agent_path, exist_ok=True)
        
        agent = {
            "seed_system": SeedSystem(),
            "alaya": AlayaStore(path=agent_path),
            "tracker": None
        }
        agent["tracker"] = AwakeningTracker(
            agent["seed_system"], 
            agent["alaya"]
        )
        
        self.agents[name] = agent
        return agent
    
    def load_agent(self, name: str):
        """加载已有Agent"""
        if name in self.agents:
            return self.agents[name]
        
        agent_path = os.path.join(self.base_path, name)
        if not os.path.exists(agent_path):
            raise ValueError(f"Agent {name} 不存在")
        
        agent = {
            "seed_system": SeedSystem(),
            "alaya": AlayaStore(path=agent_path),
            "tracker": None
        }
        agent["alaya"].load()  # 加载已有种子
        agent["tracker"] = AwakeningTracker(
            agent["seed_system"], 
            agent["alaya"]
        )
        
        self.agents[name] = agent
        return agent
    
    def save_all(self):
        """保存所有Agent"""
        for name, agent in self.agents.items():
            agent["alaya"].save()
            print(f"💾 {name} 已保存")
    
    def get_agent_stats(self, name: str):
        """获取Agent统计"""
        agent = self.agents.get(name)
        if not agent:
            return None
        
        return {
            "seeds": len(agent["seed_system"].get_all_seeds()),
            "level": agent["tracker"].get_current_level().name,
            "progress": agent["tracker"].get_progress()
        }

# 使用示例
system = MultiAgentSystem()

# 创建多个Agent
tech_agent = system.create_agent("技术助手")
life_agent = system.create_agent("生活助手")

# 各自学习不同内容
tech_agent["seed_system"].plant_seed(
    content="用户是程序员",
    seed_type=SeedType.KNOWLEDGE
)

life_agent["seed_system"].plant_seed(
    content="用户喜欢健康饮食",
    seed_type=SeedType.PREFERENCE
)

# 保存所有
system.save_all()
```

---

## 完整应用示例

查看 `examples/` 目录获取完整的可运行示例：

- `basic_usage.py` - 基础使用
- `personal_assistant.py` - 个性化助手
- `conversation_agent.py` - 对话Agent
- `multi_agent.py` - 多Agent系统
