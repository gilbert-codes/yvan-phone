# gunicorn.conf.py
import os

# Bind to port 10000 (Render default)
bind = "0.0.0.0:10000"

# Worker settings
workers = 1
threads = 2
worker_class = "sync"
worker_tmp_dir = "/dev/shm"

# Timeouts
timeout = 120
graceful_timeout = 30
keepalive = 2

# Limit request size to avoid HTTP/2 issues
limit_request_line = 8190
limit_request_fields = 100
limit_request_field_size = 8190

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Preload app to save memory
preload_app = True