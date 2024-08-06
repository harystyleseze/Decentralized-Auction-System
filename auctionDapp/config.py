import os

class Config:
    ROLLUP_HTTP_SERVER_URL = os.environ.get("ROLLUP_HTTP_SERVER_URL", "http://localhost:5000")
