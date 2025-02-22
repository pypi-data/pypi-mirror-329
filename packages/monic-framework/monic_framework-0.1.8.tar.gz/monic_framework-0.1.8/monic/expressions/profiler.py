#
# Monic Framework
#
# Copyright (c) 2024-2025 Cognica, Inc.
#

import gc
import tracemalloc

from dataclasses import dataclass


@dataclass
class MemorySnapshot:
    """Memory snapshot information."""

    total_allocated: int
    peak_allocated: int
    current_objects: dict[str, int]
    peak_frame: tracemalloc.Frame | None = None


class MemoryProfiler:
    def __init__(self):
        self.snapshots: list[MemorySnapshot] = []
        self.peak_snapshot: MemorySnapshot | None = None

    def start(self):
        tracemalloc.start()

    def stop(self):
        tracemalloc.stop()

    def take_snapshot(self) -> MemorySnapshot:
        """Create a snapshot of the current memory state."""
        snapshot = tracemalloc.take_snapshot()
        stats = snapshot.statistics("filename")

        # Count objects by type
        gc.collect()  # Run GC for accurate measurement
        objects = {}
        for obj in gc.get_objects():
            obj_type = type(obj).__name__
            objects[obj_type] = objects.get(obj_type, 0) + 1

        peak_allocated = 0
        peak_frame: tracemalloc.Frame | None = None
        top_stats = snapshot.statistics("traceback")
        if top_stats:
            peak_allocated = top_stats[0].size
            peak_frame = (
                top_stats[0].traceback[0] if top_stats[0].traceback else None
            )

        current = MemorySnapshot(
            total_allocated=sum(stat.size for stat in stats),
            peak_allocated=peak_allocated,
            current_objects=objects,
            peak_frame=peak_frame,
        )

        self.snapshots.append(current)
        if (
            not self.peak_snapshot
            or current.total_allocated > self.peak_snapshot.total_allocated
        ):
            self.peak_snapshot = current

        return current
