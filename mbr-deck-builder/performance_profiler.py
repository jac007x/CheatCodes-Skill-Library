"""Performance Profiler - Identify and Measure Bottlenecks

Tools for profiling:
- Function execution time
- Memory usage
- Algorithmic complexity analysis
- Load testing

Author: Code Puppy 🐶
Date: March 16, 2026
"""

import time
import functools
import tracemalloc
from typing import Callable, Any, Dict, List
from dataclasses import dataclass, field
from datetime import datetime
import statistics


@dataclass
class FunctionProfile:
    """Profile results for a single function"""
    function_name: str
    total_calls: int = 0
    total_time_ms: float = 0.0
    min_time_ms: float = float('inf')
    max_time_ms: float = 0.0
    avg_time_ms: float = 0.0
    memory_bytes: int = 0
    error_count: int = 0
    
    def update(self, execution_time_ms: float, memory_bytes: int = 0, error: bool = False):
        """Update profile with new execution"""
        self.total_calls += 1
        self.total_time_ms += execution_time_ms
        self.min_time_ms = min(self.min_time_ms, execution_time_ms)
        self.max_time_ms = max(self.max_time_ms, execution_time_ms)
        self.avg_time_ms = self.total_time_ms / self.total_calls
        self.memory_bytes = max(self.memory_bytes, memory_bytes)
        if error:
            self.error_count += 1
    
    def is_slow(self, threshold_ms: float = 100.0) -> bool:
        """Is this function slow?"""
        return self.avg_time_ms > threshold_ms
    
    def is_memory_heavy(self, threshold_bytes: float = 10_000_000) -> bool:
        """Is this function memory-heavy?"""
        return self.memory_bytes > threshold_bytes
    
    def report(self) -> str:
        """Generate report"""
        return f"""
  Function: {self.function_name}
  Calls: {self.total_calls}
  Total Time: {self.total_time_ms:.2f}ms
  Avg Time: {self.avg_time_ms:.2f}ms
  Min Time: {self.min_time_ms:.2f}ms
  Max Time: {self.max_time_ms:.2f}ms
  Memory: {self.memory_bytes / 1_000_000:.2f}MB
  Errors: {self.error_count}
        """.strip()


class Profiler:
    """Global profiler for tracking function performance"""
    
    def __init__(self):
        self.profiles: Dict[str, FunctionProfile] = {}
        self.enabled = True
    
    def profile_function(self, func: Callable) -> Callable:
        """Decorator to profile a function"""
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if not self.enabled:
                return func(*args, **kwargs)
            
            function_name = func.__qualname__
            
            # Start memory tracking
            tracemalloc.start()
            start_time = time.perf_counter()
            
            try:
                result = func(*args, **kwargs)
                execution_time_ms = (time.perf_counter() - start_time) * 1000
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                
                # Update profile
                if function_name not in self.profiles:
                    self.profiles[function_name] = FunctionProfile(function_name)
                
                self.profiles[function_name].update(
                    execution_time_ms=execution_time_ms,
                    memory_bytes=peak,
                    error=False
                )
                
                return result
            
            except Exception as e:
                execution_time_ms = (time.perf_counter() - start_time) * 1000
                tracemalloc.stop()
                
                if function_name not in self.profiles:
                    self.profiles[function_name] = FunctionProfile(function_name)
                
                self.profiles[function_name].update(
                    execution_time_ms=execution_time_ms,
                    error=True
                )
                
                raise
        
        return wrapper
    
    def get_slowest(self, limit: int = 10) -> List[FunctionProfile]:
        """Get slowest functions"""
        return sorted(
            self.profiles.values(),
            key=lambda p: p.avg_time_ms,
            reverse=True
        )[:limit]
    
    def get_memory_heavy(self, limit: int = 10) -> List[FunctionProfile]:
        """Get memory-heavy functions"""
        return sorted(
            self.profiles.values(),
            key=lambda p: p.memory_bytes,
            reverse=True
        )[:limit]
    
    def report(self) -> str:
        """Generate performance report"""
        slowest = self.get_slowest(10)
        memory_heavy = self.get_memory_heavy(10)
        
        report = "\n" + "="*70
        report += "\nPERFORMANCE PROFILE REPORT"
        report += "\n" + "="*70
        
        report += "\n\n🐌 TOP 10 SLOWEST FUNCTIONS:"
        report += "\n" + "-"*70
        for profile in slowest:
            status = "⚠️ SLOW" if profile.is_slow() else "✅ OK"
            report += f"\n{status} {profile.function_name}: {profile.avg_time_ms:.2f}ms"
        
        report += "\n\n💾 TOP 10 MEMORY-HEAVY FUNCTIONS:"
        report += "\n" + "-"*70
        for profile in memory_heavy:
            status = "⚠️ HEAVY" if profile.is_memory_heavy() else "✅ OK"
            report += f"\n{status} {profile.function_name}: {profile.memory_bytes / 1_000_000:.2f}MB"
        
        report += "\n\n📊 SUMMARY:"
        report += "\n" + "-"*70
        total_calls = sum(p.total_calls for p in self.profiles.values())
        total_time = sum(p.total_time_ms for p in self.profiles.values())
        report += f"\nTotal Functions: {len(self.profiles)}"
        report += f"\nTotal Calls: {total_calls}"
        report += f"\nTotal Time: {total_time:.2f}ms"
        
        report += "\n" + "="*70
        
        return report
    
    def reset(self):
        """Reset profiles"""
        self.profiles = {}


# Global profiler instance
_global_profiler = Profiler()


def profile(func: Callable) -> Callable:
    """Convenience decorator to profile a function"""
    return _global_profiler.profile_function(func)


def get_profiler() -> Profiler:
    """Get global profiler instance"""
    return _global_profiler