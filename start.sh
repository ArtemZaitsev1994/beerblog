#!/bin/bash
/wait
uvicorn app:app --host 0.0.0.0 --port 9090
