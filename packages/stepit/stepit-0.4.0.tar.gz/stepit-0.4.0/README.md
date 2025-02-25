# stepit

Yet another python decorator for persistent caching. `stepit` caches function results based on their source code and arguments, automatically invalidating the cache when either changes.

## Key Features

- **Smart Cache Invalidation**: Cache is updated when function source code changes
- **Recursive Awareness**: Tracks changes in nested function calls
- **Informative Logging**: Color-coded progress and status messages
- **Zero Configuration**: Works out of the box with sensible defaults
- **Customizable**: Supports custom cache keys, directories, and serialization

## Installation

```sh
pip install stepit
```

## Quick Start

```python
from stepit import stepit

@stepit
def expensive_calculation(x):
    # ... complex computation ...
    return result

# First call: computes and caches
result = expensive_calculation(42)
# Second call: uses cache
result = expensive_calculation(42)
```

## Advanced Usage

### Recursive Functions with Automatic Cache Invalidation

```python
@stepit
def fibonacci(n):
    if n <= 1: return n
    return fibonacci(n-1) + fibonacci(n-2)

# First run: calculates and caches all intermediate results
fibonacci(100)

# Change the function
@stepit
def fibonacci(n):  # Different implementation
    if n <= 0: return 0
    if n == 1: return 1
    return fibonacci(n-1) + fibonacci(n-2)

# Cache is automatically invalidated due to source code change
fibonacci(100)
```

### Custom Cache Configuration

```python
@stepit(
    key="my_special_function",
    cache_dir="custom_cache"
)
def process_data(x):
    return x * 2
```

### Informative Logging

```python
import logging
logging.getLogger("stepit").setLevel(logging.DEBUG)

@stepit
def add(a, b):
    return a + b

add(1, 2)  # Outputs:
# ⏩ stepit 'add': Starting execution of `__main__.add()`
# ✅ stepit 'add': Successfully completed and cached [exec time 0 seconds, size 37 bytes]
# ♻️  stepit 'add': is up-to-date. Using cached result
```

## Use Cases

- Data processing pipelines
- Scientific computations
- Machine learning model training
- Any expensive computations that may be repeated

## How It Works

1. Creates a unique key based on:
   - Function's source code
   - Arguments
   - Any nested `@stepit`-decorated function calls
2. Checks if result exists in cache
3. Executes function if:
   - No cached result exists
   - Source code has changed
   - Arguments are different
4. Stores result in cache for future use

## License

MIT License

## Contributing

Contributions welcome! Please check our GitHub repository for guidelines.

