#!/usr/bin/env python3
import uvicorn
from uvicorn.config import LOGGING_CONFIG

def run():
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s %(levelprefix)s %(message)s"
    uvicorn.run("api:app", host="localhost", port=5000, reload=True)

if __name__ == "__main__":
    run()