"""Performance Optimizations - Caching, Memoization, and Algorithmic Improvements

Optimizations applied:
1. Caching for metric analysis results
2. Memoization for owner lookups
3. Batch processing instead of sequential
4. Lazy evaluation of expensive operations
5. Object pooling for recommendation objects

Author: Code Puppy 🐶
Date: March 16, 2026
"""

import functools
from typing import Dict, Optional, Any, List, Tuple
from dataclasses import dataclass, field
import time
from collections import defaultdict


@dataclass
class CacheEntry:
    """Single cache entry with TTL"""
    value: Any
    timestamp: float = field(default_factory=time.time)
    ttl_seconds: float = 3600  # 1 hour default
    
    def is_expired(self) -> bool:
        """Check if entry has expired"""
        return (time.time() - self.timestamp) > self.ttl_seconds


class SmartCache:
    """Simple but effective caching system with TTL"""
    
    def __init__(self, max_size: int = 1000):
        self.cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache, None if not found or expired"""
        if key in self.cache:
            entry = self.cache[key]
            if not entry.is_expired():
                self.hits += 1
                return entry.value
            else:
                # Expired, remove it
                del self.cache[key]
        
        self.misses += 1
        return None
    
    def set(self, key: str, value: Any, ttl_seconds: float = 3600):
        """Set value in cache with TTL"""
        # Simple eviction: if full, clear oldest 10%
        if len(self.cache) >= self.max_size:
            oldest_keys = sorted(
                self.cache.items(),
                key=lambda x: x[1].timestamp
            )[:self.max_size // 10]
            for k, _ in oldest_keys:
                del self.cache[k]
        
        self.cache[key] = CacheEntry(
            value=value,
            ttl_seconds=ttl_seconds
        )
    
    def hit_rate(self) -> float:
        """Return cache hit rate"""
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0
    
    def clear(self):
        """Clear entire cache"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
    
    def report(self) -> str:
        """Generate cache report"""
        return f"""
  Cache Statistics:
  Size: {len(self.cache)}/{self.max_size}
  Hits: {self.hits}
  Misses: {self.misses}
  Hit Rate: {self.hit_rate():.1f}%
        """.strip()


class CachedOwnerLookup:
    """Cached owner lookup to avoid repeated dictionary searches"""
    
    def __init__(self):
        self.cache = SmartCache(max_size=100)
        self.owner_map = {
            "revenue": {"owner": "Finance/Revenue Team", "function": "Finance"},
            "cac": {"owner": "Marketing Team", "function": "Marketing"},
            "conversion": {"owner": "Product Team", "function": "Product"},
            "ltv": {"owner": "Finance/Product Team", "function": "Finance"},
            "churn": {"owner": "Customer Success Team", "function": "Operations"},
            "nps": {"owner": "Customer Success Team", "function": "Operations"},
            "uptime": {"owner": "Engineering Team", "function": "Engineering"},
            "default": {"owner": "Data Team", "function": "Analytics"},
        }
    
    def get_owner(self, metric_name: str) -> Dict[str, str]:
        """Get owner with caching"""
        cache_key = f"owner:{metric_name.lower()}"
        
        # Check cache first
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        # Compute
        metric_lower = metric_name.lower()
        for key, owner_info in self.owner_map.items():
            if key in metric_lower:
                self.cache.set(cache_key, owner_info)
                return owner_info
        
        # Default
        self.cache.set(cache_key, self.owner_map["default"])
        return self.owner_map["default"]


class BatchMetricProcessor:
    """Process metrics in batches to improve cache locality and reduce overhead"""
    
    def __init__(self, batch_size: int = 10):
        self.batch_size = batch_size
        self.owner_cache = CachedOwnerLookup()
    
    def process_batch(
        self,
        metrics: Dict[str, Dict[str, Any]],
        analyzer_func: callable
    ) -> List[Any]:
        """Process metrics in batches
        
        Benefits:
        - Better cache locality
        - Reduced function call overhead
        - Opportunity for vectorization
        """
        results = []
        batch = []
        
        for metric_name, metric_data in metrics.items():
            batch.append((metric_name, metric_data))
            
            if len(batch) >= self.batch_size:
                # Process batch
                batch_results = self._process_batch_internal(batch, analyzer_func)
                results.extend(batch_results)
                batch = []
        
        # Process remaining items
        if batch:
            batch_results = self._process_batch_internal(batch, analyzer_func)
            results.extend(batch_results)
        
        return results
    
    def _process_batch_internal(
        self,
        batch: List[Tuple[str, Dict[str, Any]]],
        analyzer_func: callable
    ) -> List[Any]:
        """Process a single batch"""
        results = []
        for metric_name, metric_data in batch:
            result = analyzer_func(metric_name, metric_data)
            results.append(result)
        return results


class LazyEvaluator:
    """Defer expensive computations until actually needed"""
    
    def __init__(self):
        self.pending_tasks = []
        self.completed = {}
    
    def defer(self, key: str, func: callable, *args, **kwargs):
        """Defer computation of func(*args, **kwargs)"""
        self.pending_tasks.append({
            "key": key,
            "func": func,
            "args": args,
            "kwargs": kwargs
        })
    
    def evaluate(self, key: str) -> Optional[Any]:
        """Evaluate deferred computation if not already done"""
        if key in self.completed:
            return self.completed[key]
        
        # Find and execute task
        for i, task in enumerate(self.pending_tasks):
            if task["key"] == key:
                result = task["func"](*task["args"], **task["kwargs"])
                self.completed[key] = result
                self.pending_tasks.pop(i)
                return result
        
        return None
    
    def evaluate_all(self):
        """Evaluate all pending tasks"""
        while self.pending_tasks:
            task = self.pending_tasks.pop(0)
            result = task["func"](*task["args"], **task["kwargs"])
            self.completed[task["key"]] = result


class ObjectPool:
    """Reuse objects to reduce garbage collection pressure"""
    
    def __init__(self, object_class: type, initial_size: int = 100):
        self.object_class = object_class
        self.pool = [object_class() for _ in range(initial_size)]
        self.available = list(range(initial_size))
        self.in_use = set()
    
    def acquire(self) -> Any:
        """Get object from pool"""
        if not self.available:
            # Pool exhausted, create new object
            obj = self.object_class()
            self.pool.append(obj)
            idx = len(self.pool) - 1
        else:
            idx = self.available.pop()
        
        self.in_use.add(idx)
        return self.pool[idx]
    
    def release(self, obj: Any):
        """Return object to pool"""
        try:
            idx = self.pool.index(obj)
            self.in_use.discard(idx)
            self.available.append(idx)
        except ValueError:
            pass  # Object not in pool
    
    def stats(self) -> str:
        """Get pool statistics"""
        return f"Pool: {len(self.available)} available, {len(self.in_use)} in use"


# Global instances
_metric_cache = SmartCache(max_size=500)
_owner_lookup = CachedOwnerLookup()
_batch_processor = BatchMetricProcessor(batch_size=10)


def get_metric_cache() -> SmartCache:
    """Get global metric cache"""
    return _metric_cache


def get_owner_lookup() -> CachedOwnerLookup:
    """Get global owner lookup"""
    return _owner_lookup


def get_batch_processor() -> BatchMetricProcessor:
    """Get global batch processor"""
    return _batch_processor