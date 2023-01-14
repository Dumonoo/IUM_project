#!/usr/bin/env python3
import uvicorn

if __name__ == "__main__":
    uvicorn.run("api:app", host="localhost", port=5000, reload=True)