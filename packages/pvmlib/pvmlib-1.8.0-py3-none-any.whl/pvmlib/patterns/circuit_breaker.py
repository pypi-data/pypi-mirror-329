from pybreaker import CircuitBreaker, CircuitMemoryStorage
import os

fail_max = int(os.getenv("CIRCUIT_BREAKER_FAIL_MAX", 5))
reset_timeout = int(os.getenv("CIRCUIT_BREAKER_RESET_TIMEOUT", 60))

memory_storage = CircuitMemoryStorage(state="half-open")

circuit_breaker = CircuitBreaker(
    fail_max=fail_max,
    reset_timeout=reset_timeout,
    state_storage=memory_storage
)