import time

def log_event(message):
    """Log an event with a timestamp."""
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")