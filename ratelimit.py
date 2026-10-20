"""Rate limiting that does not reset when a visitor refreshes the page.

The per-session limit in the UI stops fast clicking. This one is shared by every visitor
of the running app, so opening a new tab does not give a fresh allowance.
"""
import threading
import time
from collections import deque


class SlidingWindowLimiter:
    def __init__(self, max_requests: int, window_seconds: float = 60.0):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._times: deque[float] = deque()
        self._lock = threading.Lock()

    def allow(self, now: float | None = None) -> bool:
        now = time.time() if now is None else now
        with self._lock:
            while self._times and now - self._times[0] >= self.window_seconds:
                self._times.popleft()
            if len(self._times) >= self.max_requests:
                return False
            self._times.append(now)
            return True
