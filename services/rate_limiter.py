from fastapi import Request
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self):
        self.request_counts = defaultdict(lambda: defaultdict(int))
        self.last_reset = defaultdict(float)

    def check_rate_limit(self, request: Request) -> bool:
        client_ip = request.client.host
        current_time = time.time()

        if current_time - self.last_reset[client_ip] >= 3600:  # 1 hour window
            self.request_counts[client_ip].clear()
            self.last_reset[client_ip] = current_time

        self.request_counts[client_ip][current_time] += 1

        # Check if the number of requests in the last hour exceeds the limit
        requests_in_window = sum(count for timestamp, count in self.request_counts[client_ip].items() if current_time - timestamp < 3600)

        return requests_in_window <= 100  # Adjust this limit as needed

rate_limiter = RateLimiter()
