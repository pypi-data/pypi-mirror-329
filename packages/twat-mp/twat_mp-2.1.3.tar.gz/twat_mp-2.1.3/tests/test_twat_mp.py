"""Test suite for twat_mp."""

import time
from collections.abc import Iterator
from typing import TypeVar

import pytest

from twat_mp import ProcessPool, ThreadPool, amap, imap, mmap, pmap
from twat_mp.__version__ import version as __version__

T = TypeVar("T")
U = TypeVar("U")

# Test constants
TEST_PROCESS_POOL_SIZE = 2
TEST_THREAD_POOL_SIZE = 3


def test_version():
    """Verify package exposes version."""
    assert __version__


def _square(x: int) -> int:
    """Square a number."""
    return x * x


def _subs(x: int) -> int:
    """Subtract one."""
    return x - 1


# Create decorated versions of the functions
isquare = amap(_square)
isubs = amap(_subs)


def test_process_pool_context():
    """Test ProcessPool context manager functionality."""
    with ProcessPool() as pool:
        result = list(pool.map(_square, iter(range(5))))
        assert result == [0, 1, 4, 9, 16]


def test_thread_pool_context():
    """Test ThreadPool context manager functionality."""
    with ThreadPool() as pool:
        result = list(pool.map(_square, iter(range(5))))
        assert result == [0, 1, 4, 9, 16]


def test_amap_decorator():
    """Test async parallel map decorator."""
    result = list(isquare(iter(range(5))))
    assert result == [0, 1, 4, 9, 16]


def test_pmap_decorator():
    """Test standard parallel map decorator."""
    psquare = pmap(_square)
    result = list(psquare(iter(range(5))))
    assert result == [0, 1, 4, 9, 16]


def test_imap_decorator():
    """Test iterator parallel map decorator."""
    isquare_iter = imap(_square)
    result = list(isquare_iter(iter(range(5))))
    assert result == [0, 1, 4, 9, 16]
    # Verify it returns an iterator
    result_iter = isquare_iter(iter(range(5)))
    assert isinstance(result_iter, Iterator)


def test_composed_operations():
    """Test composition of parallel operations."""
    result = list(isubs(isquare(iter(range(5)))))
    assert result == [-1, 0, 3, 8, 15]


def test_pool_nodes_specification():
    """Test pool creation with specific node count."""
    with ProcessPool(nodes=TEST_PROCESS_POOL_SIZE) as pool:
        assert pool.nodes == TEST_PROCESS_POOL_SIZE
    with ThreadPool(nodes=TEST_THREAD_POOL_SIZE) as pool:
        assert pool.nodes == TEST_THREAD_POOL_SIZE


@pytest.mark.benchmark
def test_parallel_vs_sequential_performance():
    """Benchmark parallel vs sequential processing."""
    test_range = range(1000)

    # Sequential processing
    start_time = time.perf_counter()
    seq_result = list(map(_square, test_range))
    time.perf_counter() - start_time

    # Parallel processing
    start_time = time.perf_counter()
    par_result = list(isquare(iter(test_range)))
    time.perf_counter() - start_time

    # Assert results are equal
    assert seq_result == par_result

    # On sufficiently large inputs, parallel should be faster
    # Note: This might not always be true due to overhead, system load, etc.
    # so we don't make it a hard assertion


def test_mmap_decorator_variants():
    """Test mmap decorator with different 'how' parameters."""
    # Test standard map variant
    standard_map = mmap(how="map")(_square)
    result_map = list(standard_map(iter(range(5))))
    assert result_map == [0, 1, 4, 9, 16]

    # Test imap variant
    iter_map = mmap(how="imap")(_square)
    result_imap = list(iter_map(iter(range(5))))
    assert result_imap == [0, 1, 4, 9, 16]
    # Verify it returns an iterator
    result_iter = iter_map(iter(range(5)))
    assert isinstance(result_iter, Iterator)

    # Test amap variant with get_result=True
    async_map = mmap(how="amap", get_result=True)(_square)
    result_amap = list(async_map(iter(range(5))))
    assert result_amap == [0, 1, 4, 9, 16]

    # Verify all variants produce the same results
    assert result_map == result_imap == result_amap
