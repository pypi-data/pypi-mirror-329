"""
hot_reload.py - Automatic module reloading for development
"""
import importlib
import logging
import sys
import time
from pathlib import Path
from threading import Thread, Event
from typing import List, Optional, Dict, Set
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

from .pprint import ppi, ppw

logger = logging.getLogger(__name__)


class ModuleReloader(FileSystemEventHandler):
    """Handles file system events and reloads modified modules."""

    def __init__(self,
                 modules_to_watch: Optional[List[str]] = None,
                 paths_to_watch: Optional[List[str]] = None,
                 callback: Optional[callable] = None):
        super().__init__()
        self.modules_to_watch = set(modules_to_watch or [])
        self.paths_to_watch = set(paths_to_watch or [])
        self.callback = callback
        self._last_reload_time: Dict[str, float] = {}
        self._debounce_interval = 0.5  # seconds

    def on_modified(self, event: FileModifiedEvent):
        if not event.src_path.endswith('.py'):
            return

        # Debounce to prevent multiple reloads
        current_time = time.time()
        if (event.src_path in self._last_reload_time and
                current_time - self._last_reload_time[event.src_path] < self._debounce_interval):
            return

        self._last_reload_time[event.src_path] = current_time

        # Get module name from file path
        module_path = Path(event.src_path)
        module_name = module_path.stem

        # Check if this module should be reloaded
        if (module_name in self.modules_to_watch or
                str(module_path) in self.paths_to_watch or
                any(str(module_path).startswith(str(p)) for p in self.paths_to_watch)):

            try:
                # Find all modules that need to be reloaded
                modules_to_reload = self._find_dependent_modules(module_name)

                # Reload modules in dependency order
                for mod_name in modules_to_reload:
                    if mod_name in sys.modules:
                        importlib.reload(sys.modules[mod_name])
                        ppi(f"Reloaded module: {mod_name}")

                if self.callback:
                    self.callback(module_name)

            except Exception as e:
                ppw(f"Error reloading {module_name}: {str(e)}")

    def _find_dependent_modules(self, changed_module: str) -> List[str]:
        """Find all modules that depend on the changed module."""
        dependent_modules = []

        def add_module(mod_name: str):
            if mod_name not in dependent_modules:
                dependent_modules.append(mod_name)

        # Add the changed module first
        add_module(changed_module)

        # Find modules that import the changed module
        for name, module in list(sys.modules.items()):
            if module is None:
                continue

            try:
                # Check module.__spec__ for imports
                if hasattr(module, '__spec__') and module.__spec__:
                    if changed_module in str(module.__spec__):
                        add_module(name)

                # Check module.__file__ to find related modules
                if (hasattr(module, '__file__') and module.__file__ and
                        changed_module in str(Path(module.__file__).parent)):
                    add_module(name)
            except Exception:
                continue

        return dependent_modules


class HotReloader:
    """Manages automatic reloading of Python modules during development."""

    def __init__(self):
        self._observer = Observer()
        self._stop_event = Event()
        self._watch_paths: Set[str] = set()
        self._handler: Optional[ModuleReloader] = None

    def watch(self,
              modules: Optional[List[str]] = None,
              paths: Optional[List[str]] = None,
              callback: Optional[callable] = None) -> None:
        """
        Start watching modules and paths for changes.

        Args:
            modules: List of module names to watch
            paths: List of file system paths to watch
            callback: Optional callback function to call after reload
        """
        # Convert relative paths to absolute
        if paths:
            paths = [str(Path(p).resolve()) for p in paths]

        # Create handler
        self._handler = ModuleReloader(
            modules_to_watch=modules,
            paths_to_watch=paths,
            callback=callback
        )

        # Determine directories to watch
        dirs_to_watch = set()

        # Add module directories
        if modules:
            for module_name in modules:
                if module_name in sys.modules:
                    module = sys.modules[module_name]
                    if hasattr(module, '__file__'):
                        dirs_to_watch.add(str(Path(module.__file__).parent))

        # Add explicit paths
        if paths:
            for path in paths:
                if Path(path).is_file():
                    dirs_to_watch.add(str(Path(path).parent))
                else:
                    dirs_to_watch.add(path)

        # Start watching
        for directory in dirs_to_watch:
            self._observer.schedule(self._handler, directory, recursive=True)
            self._watch_paths.add(directory)
            ppi(f"Watching directory: {directory}")

        if not self._observer.is_alive():
            self._observer.start()

    def stop(self) -> None:
        """Stop watching for changes."""
        self._stop_event.set()
        self._observer.stop()
        self._observer.join()
        self._watch_paths.clear()
        ppi("Stopped watching for changes")


# Global reloader instance
_reloader = HotReloader()


def watch_modules(modules: Optional[List[str]] = None,
                  paths: Optional[List[str]] = None,
                  callback: Optional[callable] = None) -> None:
    """
    Start watching modules and paths for changes.

    Example:
        >>> watch_modules(['my_module'], ['path/to/watch'])
        >>> # or use it as a context manager
        >>> with watch_modules(['my_module']):
        ...     # Do development work
        ...     pass
    """
    _reloader.watch(modules, paths, callback)


def stop_watching() -> None:
    """Stop watching for changes."""
    _reloader.stop()


# Context manager support
class watch_modules_context:
    def __init__(self,
                 modules: Optional[List[str]] = None,
                 paths: Optional[List[str]] = None,
                 callback: Optional[callable] = None):
        self.modules = modules
        self.paths = paths
        self.callback = callback

    def __enter__(self):
        watch_modules(self.modules, self.paths, self.callback)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        stop_watching()