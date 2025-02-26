import functools
import hashlib
import inspect
import logging
import os
import pickle
import time

# Set up logging
logger = logging.getLogger("stepit")
logger.setLevel(logging.INFO)  # NOTSET
handler = logging.StreamHandler()

# Define colors
COLORS = {
    "INFO": "\033[94m",  # Blue
    "DEBUG": "\033[95m",  # Purple
    "WARNING": "\033[93m",  # Yellow
    "ERROR": "\033[91m",  # Red
    "SUCCESS": "\033[92m",  # Green
    "RESET": "\033[0m",  # Reset to default
}


class ColorFormatter(logging.Formatter):
    def format(self, record):
        color = COLORS.get(record.levelname, COLORS["RESET"])
        return f"{color}{record.getMessage()}{COLORS['RESET']}"


handler.setFormatter(ColorFormatter())
logger.addHandler(handler)


def default_serialize(result, filename):
    """Serialize using pickle."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        pickle.dump(result, f)


def default_deserialize(filename):
    """Deserialize using pickle."""

    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except Exception:
        with open(filename, "r") as f:
            real_file = f.readline().strip()
            filename = real_file
        with open(filename, "rb") as f:
            return pickle.load(f)


def format_size(size):
    """
    Convert size to a human-readable format with appropriate units.

    Args:
        size (int or float): The size in bytes.

    Returns:
        str: A string representing the size in a human-readable format (e.g., "10 bytes", "2.5 KB", "1.8 MB").
    """
    for unit in ["bytes", "KB", "MB", "GB"]:
        if size < 1024.0:
            return f"{int(size)} {unit}" if (size % 1) == 0 else f"{size:.1f} {unit}"
        size /= 1024.0

    unit = "TB"
    return f"{int(size)} {unit}" if (size % 1) == 0 else f"{size:.1f} {unit}"


def format_time(seconds):
    """Converts a given number of seconds into a human-readable time format.

    The function iteratively checks if the remaining time is less than 60, and if so,
    formats the time with the appropriate unit (seconds, minutes, hours, or days).
    If the time is less than 60 seconds, it returns the time as an integer number of seconds.
    Otherwise, it returns the time as a float with one decimal place, along with the unit.

    Args:
        seconds (float): The number of seconds to convert.

    Returns:
        str: A string representing the formatted time.
             Examples: "5 seconds", "1.5 minutes", "2.3 hours", "1.1 days"
    """
    units = [("seconds", 60), ("minutes", 60), ("hours", 24), ("days", None)]

    seconds = float(seconds)  # Ensure float division
    for unit, threshold in units:
        if threshold is None or seconds < threshold:
            return (
                f"{int(seconds)} {unit}"
                if seconds.is_integer()
                else f"{seconds:.1f} {unit}"
            )
        seconds /= threshold  # Convert to the next unit


def _compute_args_hash(func, args, kwargs):
    logger.debug(f"Computing hash for args passed to fn: {func.__qualname__}")
    logger.debug(f"Hash for args: {args}, kwargs: {kwargs}")
    try:
        pickled_args = pickle.dumps((args, kwargs))
    except Exception:
        pickled_args = func.__qualname__
        logger.warning(f"Cannot pickle args for {func.__qualname__}")

    args_hash = hashlib.md5(pickled_args).hexdigest()
    logger.debug(f"Resulting hash for args: {args_hash}")
    return args_hash


def _compute_source_hash(func, seen=None):
    """Computes a hash of the function's source code and, recursively,
    all stepit-decorated functions it calls."""

    if seen is None:
        seen = set()
    if func in seen:
        return ""

    seen.add(func)

    try:
        logger.debug(f"Computing hash for function {func.__qualname__}")
        source = inspect.getsource(func)
        logger.debug(f"Source code: {source}")
    except Exception:
        logger.warning(f"Couldn't get the source for: {func.__qualname__}")
        source = func.__qualname__  # fallback

    try:
        fnclvrs = inspect.getclosurevars(func)
        logger.debug(f"nonlocals: {fnclvrs.nonlocals}")
        logger.debug(f"globals: {fnclvrs.globals}")
        logger.debug(f"globals: {fnclvrs.builtins}")
        logger.debug(f"globals: {fnclvrs.unbound}")

        for name, value in {**fnclvrs.nonlocals, **fnclvrs.globals}.items():
            if callable(value) and hasattr(value, "__stepit__"):
                source += _compute_source_hash(value, seen)

    except Exception as e:
        logger.warning(f"Couldn't get closurevars: {func.__qualname__}, {e}")

    source_hash = hashlib.md5(source.encode("utf-8")).hexdigest()
    logger.debug(f"Final hash for function source: {source_hash}")
    return source_hash


def create_symlink(symlink_path, target_file):
    """Creates a plain text file containing the target file's path."""
    try:
        with open(symlink_path, "w") as f:
            f.write(target_file)
    except OSError as e:
        logger.error(f"Failed to create text file: {e}")


def stepit(
    func=None,
    *,
    key=None,
    cache_dir=".stepit_cache",
    serialize=default_serialize,
    deserialize=default_deserialize,
):
    """
    Decorator for persistent caching. Can be used with or without arguments:

        @stepit
        def my_func(x): ...

        @stepit(key="custom_key", cache_dir="my_cache")
        def my_func(x): ...

    The cache key is based on:
      - A custom prefix (if provided) or the function's fully qualified name by default.
      - A recursive hash of its source (including decorated functions it calls).
      - A hash of the call arguments.
    """
    if callable(func):
        return stepit()(func)

    def decorator(func):
        nonlocal key
        if key is None:
            # key = f"{func.__module__}.{func.__qualname__}"
            key = f"{func.__name__}"
            # let's use the simplest name (qual would need to be cleaned to be able
            # to be used as a filename)

        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)

        config = {
            "key": key,
            "cache_dir": cache_dir,
            "serialize": serialize,
            "deserialize": deserialize,
        }

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_hash = _compute_args_hash(func, args, kwargs)
            source_hash = _compute_source_hash(func)

            current = wrapper.__stepit_config__
            cache_file = os.path.join(
                current["cache_dir"], f"{current['key']}_{source_hash}_{args_hash}"
            )
            key_file = os.path.join(current["cache_dir"], f"{current['key']}")

            if os.path.exists(cache_file):
                try:
                    logger.info(
                        f"♻️  stepit '{config['key']}': is up-to-date. "
                        f"Using cached result for "
                        f"`{func.__module__}.{func.__qualname__}()` "
                        f"{time.strftime('%Y-%m-%d %H:%M:%S')}"
                    )

                    create_symlink(key_file, cache_file)
                    return current["deserialize"](cache_file)

                except Exception as e:
                    logger.warning(
                        f"⚠️ stepit '{config['key']}': Could not load cache. "
                        f"Need to execute again "
                        f"`{func.__module__}.{func.__qualname__}()` "
                        f"Underlying exception: {e}"
                    )

            logger.info(
                f"⏩ stepit '{config['key']}': Starting execution of "
                f"`{func.__module__}.{func.__qualname__}()` "  # ▶
                f"{time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            start_time = time.time()
            result = func(*args, **kwargs)
            exec_time = time.time() - start_time

            try:
                start_time = time.time()
                current["serialize"](result, cache_file)
                create_symlink(key_file, cache_file)
                persist_time = time.time() - start_time
                file_size = os.path.getsize(cache_file)

                formatted_size = format_size(file_size)
                formatted_exec_time = format_time(exec_time)
                formatted_persist_time = format_time(persist_time)

                logger.info(
                    f"✅ stepit '{config['key']}': Successfully completed and cached "
                    f"[exec time {formatted_exec_time}, "
                    f"cache time {formatted_persist_time}, size {formatted_size}] "
                    f"`{func.__module__}.{func.__qualname__}()` "
                    f"{time.strftime('%Y-%m-%d %H:%M:%S')}"
                )

            except Exception as e:
                logger.error(
                    f"❌  stepit '{config['key']}': Failed to save cache for "
                    f"`{func.__module__}.{func.__qualname__}()` "
                    f"Underlying exception: {e}"
                )

            return result

        wrapper.__stepit__ = True
        wrapper.__stepit_config__ = config

        def update(**kwargs):
            wrapper.__stepit_config__.update(kwargs)
            if "cache_dir" in kwargs and not os.path.exists(kwargs["cache_dir"]):
                os.makedirs(kwargs["cache_dir"], exist_ok=True)
            return wrapper

        wrapper.update = update
        return wrapper

    return decorator
