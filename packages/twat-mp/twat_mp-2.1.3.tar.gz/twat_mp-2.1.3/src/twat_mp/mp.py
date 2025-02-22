"""
Parallel processing utilities using the Pathos multiprocessing library.

This module provides convenient context managers for creating and managing
parallel processing pools (process or thread based) and decorators for applying
parallel map operations to functions. It uses Pathos pools under the hood,
automatically determining the optimal number of processes/threads based on the
system's CPU count if not specified.

Example usage:
    >>> from mp import pmap, imap, amap, ProcessPool, ThreadPool
    >>>
    >>> # Using the parallel map decorator (synchronous mapping)
    >>> @pmap
    ... def square(x: int) -> int:
    ...     return x * x
    >>>
    >>> results = list(square(range(10)))
    >>> print(results)
    [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
"""

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Literal, TypeVar

from pathos.helpers import mp  # Provides CPU count helper
from pathos.pools import ProcessPool as PathosProcessPool
from pathos.pools import ThreadPool as PathosThreadPool

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

# Type variables for generality in mapping functions
T = TypeVar("T")
U = TypeVar("U")

# Define a union type for either a process pool or a thread pool from Pathos
PathosPool = PathosProcessPool | PathosThreadPool
"""Type alias for either a ProcessPool or ThreadPool from Pathos."""


class MultiPool:
    """
    Context manager for managing Pathos parallel processing pools.

    This class abstracts the creation and cleanup of a parallel processing pool.
    It automatically chooses the number of nodes (processes or threads) based on
    the CPU count if not provided. It can be subclassed for specific pool types.

    Attributes:
        pool_class: The Pathos pool class to instantiate.
        nodes: The number of processes/threads to use.
        pool: The actual pool instance (created on entering the context).

    Example:
        >>> with MultiPool(pool_class=PathosProcessPool) as pool:
        ...     results = pool.map(lambda x: x * 2, range(5))
        >>> print(list(results))
    """

    def __init__(
        self, pool_class: type[PathosPool] = PathosProcessPool, nodes: int | None = None
    ) -> None:
        """
        Initialize the MultiPool context manager.

        Args:
            pool_class: The pool class to use (ProcessPool or ThreadPool).
            Defaults to ProcessPool.
            nodes: The number of processes/threads to create.
            If None, uses the CPU count.
        """
        self.pool_class = pool_class
        # If nodes is not specified, determine optimal number based on CPU count.
        self.nodes: int = nodes if nodes is not None else mp.cpu_count()  # type: ignore
        self.pool: PathosPool | None = None  # Pool will be created in __enter__

    def __enter__(self) -> PathosPool:
        """
        Enter the runtime context and create the pool.

        Returns:
            The instantiated pool object.

        Raises:
            RuntimeError: If pool creation fails.
        """
        self.pool = self.pool_class(nodes=self.nodes)
        if self.pool is None:
            # This should rarely happen; raise an error if pool instantiation fails.
            msg = f"Failed to create a pool using {self.pool_class}"
            raise RuntimeError(msg)
        return self.pool

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> Literal[False]:
        """
        Exit the runtime context, ensuring the pool is properly closed and resources are freed.

        Args:
            exc_type: The exception type if an exception was raised.
            exc_value: The exception value if an exception was raised.
            traceback: The traceback if an exception was raised.

        Returns:
            False to indicate that any exception should be propagated.
        """
        if self.pool:
            # Close the pool and join to wait for all tasks to complete
            self.pool.close()
            self.pool.join()
            # Clear the pool to free up resources
            self.pool.clear()
        return False  # Propagate any exception that occurred


class ProcessPool(MultiPool):
    """
    Context manager specifically for creating a process-based pool.

    This subclass of MultiPool defaults to using the ProcessPool from Pathos.

    Example:
        >>> with ProcessPool() as pool:
        ...     results = pool.map(lambda x: x * 2, range(10))
    """

    def __init__(self, nodes: int | None = None) -> None:
        """
        Initialize a ProcessPool with an optional node count.

        Args:
            nodes: Number of processes to use. If None, defaults to the CPU count.
        """
        super().__init__(pool_class=PathosProcessPool, nodes=nodes)


class ThreadPool(MultiPool):
    """
    Context manager specifically for creating a thread-based pool.

    This subclass of MultiPool defaults to using the ThreadPool from Pathos.

    Example:
        >>> with ThreadPool() as pool:
        ...     results = pool.map(lambda x: x * 2, range(10))
    """

    def __init__(self, nodes: int | None = None) -> None:
        """
        Initialize a ThreadPool with an optional node count.

        Args:
            nodes: Number of threads to use. If None, defaults to the CPU count.
        """
        super().__init__(pool_class=PathosThreadPool, nodes=nodes)


def mmap(
    how: str, *, get_result: bool = False
) -> Callable[[Callable[[T], U]], Callable[[Iterator[T]], Iterator[U]]]:
    """
    Create a decorator to perform parallel mapping using a specified Pathos pool method.

    The decorator wraps a function so that when it is called with an iterable,
    the function is applied in parallel using the specified mapping method.
    For asynchronous mapping (e.g., 'amap'), the result's `.get()` method can be
    automatically called to retrieve the computed values.

    Args:
        how: Name of the pool mapping method ('map', 'imap', or 'amap').
        get_result: If True, automatically call .get() on the result (useful for amap).
                    Defaults to False.

    Returns:
        A decorator function that transforms the target function for parallel execution.

    Example:
        >>> @mmap('map')
        ... def cube(x: int) -> int:
        ...     return x ** 3
        >>> results = list(cube(range(5)))
        >>> print(results)
        [0, 1, 8, 27, 64]
    """

    def decorator(func: Callable[[T], U]) -> Callable[[Iterator[T]], Iterator[U]]:
        @wraps(func)
        def wrapper(iterable: Iterator[T], *args: Any, **kwargs: Any) -> Any:
            # Create a MultiPool context to manage the pool lifecycle
            with MultiPool() as pool:
                # Dynamically fetch the mapping method (map, imap, or amap)
                mapping_method = getattr(pool, how)
                result = mapping_method(func, iterable)
                # For asynchronous mapping, call .get() to obtain the actual results
                if get_result:
                    result = result.get()
                return result

        return wrapper

    return decorator


# Convenience decorators for common mapping strategies:
imap = mmap(how="imap")  # Lazy evaluation: returns an iterator
amap = mmap(how="amap", get_result=True)  # Async evaluation with automatic .get()
pmap = mmap(how="map")  # Standard parallel map (eager evaluation)
