"""Utility functions for DevPulse."""

import time
from collections.abc import Generator
from contextlib import contextmanager


@contextmanager
def timer() -> Generator[list[float], None, None]:
    """Context manager to measure execution time.

    Usage:
        with timer() as elapsed:
            # do work
        print(f"Took {elapsed[0]}ms")
    """
    start = time.perf_counter()
    elapsed = [0.0]
    try:
        yield elapsed
    finally:
        elapsed[0] = (time.perf_counter() - start) * 1000


def parse_urls(input_str: str) -> list[str]:
    """Parse URLs from comma-separated string or file path.

    Args:
        input_str: Either a comma-separated list of URLs or a file path

    Returns:
        List of URLs
    """
    # Check if it's a file
    try:
        with open(input_str) as f:
            urls = [line.strip() for line in f if line.strip()]
            return urls
    except (OSError, FileNotFoundError):
        # Treat as comma-separated URLs
        return [url.strip() for url in input_str.split(",") if url.strip()]
