from __future__ import annotations

import os
import tempfile
from pathlib import Path
from time import perf_counter


def nested_loops(limit: int = 1000) -> tuple[float, int]:
    start = perf_counter()
    total = 0
    for outer in range(limit):
        for inner in range(limit):
            total += outer + inner
    return perf_counter() - start, total


def file_io(size_mb: int = 20) -> float:
    start = perf_counter()
    with tempfile.TemporaryDirectory() as tmpdir:
        payload = os.urandom(size_mb * 1024 * 1024)
        target = Path(tmpdir) / "benchmark.bin"
        target.write_bytes(payload)
        _ = target.read_bytes()
    return perf_counter() - start


def main() -> None:
    loops_time, checksum = nested_loops()
    io_time = file_io()

    print("Python benchmark results")
    print(f"Nested loops (1000x1000): {loops_time:.4f}s | checksum={checksum}")
    print(f"Write + read 20 MB file: {io_time:.4f}s")


if __name__ == "__main__":
    main()
