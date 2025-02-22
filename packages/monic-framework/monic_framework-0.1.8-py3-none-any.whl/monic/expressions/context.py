#
# Monic Framework
#
# Copyright (c) 2024-2025 Cognica, Inc.
#

from dataclasses import dataclass


@dataclass
class ExpressionsContext:
    # Allow return statements at top-level
    allow_return_at_top_level: bool = False

    # The timeout for evaluating the expression in seconds.
    timeout: float | None = 10.0

    # Whether to enable CPU profiling.
    enable_cpu_profiling: bool = False
    # The CPU threshold for evaluating the expression in seconds.
    cpu_threshold: float | None = None

    # Whether to enable memory profiling.
    enable_memory_profiling: bool = False
    # The memory threshold for evaluating the expression in bytes.
    memory_threshold: int = 1024 * 1024 * 10  # 10MB
    # The maximum memory for evaluating the expression in bytes.
    max_memory: int | None = None
