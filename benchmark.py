from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path
from time import perf_counter


def nested_loops(limit: int = 10000) -> tuple[float, int]:
    start = perf_counter()
    total = 0
    for outer in range(limit):
        for inner in range(limit):
            total += outer + inner
    return perf_counter() - start, total


def file_io(size_mb: int = 50) -> float:
    start = perf_counter()
    with tempfile.TemporaryDirectory() as tmpdir:
        payload = os.urandom(size_mb * 1024 * 1024)
        target = Path(tmpdir) / "benchmark.bin"
        target.write_bytes(payload)
        _ = target.read_bytes()
    return perf_counter() - start


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a simple CPU and file I/O benchmark for language comparison."
    )
    parser.add_argument(
        "--loop-limit",
        type=int,
        default=10000,
        help="Upper bound used for the nested loop benchmark.",
    )
    parser.add_argument(
        "--size-mb",
        type=int,
        default=50,
        help="Size of the random binary file used for the I/O benchmark.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    loops_time, checksum = nested_loops(args.loop_limit)
    io_time = file_io(args.size_mb)

    print("Python benchmark results")
    print(
        f"Nested loops ({args.loop_limit}x{args.loop_limit}): "
        f"{loops_time:.4f}s | checksum={checksum}"
    )
    print(f"Write + read {args.size_mb} MB file: {io_time:.4f}s")


if __name__ == "__main__":
    main()
