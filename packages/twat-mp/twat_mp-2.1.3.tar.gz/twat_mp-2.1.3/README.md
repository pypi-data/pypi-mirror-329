# twat-mp

(work in progress)

Parallel processing utilities using the Pathos multiprocessing library. This package provides convenient context managers and decorators for parallel processing, with both process-based and thread-based pools.

## Features

* Context managers for both process and thread pools:
  + `ProcessPool`: For CPU-intensive parallel processing
  + `ThreadPool`: For I/O-bound parallel processing
* Decorators for common parallel mapping operations:
  + `amap`: Asynchronous parallel map with automatic result retrieval
  + `imap`: Lazy parallel map returning an iterator
  + `pmap`: Standard parallel map (eager evaluation)
* Automatic CPU core detection for optimal pool sizing
* Clean resource management with context managers
* Full type hints and modern Python features
* Flexible pool configuration with customizable worker count

## Installation

```bash
pip install twat-mp
```

## Usage

### Using Process and Thread Pools

The package provides dedicated context managers for both process and thread pools:

```python
from twat_mp import ProcessPool, ThreadPool

# For CPU-intensive operations
with ProcessPool() as pool:
    results = pool.map(lambda x: x * x, range(10))
    print(list(results))  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# For I/O-bound operations
with ThreadPool() as pool:
    results = pool.map(lambda x: x * 2, range(10))
    print(list(results))  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Custom number of workers
with ProcessPool(nodes=4) as pool:
    results = pool.map(lambda x: x * x, range(10))
```

### Using Map Decorators

The package provides three decorators for different mapping strategies:

```python
from twat_mp import amap, imap, pmap

# Standard parallel map (eager evaluation)
@pmap
def square(x: int) -> int:
    return x * x

results = list(square(range(10)))
print(results)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# Lazy parallel map (returns iterator)
@imap
def cube(x: int) -> int:
    return x * x * x

for result in cube(range(5)):
    print(result)  # Prints results as they become available

# Asynchronous parallel map with automatic result retrieval
@amap
def double(x: int) -> int:
    return x * 2

results = list(double(range(10)))
print(results)  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

### Function Composition

Decorators can be composed for complex parallel operations:

```python
from twat_mp import amap

@amap
def compute_intensive(x: int) -> int:
    result = x
    for _ in range(1000):  # Simulate CPU-intensive work
        result = (result * x + x) % 10000
    return result

@amap
def io_intensive(x: int) -> int:
    import time
    time.sleep(0.001)  # Simulate I/O wait
    return x * 2

# Chain parallel operations
results = list(io_intensive(compute_intensive(range(100))))
```

## Dependencies

* `pathos`: For parallel processing functionality

## Development

To set up the development environment:

```bash
# Install in development mode with test dependencies
uv pip install -e ".[test]"

# Run tests
python -m pytest tests/

# Run benchmarks
python -m pytest tests/test_benchmark.py
```

## License

MIT License
.
