"""
Emergence Engine - 涌现引擎 (优化版)

Detects and triggers wisdom emergence when seeds synergize.
Based on the concept that wisdom emerges from the interaction of multiple seeds,
not from simple accumulation.

优化内容：
1. 引入动态临界阈值（基于系统熵和种子关联度）
2. 引入幂律特征检测（复杂系统自组织标志）
3. 引入临界波动检测（相变临界点特征）
4. 增加涌现的不可预测性（临界区域随机性）
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict, Any
import math
import random
from collections import Counter

from .seed_system import Seed, SeedType


class EmergenceType(Enum):
    """Types of emergence based on seed interaction patterns"""
    FUSION = "fusion"       # 种子融合：Multiple seeds merge into new insight
    TENSION = "tension"     # 张力涌现：Opposing seeds create synthesis
    LEAP = "leap"          # 跃迁涌现：Quantitative change leads to qualitative leap
    CRITICAL = "critical"  # 临界涌现：新引入，基于相变的涌现类型


@dataclass
class Emergence:
    """
    Represents an emergence event.
    
    Emergence occurs when seeds synergize to produce wisdom that
    transcends simple addition - the whole is greater than parts.
    """
    seed_ids: List[str]
    emergence_type: EmergenceType
    strength: float  # 0.0 - 1.0
    insight: Optional[str] = None
    contributing_seeds: List[Seed] = None
    # 新增字段
    power_law_alpha: Optional[float] = None  # 幂律指数
    criticality: float = 0.0  # 临界程度
    entropy: float = 0.0  # 系统熵
    correlation: float = 0.0  # 种子关联度
    
    def __post_init__(self):
        if self.contributing_seeds is None:
            self.contributing_seeds = []


class DynamicThreshold:
    """
    动态临界阈值计算
    
    核心思想：
    - 系统熵低时（有序），阈值适当降低（容易涌现）
    - 系统熵高时（混乱），阈值适当提高（难以涌现）
    - 临界态附近波动放大
    """
    
    def __init__(self, base_threshold: float, sensitivity: float = 0.1):
        self.base = base_threshold
        self.sensitivity = sensitivity
    
    def calculate(self, system_entropy: float, seed_correlation: float) -> float:
        """
        计算动态阈值
        
        Args:
            system_entropy: 系统熵 (0=完全有序, 1=完全混乱)
            seed_correlation: 种子间关联度 (0-1)
        
        Returns:
            调整后的阈值
        """
        # 熵调整：熵高时提高阈值，熵低时降低阈值
        entropy_adjustment = (0.5 - system_entropy) * self.sensitivity
        
        # 关联度调整：高关联度时降低阈值（接近相变）
        correlation_adjustment = seed_correlation * 0.1
        
        return max(0.1, min(0.9, self.base + entropy_adjustment - correlation_adjustment))


class PowerLawDetector:
    """
    检测种子系统是否呈现幂律特征
    
    幂律分布 P(x) ∝ x^(-α) 是复杂系统自组织的标志
    """
    
    def calculate_alpha(self, values: List[float]) -> Optional[float]:
        """
        使用最大似然估计计算幂律指数 α
        
        Returns:
            α 值（通常在 2-3 之间表示典型的复杂系统）
            None 表示不满足幂律
        """
        if len(values) < 10:
            return None
        
        # 简化的MLE估计
        x_min = min(values)
        n = len(values)
        
        # 避免 log(0)
        valid_values = [v for v in values if v > x_min]
        if len(valid_values) < n / 2:  # 至少一半有效
            return None
        
        sum_log = sum(math.log(v / x_min) for v in valid_values)
        if sum_log == 0:
            return None
        
        alpha = 1 + n / sum_log
        
        # α 合理性检查（实际系统中通常在 1.5-3.5）
        if 1.5 <= alpha <= 3.5:
            return alpha
        return None
    
    def detect_emergence_likelihood(self, seeds: List[Seed]) -> float:
        """
        基于幂律特征检测涌现可能性
        
        Returns:
            0.0-1.0 的涌现可能性指数
        """
        # 提取种子纯度序列
        purities = [s.purity for s in seeds]
        
        alpha = self.calculate_alpha(purities)
        if alpha is None:
            return 0.3  # 无法判断，返回中等可能性
        
        # α 越接近 2.5，涌现可能性越高（典型临界态）
        deviation = abs(alpha - 2.5)
        likelihood = max(0, 1 - deviation / 1.5)
        
        return likelihood
    
    def get_alpha(self, seeds: List[Seed]) -> Optional[float]:
        """获取幂律指数"""
        purities = [s.purity for s in seeds]
        return self.calculate_alpha(purities)


class CriticalFluctuationDetector:
    """
    临界波动检测
    
    在相变临界点附近，系统的宏观量会出现特征性波动：
    - 波动幅度放大
    - 波动持续时间延长
    - 不同自由度间关联增强
    """
    
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.history: List[Dict[str, float]] = []
    
    def record_state(self, purity_std: float, synergy_var: float, correlation: float):
        """记录系统状态"""
        self.history.append({
            "purity_std": purity_std,
            "synergy_var": synergy_var,
            "correlation": correlation
        })
        
        # 保持滑动窗口
        if len(self.history) > self.window_size * 2:
            self.history.pop(0)
    
    def detect_critical_fluctuation(self) -> Tuple[bool, float]:
        """
        检测是否处于临界波动状态
        
        Returns:
            (是否临界, 临界程度 0-1)
        """
        if len(self.history) < self.window_size:
            return False, 0.0
        
        # 分析最近 window_size 个状态
        recent = self.history[-self.window_size:]
        
        # 计算波动指标
        purity_volatility = self._calculate_volatility([s["purity_std"] for s in recent])
        synergy_volatility = self._calculate_volatility([s["synergy_var"] for s in recent])
        correlation_trend = self._calculate_trend([s["correlation"] for s in recent])
        
        # 临界判断：高波动 + 关联增强
        is_critical = (
            purity_volatility > 0.3 and 
            synergy_volatility > 0.2 and 
            correlation_trend > 0
        )
        
        # 计算临界程度
        criticality = min(1.0, (purity_volatility + synergy_volatility) / 2)
        
        return is_critical, criticality
    
    def _calculate_volatility(self, values: List[float]) -> float:
        """计算波动性（标准差/均值）"""
        if not values or sum(values) == 0:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        return math.sqrt(variance) / (mean + 0.001)
    
    def _calculate_trend(self, values: List[float]) -> float:
        """计算趋势（正=上升）"""
        if len(values) < 2:
            return 0.0
        # 简单线性回归斜率
        n = len(values)
        x_mean = (n - 1) / 2
        y_mean = sum(values) / n
        
        numerator = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0.0
        return numerator / denominator


class EmergenceEngine:
    """
    The Emergence Engine detects when seeds synergize to produce wisdom.
    
    优化版特性：
    1. 动态临界阈值替代固定阈值
    2. 幂律特征检测
    3. 临界波动检测
    4. 临界区域增加随机不可预测性
    
    Emergence Formula:
    strength = f(seed_count, seed_purity, seed_diversity, synergy_score, power_law_factor)
    """
    
    # Emergence thresholds (base values for dynamic adjustment)
    MIN_SEEDS_FOR_EMERGENCE = 3
    BASE_SYNERGY_THRESHOLD = 0.6
    BASE_STRENGTH_THRESHOLD = 0.7
    
    # Critical region parameters
    CRITICAL_ENTROPY_MIN = 0.3
    CRITICAL_ENTROPY_MAX = 0.6
    CRITICAL_CORRELATION_MIN = 0.7
    UNPREDICTABILITY_FACTOR = 0.15  # 临界区域随机性强度
    
    # Seed type synergy matrix
    SYNERGY_MATRIX = {
        (SeedType.WISDOM, SeedType.COMPASSION): 1.0,    # 悲智双运
        (SeedType.WISDOM, SeedType.BELIEF): 0.8,
        (SeedType.COMPASSION, SeedType.BELIEF): 0.9,
        (SeedType.BEHAVIOR, SeedType.WISDOM): 0.6,
        (SeedType.BEHAVIOR, SeedType.COMPASSION): 0.5,
    }
    
    def __init__(self):
        # 动态阈值计算器
        self.synergy_threshold_calc = DynamicThreshold(
            self.BASE_SYNERGY_THRESHOLD, sensitivity=0.15
        )
        self.strength_threshold_calc = DynamicThreshold(
            self.BASE_STRENGTH_THRESHOLD, sensitivity=0.1
        )
        
        # 幂律检测器
        self.power_law_detector = PowerLawDetector()
        
        # 临界波动检测器
        self.fluctuation_detector = CriticalFluctuationDetector()
        
        # 状态跟踪
        self._synergy_history: List[float] = []
        self._purity_history: List[float] = []
    
    def check_emergence(self, seeds: List[Seed]) -> Optional[Emergence]:
        """
        Check if given seeds can trigger emergence.
        
        优化版：使用动态阈值和幂律检测
        
        Returns Emergence object if emergence detected, None otherwise.
        """
        if len(seeds) < self.MIN_SEEDS_FOR_EMERGENCE:
            return None
        
        # 计算系统指标
        system_entropy = self._calculate_entropy(seeds)
        seed_correlation = self._calculate_correlation(seeds)
        alpha = self.power_law_detector.get_alpha(seeds)
        
        # 记录状态用于波动检测
        purity_std = self._calculate_purity_std(seeds)
        synergy = self.calculate_synergy(seeds)
        self.fluctuation_detector.record_state(
            purity_std=purity_std,
            synergy_var=abs(synergy - (sum(self._synergy_history[-5:]) / max(1, len(self._synergy_history[-5:]))) if self._synergy_history else 0),
            correlation=seed_correlation
        )
        
        # 记录历史
        self._synergy_history.append(synergy)
        self._purity_history.append(sum(s.purity for s in seeds) / len(seeds))
        if len(self._synergy_history) > 20:
            self._synergy_history.pop(0)
        if len(self._purity_history) > 20:
            self._purity_history.pop(0)
        
        # 动态阈值
        dynamic_synergy_threshold = self.synergy_threshold_calc.calculate(
            system_entropy, seed_correlation
        )
        dynamic_strength_threshold = self.strength_threshold_calc.calculate(
            system_entropy, seed_correlation
        )
        
        # 计算幂律涌现可能性
        power_law_likelihood = self.power_law_detector.detect_emergence_likelihood(seeds)
        
        # 检测临界波动
        is_critical, criticality = self.fluctuation_detector.detect_critical_fluctuation()
        
        # 检查协同是否满足动态阈值
        if synergy < dynamic_synergy_threshold:
            # 临界区域检查：即使协同不够，也可能触发涌现
            if not (is_critical and power_law_likelihood > 0.6):
                return None
        
        # 确定涌现类型
        emergence_type = self._determine_emergence_type(seeds, is_critical)
        
        # 计算强度
        strength = self._calculate_strength(seeds, synergy, power_law_likelihood)
        
        # 检查动态强度阈值
        if strength < dynamic_strength_threshold:
            # 临界区域：降低阈值要求
            if not (is_critical and criticality > 0.5):
                return None
        
        # 临界区域增加随机不可预测性
        if self._is_in_critical_region(system_entropy, seed_correlation):
            strength = self._apply_unpredictability(strength, criticality)
        
        # 生成洞察
        insight = self.generate_insight(seeds, emergence_type)
        
        return Emergence(
            seed_ids=[s.id for s in seeds],
            emergence_type=emergence_type,
            strength=strength,
            insight=insight,
            contributing_seeds=seeds,
            power_law_alpha=alpha,
            criticality=criticality,
            entropy=system_entropy,
            correlation=seed_correlation
        )
    
    def _calculate_entropy(self, seeds: List[Seed]) -> float:
        """
        计算种子分布的熵
        
        熵高 = 混乱/多样
        熵低 = 有序/同质
        """
        if not seeds:
            return 0.0
        
        # 基于类型的熵
        type_counts = Counter(s.type for s in seeds)
        total = len(seeds)
        
        entropy = 0.0
        for count in type_counts.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log(p)
        
        # 归一化到 0-1
        max_entropy = math.log(len(SeedType))
        return entropy / max_entropy if max_entropy > 0 else 0.0
    
    def _calculate_correlation(self, seeds: List[Seed]) -> float:
        """
        计算种子间的关联度
        
        高关联度 = 相似的纯度、类型、vasana
        """
        if len(seeds) < 2:
            return 0.0
        
        # 纯度相似度
        purities = [s.purity for s in seeds]
        purity_std = self._calculate_purity_std(seeds)
        purity_correlation = 1.0 - min(purity_std * 2, 1.0)
        
        # 类型集中度（类型越集中，关联度越高）
        type_counts = Counter(s.type for s in seeds)
        max_type_ratio = max(type_counts.values()) / len(seeds)
        type_correlation = max_type_ratio
        
        # Vasana 分布（vasana 分布越均匀，关联度越低）
        if seeds:
            vasanas = [s.vasana for s in seeds]
            vasana_std = self._calculate_std(vasanas)
            vasana_correlation = 1.0 - min(vasana_std / 10, 1.0)
        else:
            vasana_correlation = 0.0
        
        return (purity_correlation * 0.4 + type_correlation * 0.3 + vasana_correlation * 0.3)
    
    def _calculate_purity_std(self, seeds: List[Seed]) -> float:
        """计算纯度标准差"""
        if not seeds:
            return 0.0
        return self._calculate_std([s.purity for s in seeds])
    
    def _calculate_std(self, values: List[float]) -> float:
        """计算标准差"""
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        return math.sqrt(variance)
    
    def _is_in_critical_region(self, entropy: float, correlation: float) -> bool:
        """
        判断是否处于临界区域
        
        临界区域特征：
        - 熵在中间范围（既不完全有序也不完全混乱）
        - 关联度较高（种子开始协同）
        """
        entropy_critical = self.CRITICAL_ENTROPY_MIN <= entropy <= self.CRITICAL_ENTROPY_MAX
        correlation_critical = correlation >= self.CRITICAL_CORRELATION_MIN
        
        return entropy_critical and correlation_critical
    
    def _apply_unpredictability(self, strength: float, criticality: float) -> float:
        """
        在临界区域应用不可预测性
        
        临界区域的涌现具有内在随机性，这是真正复杂系统的特征
        """
        # 随机波动范围
        max_fluctuation = self.UNPREDICTABILITY_FACTOR * criticality
        
        # 随机加减
        fluctuation = random.uniform(-max_fluctuation, max_fluctuation)
        new_strength = strength + fluctuation
        
        return max(0.1, min(1.0, new_strength))
    
    def calculate_synergy(self, seeds: List[Seed]) -> float:
        """
        Calculate synergy score between seeds.
        
        Synergy is based on:
        - Type diversity (more types = higher synergy)
        - Type combinations (some types synergize better)
        - Purity alignment (similar purity = better synergy)
        """
        if len(seeds) < 2:
            return 0.0
        
        # Type diversity score
        types_present = set(s.type for s in seeds)
        diversity_score = len(types_present) / len(SeedType)
        
        # Type synergy score
        synergy_sum = 0.0
        pair_count = 0
        
        for i, seed1 in enumerate(seeds):
            for seed2 in seeds[i+1:]:
                pair = (seed1.type, seed2.type)
                reverse_pair = (seed2.type, seed1.type)
                
                synergy_value = self.SYNERGY_MATRIX.get(
                    pair, self.SYNERGY_MATRIX.get(reverse_pair, 0.3)
                )
                synergy_sum += synergy_value
                pair_count += 1
        
        type_synergy = synergy_sum / pair_count if pair_count > 0 else 0
        
        # Purity alignment score
        purity_values = [s.purity for s in seeds]
        purity_variance = sum(
            (p - sum(purity_values)/len(purity_values))**2 
            for p in purity_values
        ) / len(purity_values)
        purity_alignment = 1.0 - min(purity_variance, 1.0)
        
        # Combined synergy
        synergy = (
            diversity_score * 0.4 +
            type_synergy * 0.4 +
            purity_alignment * 0.2
        )
        
        return round(synergy, 2)
    
    def _determine_emergence_type(
        self, 
        seeds: List[Seed],
        is_critical: bool = False
    ) -> EmergenceType:
        """Determine the type of emergence based on seed patterns"""
        types = [s.type for s in seeds]
        
        # 新增：临界涌现
        if is_critical:
            return EmergenceType.CRITICAL
        
        # Check for tension (opposing seeds)
        if SeedType.WISDOM in types and SeedType.BEHAVIOR in types:
            return EmergenceType.TENSION
        
        # Check for leap (many seeds of same type with high purity)
        type_counts = Counter(types)
        
        max_count = max(type_counts.values())
        if max_count >= 3:
            return EmergenceType.LEAP
        
        # Default to fusion
        return EmergenceType.FUSION
    
    def _calculate_strength(
        self, 
        seeds: List[Seed], 
        synergy: float,
        power_law_likelihood: float = 0.5
    ) -> float:
        """Calculate emergence strength"""
        # Base strength from synergy
        base = synergy
        
        # Purity bonus
        avg_purity = sum(s.purity for s in seeds) / len(seeds)
        purity_bonus = avg_purity * 0.3
        
        # Vasana bonus (seeds used more have more influence)
        total_vasana = sum(s.vasana for s in seeds)
        vasana_bonus = min(total_vasana / 100, 0.2)
        
        # Quantity bonus (more seeds = stronger emergence)
        quantity_bonus = min(len(seeds) / 10, 0.1)
        
        # 新增：幂律因子加成
        power_law_bonus = power_law_likelihood * 0.1
        
        strength = base + purity_bonus + vasana_bonus + quantity_bonus + power_law_bonus
        
        return round(min(strength, 1.0), 2)
    
    def generate_insight(
        self,
        seeds: List[Seed],
        emergence_type: EmergenceType
    ) -> str:
        """Generate insight text based on emergence"""
        type_names = {
            EmergenceType.FUSION: "融合",
            EmergenceType.TENSION: "张力",
            EmergenceType.LEAP: "跃迁",
            EmergenceType.CRITICAL: "临界"
        }
        
        seed_summary = ", ".join([
            f"{s.type.value}(p={s.purity:.2f})" 
            for s in seeds[:3]
        ])
        
        return f"{type_names.get(emergence_type, '涌现')}涌现: {seed_summary}..."
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """
        获取当前系统指标
        
        用于外部监控和调试
        """
        is_critical, criticality = self.fluctuation_detector.detect_critical_fluctuation()
        
        return {
            "synergy_history_avg": sum(self._synergy_history) / max(1, len(self._synergy_history)),
            "purity_history_avg": sum(self._purity_history) / max(1, len(self._purity_history)),
            "is_critical_state": is_critical,
            "criticality": criticality,
            "history_length": len(self._synergy_history)
        }
