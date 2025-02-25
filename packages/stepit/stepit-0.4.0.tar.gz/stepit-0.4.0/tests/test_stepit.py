import glob
import os
import shutil
import time

import pytest

from stepit import default_deserialize, stepit


def test_stepit_defaults(caplog: pytest.LogCaptureFixture):
    """Test with defaults, that a stepit-decorated function saves its result to
    cache and when args are the same, that it reads from cache instead of running again,"""
    cache_dir = ".stepit_cache"
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)

    @stepit
    def a(x):
        time.sleep(5)
        return x + 2

    with pytest.raises(FileNotFoundError):
        default_deserialize(f"{cache_dir}/a")

    start_time = time.time()
    a(5)
    elapsed_time = time.time() - start_time
    assert "Starting execution" in caplog.text
    assert "Successfully completed and cached" in caplog.text
    assert elapsed_time >= 5
    assert default_deserialize(f"{cache_dir}/a") == 7
    caplog.clear()

    start_time = time.time()
    a(5)
    elapsed_time = time.time() - start_time
    assert "is up-to-date. Using cached result" in caplog.text
    assert "Starting execution" not in caplog.text
    assert "Successfully completed and cached" not in caplog.text
    assert elapsed_time < 2


def test_stepit_change_source(caplog: pytest.LogCaptureFixture):
    """Test that updating a stepit-decorated function (changing its source code)
    results in the function being executed again, when called with the same args"""
    cache_dir = ".stepit_cache"
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)

    @stepit
    def a(x):
        time.sleep(5)
        return x + 2

    with pytest.raises(FileNotFoundError):
        default_deserialize(f"{cache_dir}/a")

    start_time = time.time()
    a(5)
    elapsed_time = time.time() - start_time
    assert "Starting execution" in caplog.text
    assert "Successfully completed and cached" in caplog.text
    assert elapsed_time >= 5
    assert default_deserialize(f"{cache_dir}/a") == 7
    caplog.clear()

    @stepit
    def a(x):
        time.sleep(5)
        return x + 3  # fn changed, so it should induce re-running it with same args

    start_time = time.time()
    a(5)
    elapsed_time = time.time() - start_time
    assert "Starting execution" in caplog.text
    assert "Successfully completed and cached" in caplog.text
    assert elapsed_time >= 5
    assert default_deserialize(f"{cache_dir}/a") == 8
    caplog.clear()


def test_stepit_recursive_invalidation(caplog: pytest.LogCaptureFixture):
    """Test that updating a stepit-decorated function (changing its source code)
    results in the function being executed again, when called with the same args"""

    cache_dir = ".stepit_cache"
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)

    @stepit
    def a(x):
        time.sleep(5)
        return b(x) + c(x)

    @stepit
    def b(x):
        time.sleep(5)
        return x + 2

    @stepit
    def c(x):
        time.sleep(5)
        return x + 3

    with pytest.raises(FileNotFoundError):
        default_deserialize(f"{cache_dir}/a")
    with pytest.raises(FileNotFoundError):
        default_deserialize(f"{cache_dir}/b")
    with pytest.raises(FileNotFoundError):
        default_deserialize(f"{cache_dir}/c")

    start_time = time.time()
    a(5)
    elapsed_time = time.time() - start_time
    assert "Starting execution" in caplog.text
    assert "Successfully completed and cached" in caplog.text
    assert elapsed_time >= 15
    assert default_deserialize(f"{cache_dir}/a") == 15
    assert default_deserialize(f"{cache_dir}/b") == 7
    assert default_deserialize(f"{cache_dir}/c") == 8
    caplog.clear()

    start_time = time.time()
    a(5)
    elapsed_time = time.time() - start_time
    assert "is up-to-date. Using cached result" in caplog.text
    assert "Starting execution" not in caplog.text
    assert "Successfully completed and cached" not in caplog.text
    assert elapsed_time < 2
    caplog.clear()

    @stepit
    def b(x):
        time.sleep(5)
        return x + 7

    start_time = time.time()
    a(5)
    elapsed_time = time.time() - start_time
    assert "Starting execution" in caplog.text
    assert "Successfully completed and cached" in caplog.text
    assert "is up-to-date. Using cached result" in caplog.text  # c() did not change
    assert 10 <= elapsed_time <= 15
    assert default_deserialize(f"{cache_dir}/a") == 20
    assert default_deserialize(f"{cache_dir}/b") == 12
    assert default_deserialize(f"{cache_dir}/c") == 8
    caplog.clear()


def test_stepit_simple_recursive_change():
    cache_dir = ".stepit_cache"
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)

    @stepit  # No arguments, takes defaults
    def f(x):
        time.sleep(5)
        return g(x) + 1  # Calls g()

    @stepit
    def g(x):
        time.sleep(5)
        return x * 2

    start_time = time.time()
    f(7)
    elapsed_time = time.time() - start_time
    assert elapsed_time >= 10

    # should be cached
    start_time = time.time()
    f(7)
    elapsed_time = time.time() - start_time
    assert elapsed_time < 1

    # Redefining g(x) (Should Trigger Cache Invalidation)
    @stepit
    def g(x):  # Small change in function
        time.sleep(5)
        return x * 9  # Previously was x * 2

    # f() did not change directly, but g()'s change should invalidate f() cache
    start_time = time.time()
    f(7)
    elapsed_time = time.time() - start_time
    assert elapsed_time >= 10, "Did not induce f's invalidation"


def test_stepit_fibonacci():
    cache_dir = ".stepit_cache"
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)

    def fibonacci(n):
        # noqa
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fibonacci(n - 1) + fibonacci(n - 2)

    start_time = time.time()
    fibonacci(35)
    fibo_time = time.time() - start_time

    @stepit
    def fibonacci_stepit(n):
        # noqa
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fibonacci_stepit(n - 1) + fibonacci_stepit(n - 2)

    start_time = time.time()
    fibonacci_stepit(35)
    stepit_time = time.time() - start_time

    assert stepit_time < fibo_time

    assert len(glob.glob(f"{cache_dir}/fibonacci_stepit*")) == 37

    start_time = time.time()
    fibonacci_stepit(35)
    cache35_time = time.time() - start_time

    start_time = time.time()
    fibonacci_stepit(34)
    cache34_time = time.time() - start_time

    start_time = time.time()
    fibonacci_stepit(33)
    cache33_time = time.time() - start_time

    start_time = time.time()
    fibonacci_stepit(32)
    cache32_time = time.time() - start_time

    assert cache35_time < stepit_time
    assert cache34_time < stepit_time
    assert cache33_time < stepit_time
    assert cache32_time < stepit_time


def test_stepit_customize(caplog: pytest.LogCaptureFixture):
    """Test customizing the key and cache_dir, and updating those parameters
    for a stepit-decorated function"""

    cache_dir = ".custom_stepit_cache"
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)

    @stepit(key="key_to_result", cache_dir=cache_dir)
    def a(x):
        time.sleep(5)
        return x + 2

    with pytest.raises(FileNotFoundError):
        default_deserialize(f"{cache_dir}/key_to_result")

    start_time = time.time()
    a(5)
    elapsed_time = time.time() - start_time
    assert "Starting execution" in caplog.text
    assert "Successfully completed and cached" in caplog.text
    assert elapsed_time >= 5
    assert default_deserialize(f"{cache_dir}/key_to_result") == 7
    caplog.clear()

    start_time = time.time()
    a(5)
    elapsed_time = time.time() - start_time
    assert "is up-to-date. Using cached result" in caplog.text
    assert "Starting execution" not in caplog.text
    assert "Successfully completed and cached" not in caplog.text
    assert elapsed_time < 2
    caplog.clear()

    cache_dir = ".new_stepit_cache_dir"
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)

    start_time = time.time()
    a.update(key="new_key_to_result", cache_dir=cache_dir)(5)
    elapsed_time = time.time() - start_time
    assert "Starting execution" in caplog.text
    assert "Successfully completed and cached" in caplog.text
    assert elapsed_time >= 5
    assert default_deserialize(f"{cache_dir}/new_key_to_result") == 7
    caplog.clear()


def test_formatters():
    from stepit.stepit import format_size, format_time

    assert format_size(45) == "45 bytes"
    assert format_size(7500) == "7.3 KB"
    assert format_size(9500000) == "9.1 MB"
    assert format_size(2**64) == "16777216 TB"
    assert format_size(45e10) == "419.1 GB"
    #
    assert format_time(7) == "7 seconds"
    assert format_time(67) == "1.1 minutes"
    assert format_time(5027) == "1.4 hours"
    assert format_time(765027) == "8.9 days"
    assert format_time(60 * 4) == "4 minutes"
    assert format_time(60 * 60) == "1 hours"
    assert format_time(60 * 60 * 24) == "1 days"
    