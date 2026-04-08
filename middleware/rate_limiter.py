import time
from collections import defaultdict
from config import RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW_SECONDS

request_log: dict = defaultdict(list)


def is_rate_limited(guest_id: str) -> bool:
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW_SECONDS

    request_log[guest_id] = [
        ts for ts in request_log[guest_id] if ts > window_start
    ]

    if len(request_log[guest_id]) >= RATE_LIMIT_REQUESTS:
        return True

    request_log[guest_id].append(now)
    return False