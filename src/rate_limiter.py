# src/rate_limiter.py
# Rate limiting to prevent API abuse

import time
from collections import defaultdict
from datetime import datetime

# Store: {ip: [timestamp1, timestamp2, ...]}
_request_log = defaultdict(list)

# Settings
MAX_REQUESTS = 30       # max requests per window
WINDOW_SECONDS = 60     # per 60 seconds


# ══════════════════════════════════════════
# CHECK RATE LIMIT
# ══════════════════════════════════════════
def is_rate_limited(client_ip: str) -> bool:
    """
    Returns True if client has exceeded rate limit.
    Uses sliding window algorithm.
    """
    now = time.time()
    window_start = now - WINDOW_SECONDS

    # Remove old requests outside window
    _request_log[client_ip] = [
        t for t in _request_log[client_ip]
        if t > window_start
    ]

    # Check if limit exceeded
    if len(_request_log[client_ip]) >= MAX_REQUESTS:
        print(f"  [RateLimit] BLOCKED: {client_ip} ({len(_request_log[client_ip])} requests)")
        return True

    # Record this request
    _request_log[client_ip].append(now)
    return False


# ══════════════════════════════════════════
# GET RATE LIMIT STATUS
# ══════════════════════════════════════════
def get_rate_limit_status(client_ip: str) -> dict:
    """Returns current rate limit status for an IP"""
    now = time.time()
    window_start = now - WINDOW_SECONDS

    recent = [t for t in _request_log[client_ip] if t > window_start]

    return {
        "ip": client_ip,
        "requests_in_window": len(recent),
        "max_requests": MAX_REQUESTS,
        "window_seconds": WINDOW_SECONDS,
        "remaining": max(0, MAX_REQUESTS - len(recent)),
        "is_limited": len(recent) >= MAX_REQUESTS
    }