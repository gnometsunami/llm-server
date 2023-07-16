#!/bin/bash
/llama/server --port 8080 --host 0.0.0.0 -ngl "$GPU_LAYERS" -m /models/"$MODEL"