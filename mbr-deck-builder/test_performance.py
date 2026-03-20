"""Comprehensive Performance and Load Testing

Tests:
1. Performance benchmarks for each component
2. Load testing (simulate 100+ metrics)
3. Stress testing (memory and CPU)
4. Regression tests (ensure optimizations work)
5. Cache efficiency tests

Author: Code Puppy 🐶
Date: March 16, 2026
"""

import time
import random
import unittest
from typing import Dict, Any, List
import statistics

from phase1_orchestrator import Phase1Orchestrator, Phase1Result
from enhanced_insight_engine import EnhancedPhase2Analyzer, TrendAnalyzer
from performance_profiler import get_profiler, profile
from optimizations import (
    SmartCache,
    CachedOwnerLookup,
    BatchMetricProcessor,
    get_metric_cache,
    get_owner_lookup,
)


class PerformanceBenchmarks(unittest.TestCase):
    """Benchmark individual components"""
    
    def test_trend_analyzer_performance(self):
        """Benchmark trend analysis"""
        analyzer = TrendAnalyzer()
        
        times = []
        for _ in range(1000):
            start = time.perf_counter()
            analyzer.analyze(
                current=100,
                prior=95,
                two_prior=90
            )
            times.append((time.perf_counter() - start) * 1000)
        
        avg_time = statistics.mean(times)
        max_time = max(times)
        
        print(f"\n✅ Trend Analysis:")
        print(f"   Avg: {avg_time:.3f}ms, Max: {max_time:.3f}ms")
        
        # Should be < 1ms per call
        self.assertLess(avg_time, 1.0, "Trend analysis too slow")
    
    def test_owner_lookup_performance(self):
        """Benchmark owner lookup"""
        lookup = CachedOwnerLookup()
        metrics = ["Revenue", "CAC", "Conversion", "LTV", "Churn", "NPS"]
        
        # First pass (cache misses)
        start = time.perf_counter()
        for metric in metrics * 100:
            lookup.get_owner(metric)
        first_pass = (time.perf_counter() - start) * 1000
        
        # Second pass (cache hits)
        start = time.perf_counter()
        for metric in metrics * 100:
            lookup.get_owner(metric)
        second_pass = (time.perf_counter() - start) * 1000
        
        hit_rate = lookup.cache.hit_rate()
        improvement = (first_pass - second_pass) / first_pass * 100
        
        print(f"\n✅ Owner Lookup (with cache):")
        print(f"   First pass: {first_pass:.2f}ms")
        print(f"   Second pass: {second_pass:.2f}ms")
        print(f"   Improvement: {improvement:.1f}%")
        print(f"   Hit rate: {hit_rate:.1f}%")
        
        # Cached should be significantly faster
        self.assertGreater(improvement, 50, "Cache not improving performance")
    
    def test_insight_engine_performance(self):
        """Benchmark insight generation"""
        analyzer = EnhancedPhase2Analyzer()
        
        times = []
        for _ in range(100):
            start = time.perf_counter()
            analyzer.analyze(
                metric_name="Revenue",
                current_value=14.2,
                target_value=13.8,
                prior_value=12.6,
                ly_value=13.0,
            )
            times.append((time.perf_counter() - start) * 1000)
        
        avg_time = statistics.mean(times)
        max_time = max(times)
        
        print(f"\n✅ Insight Generation:")
        print(f"   Avg: {avg_time:.2f}ms, Max: {max_time:.2f}ms")
        
        # Should be < 10ms per call
        self.assertLess(avg_time, 10.0, "Insight generation too slow")
    
    def test_orchestrator_performance(self):
        """Benchmark complete orchestrator"""
        orchestrator = Phase1Orchestrator()
        
        metrics = {
            "Revenue": {"current_value": 14.2, "target_value": 13.8, "prior_value": 12.6, "ly_value": 13.0},
            "CAC": {"current_value": 42, "target_value": 45, "prior_value": 48, "ly_value": 40},
            "Conversion": {"current_value": 2.1, "target_value": 2.3, "prior_value": 2.2, "ly_value": 2.0},
        }
        
        start = time.perf_counter()
        result = orchestrator.run(
            mbr_month="March 2026",
            metrics_data=metrics,
        )
        elapsed = (time.perf_counter() - start) * 1000
        
        print(f"\n✅ Complete Orchestrator (3 metrics):")
        print(f"   Time: {elapsed:.2f}ms")
        print(f"   Insights: {len(result.metric_insights)}")
        print(f"   Recommendations: {len(result.all_recommendations)}")
        
        # Should be < 500ms for 3 metrics
        self.assertLess(elapsed, 500.0, "Orchestrator too slow")


class LoadTesting(unittest.TestCase):
    """Load test with many metrics"""
    
    def test_load_10_metrics(self):
        """Load test with 10 metrics"""
        self._run_load_test(10)
    
    def test_load_50_metrics(self):
        """Load test with 50 metrics"""
        self._run_load_test(50)
    
    def test_load_100_metrics(self):
        """Load test with 100 metrics"""
        self._run_load_test(100)
    
    def _run_load_test(self, num_metrics: int):
        """Run load test with specified number of metrics"""
        orchestrator = Phase1Orchestrator()
        
        # Generate metrics
        metrics = {}
        for i in range(num_metrics):
            metrics[f"Metric_{i}"] = {
                "current_value": random.uniform(10, 100),
                "target_value": random.uniform(10, 100),
                "prior_value": random.uniform(10, 100),
                "ly_value": random.uniform(10, 100),
            }
        
        # Run orchestrator
        start = time.perf_counter()
        result = orchestrator.run(
            mbr_month="March 2026",
            metrics_data=metrics,
        )
        elapsed = (time.perf_counter() - start) * 1000
        
        print(f"\n✅ Load Test ({num_metrics} metrics):")
        print(f"   Time: {elapsed:.2f}ms")
        print(f"   Per metric: {elapsed / num_metrics:.2f}ms")
        print(f"   Insights: {len(result.metric_insights)}")
        print(f"   Recommendations: {len(result.all_recommendations)}")
        
        # Performance should scale linearly
        self.assertLess(
            elapsed / num_metrics,
            50.0,
            f"Per-metric time too high: {elapsed / num_metrics:.2f}ms"
        )


class StressTesting(unittest.TestCase):
    """Stress test for edge cases"""
    
    def test_zero_targets(self):
        """Stress test with zero values"""
        analyzer = EnhancedPhase2Analyzer()
        
        # Should handle zero gracefully
        insight = analyzer.analyze(
            metric_name="Test",
            current_value=0,
            target_value=0,
            prior_value=0,
        )
        
        self.assertIsNotNone(insight)
        print(f"\n✅ Zero values handled gracefully")
    
    def test_extreme_values(self):
        """Stress test with extreme values"""
        analyzer = EnhancedPhase2Analyzer()
        
        # Very large values
        insight = analyzer.analyze(
            metric_name="Test",
            current_value=1e9,
            target_value=1e9,
            prior_value=1e8,
        )
        
        self.assertIsNotNone(insight)
        
        # Very small values
        insight = analyzer.analyze(
            metric_name="Test",
            current_value=0.0001,
            target_value=0.0001,
            prior_value=0.00008,
        )
        
        self.assertIsNotNone(insight)
        print(f"\n✅ Extreme values handled gracefully")
    
    def test_negative_values(self):
        """Stress test with negative values"""
        analyzer = EnhancedPhase2Analyzer()
        
        insight = analyzer.analyze(
            metric_name="Test",
            current_value=-10,
            target_value=-5,
            prior_value=-15,
        )
        
        self.assertIsNotNone(insight)
        print(f"\n✅ Negative values handled gracefully")


class CacheEfficiency(unittest.TestCase):
    """Test caching efficiency"""
    
    def test_cache_hit_rate(self):
        """Measure cache hit rate"""
        cache = SmartCache(max_size=100)
        
        # Populate cache
        for i in range(50):
            cache.set(f"key_{i}", f"value_{i}")
        
        # Access with repetition
        for _ in range(10):
            for i in range(50):
                cache.get(f"key_{i}")
        
        hit_rate = cache.hit_rate()
        print(f"\n✅ Cache Hit Rate: {hit_rate:.1f}%")
        print(f"   {cache.report()}")
        
        # Should have good hit rate
        self.assertGreater(hit_rate, 95, "Cache hit rate too low")
    
    def test_cache_eviction(self):
        """Test cache eviction when full"""
        cache = SmartCache(max_size=10)
        
        # Fill cache
        for i in range(10):
            cache.set(f"key_{i}", f"value_{i}")
        
        # Exceed capacity
        for i in range(10, 20):
            cache.set(f"key_{i}", f"value_{i}")
        
        # Should not exceed max size
        self.assertLessEqual(len(cache.cache), cache.max_size)
        print(f"\n✅ Cache eviction working correctly")
        print(f"   Size: {len(cache.cache)}/{cache.max_size}")


class RegressionTesting(unittest.TestCase):
    """Ensure optimizations don't break functionality"""
    
    def test_orchestrator_still_validates(self):
        """Ensure orchestrator still validates results"""
        orchestrator = Phase1Orchestrator()
        
        result = orchestrator.run(
            mbr_month="March 2026",
            metrics_data={
                "Revenue": {
                    "current_value": 14.2,
                    "target_value": 13.8,
                    "prior_value": 12.6,
                    "ly_value": 13.0,
                },
            },
        )
        
        # Should have validation result
        self.assertIsNotNone(result.validation_result)
        self.assertTrue(hasattr(result.validation_result, 'is_valid'))
        print(f"\n✅ Validation still working")
    
    def test_insights_still_generated(self):
        """Ensure insights are still generated"""
        orchestrator = Phase1Orchestrator()
        
        result = orchestrator.run(
            mbr_month="March 2026",
            metrics_data={
                "Revenue": {
                    "current_value": 14.2,
                    "target_value": 13.8,
                    "prior_value": 12.6,
                    "ly_value": 13.0,
                },
            },
        )
        
        # Should have insights
        self.assertGreater(len(result.metric_insights), 0)
        self.assertGreater(len(result.all_recommendations), 0)
        print(f"\n✅ Insights still being generated correctly")


class MemoryTesting(unittest.TestCase):
    """Test memory usage"""
    
    def test_memory_usage_with_large_dataset(self):
        """Measure memory usage with large dataset"""
        import tracemalloc
        
        tracemalloc.start()
        
        orchestrator = Phase1Orchestrator()
        
        # Generate 100 metrics
        metrics = {}
        for i in range(100):
            metrics[f"Metric_{i}"] = {
                "current_value": random.uniform(10, 100),
                "target_value": random.uniform(10, 100),
                "prior_value": random.uniform(10, 100),
                "ly_value": random.uniform(10, 100),
            }
        
        result = orchestrator.run(
            mbr_month="March 2026",
            metrics_data=metrics,
        )
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        peak_mb = peak / 1_000_000
        
        print(f"\n✅ Memory Usage (100 metrics):")
        print(f"   Peak: {peak_mb:.2f}MB")
        print(f"   Per metric: {peak_mb / 100:.3f}MB")
        
        # Should use reasonable memory
        self.assertLess(peak_mb, 100, "Memory usage too high")


class ScalabilityTesting(unittest.TestCase):
    """Test scalability characteristics"""
    
    def test_linear_scaling(self):
        """Verify linear scaling with metrics count"""
        orchestrator = Phase1Orchestrator()
        
        times = {}
        for num_metrics in [10, 25, 50, 100]:
            metrics = {}
            for i in range(num_metrics):
                metrics[f"Metric_{i}"] = {
                    "current_value": random.uniform(10, 100),
                    "target_value": random.uniform(10, 100),
                    "prior_value": random.uniform(10, 100),
                    "ly_value": random.uniform(10, 100),
                }
            
            start = time.perf_counter()
            result = orchestrator.run(
                mbr_month="March 2026",
                metrics_data=metrics,
            )
            elapsed = (time.perf_counter() - start) * 1000
            times[num_metrics] = elapsed
        
        print(f"\n✅ Scalability Analysis:")
        for num_metrics, elapsed in times.items():
            per_metric = elapsed / num_metrics
            print(f"   {num_metrics:3d} metrics: {elapsed:7.2f}ms ({per_metric:.2f}ms each)")
        
        # Should be roughly linear
        ratios = []
        prev_time = times[10]
        for num_metrics in [25, 50, 100]:
            ratio = times[num_metrics] / prev_time
            ratios.append(ratio)
            prev_time = times[num_metrics]
        
        avg_ratio = statistics.mean(ratios)
        # Should roughly double when metrics double
        self.assertLess(avg_ratio, 3.0, "Non-linear scaling detected")


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)