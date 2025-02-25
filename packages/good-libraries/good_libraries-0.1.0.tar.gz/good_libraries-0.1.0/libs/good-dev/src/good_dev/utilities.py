from loguru import logger
import inspect
from functools import wraps
import time
from importlib import import_module
from types import ModuleType


class ImportProfiler:
    def __init__(self):
        self.import_times = {}
        self.original_import = __builtins__.__import__

    def profiled_import(self, name, globals=None, locals=None, fromlist=(), level=0):
        start_time = time.time()
        module = self.original_import(name, globals, locals, fromlist, level)
        duration = time.time() - start_time

        if name not in self.import_times:
            self.import_times[name] = duration

        return module

    def __enter__(self):
        __builtins__.__import__ = self.profiled_import
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        __builtins__.__import__ = self.original_import

    def report(self, threshold_ms=0):
        sorted_times = sorted(
            self.import_times.items(), key=lambda x: x[1], reverse=True
        )

        print("\nImport Profiling Results:")
        print("-" * 50)
        print(f"{'Module':<30} {'Time (ms)':<10}")
        print("-" * 50)

        for module, duration in sorted_times:
            ms = duration * 1000
            if ms >= threshold_ms:
                print(f"{module:<30} {ms:>.2f}")
