"""Benchmark tests for twat_mp."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from twat_mp import ProcessPool, ThreadPool, amap, imap, mmap, pmap

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator


def _compute_intensive(x: int) -> int:
    """Compute-intensive operation for benchmarking."""
    result = x
    for _ in range(1000):  # Simulate CPU-intensive work
        result = (result * x + x) % 10000
    return result


def _io_intensive(x: int) -> int:
    """I/O-intensive operation for benchmarking."""
    import time

    time.sleep(0.001)  # Simulate I/O wait
    return x * 2


def generate_data(size: int) -> list[int]:
    """Generate test data of specified size."""
    return list(range(size))


@pytest.fixture
def small_data() -> list[int]:
    """Fixture for small dataset."""
    return generate_data(100)


@pytest.fixture
def medium_data() -> list[int]:
    """Fixture for medium dataset."""
    return generate_data(1000)


@pytest.fixture
def large_data() -> list[int]:
    """Fixture for large dataset."""
    return generate_data(10000)


def run_parallel_operation(
    func: Callable[[int], int],
    data: list[int] | Iterator[int],
    parallel_impl: Callable[
        [Callable[[Any], Any]], Callable[[list[Any] | Iterator[Any]], Iterator[Any]]
    ],
) -> list[int]:
    """Run a parallel operation with given implementation."""
    parallel_func = parallel_impl(func)
    return list(parallel_func(data))


@pytest.mark.benchmark
class TestComputeIntensiveBenchmarks:
    """Benchmark suite for compute-intensive operations."""

    def test_sequential_vs_process_pool(self, benchmark, medium_data):
        """Compare sequential vs process pool performance for compute-intensive work."""

        def sequential() -> list[int]:
            return list(map(_compute_intensive, medium_data))

        def parallel() -> list[int]:
            with ProcessPool() as pool:
                return list(pool.map(_compute_intensive, medium_data))

        result = sequential()  # Run once to get result
        assert parallel() == result  # Verify results match

        # Benchmark both implementations in a single call
        def run_both() -> tuple[list[int], list[int]]:
            return sequential(), parallel()

        benchmark(run_both)

    @pytest.mark.parametrize("data_size", [100, 1000, 10000])
    def test_parallel_implementations(self, benchmark, data_size):
        """Compare different parallel implementations with varying data sizes."""
        data = generate_data(data_size)

        def process_map(
            f: Callable[[Any], Any],
        ) -> Callable[[Any], Iterator[Any]]:
            return mmap(how="map")(f)

        def thread_map(
            f: Callable[[Any], Any],
        ) -> Callable[[Any], Iterator[Any]]:
            def wrapper(iterable: Any) -> Iterator[Any]:
                with ThreadPool() as pool:
                    return pool.map(f, iterable)

            return wrapper

        implementations = {
            "process_pool": process_map,
            "thread_pool": thread_map,
            "amap": lambda f: amap(f),
            "imap": lambda f: imap(f),
            "pmap": lambda f: pmap(f),
        }

        # Run once to get reference result
        reference_impl = implementations["process_pool"]
        reference_result = run_parallel_operation(
            _compute_intensive, data, reference_impl
        )

        # Verify all implementations produce the same result
        results = {}
        for name, impl in implementations.items():
            result = run_parallel_operation(_compute_intensive, data, impl)
            assert result == reference_result  # Verify results match
            results[name] = result

        # Benchmark all implementations in a single call
        def run_all() -> dict[str, list[int]]:
            return {
                name: run_parallel_operation(_compute_intensive, data, impl)
                for name, impl in implementations.items()
            }

        benchmark(run_all)


@pytest.mark.benchmark
class TestIOIntensiveBenchmarks:
    """Benchmark suite for I/O-intensive operations."""

    def test_thread_vs_process_pool(self, benchmark, medium_data):
        """Compare thread pool vs process pool for I/O-intensive work."""

        def process_pool() -> list[int]:
            with ProcessPool() as pool:
                return list(pool.map(_io_intensive, medium_data))

        def thread_pool() -> list[int]:
            with ThreadPool() as pool:
                return list(pool.map(_io_intensive, medium_data))

        result = process_pool()  # Run once to get result
        assert thread_pool() == result  # Verify results match

        # Benchmark both implementations in a single call
        def run_both() -> tuple[list[int], list[int]]:
            return process_pool(), thread_pool()

        benchmark(run_both)


@pytest.mark.benchmark
class TestScalabilityBenchmarks:
    """Benchmark suite for testing scalability with different numbers of workers."""

    @pytest.mark.parametrize("nodes", [2, 4, 8, 16])
    def test_worker_scaling(self, benchmark, medium_data, nodes):
        """Test how performance scales with different numbers of worker processes."""

        def run_with_workers() -> list[int]:
            with ProcessPool(nodes=nodes) as pool:
                return list(pool.map(_compute_intensive, medium_data))

        benchmark(run_with_workers)


@pytest.mark.benchmark
class TestCompositionBenchmarks:
    """Benchmark suite for testing composed parallel operations."""

    def test_chained_operations(self, benchmark, medium_data):
        """Test performance of chained parallel operations."""

        def sequential_chain() -> list[int]:
            return [_io_intensive(_compute_intensive(x)) for x in medium_data]

        def parallel_chain() -> list[int]:
            compute = amap(_compute_intensive)
            io_op = amap(_io_intensive)
            return list(io_op(compute(medium_data)))

        result = sequential_chain()  # Run once to get result
        assert parallel_chain() == result  # Verify results match

        # Benchmark both implementations in a single call
        def run_both() -> tuple[list[int], list[int]]:
            return sequential_chain(), parallel_chain()

        benchmark(run_both)
