# Instructions

1. Make a copy of the `env` file, name it `.env`
2. edit `.env`, make any environment configuration changes that you need

```
# Where are your models saved?
MODEL_DIR=./models

# What model do you want to use? (Relative to MODEL_DIR)
MODEL=7B/wizardLM-7B.ggmlv3.q4_1.bin

# How many layers should offload from cpu to gpu (10000 effectively offloads all layers)
GPU_LAYERS=10000

# What port should the API run on?
PORT=9000

# What version of cuda tools do you want to build & run with? (https://hub.docker.com/r/nvidia/cuda/tags) (https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html)
CUDA_VERSION=12.2.0 # minimum driver 525.60.13
#CUDA_VERSION=12.1.1 # minimum driver 525.60.13
#CUDA_VERSION=12.0.1 # minimum driver 525.60.13
#CUDA_VERSION=11.8.0 # minimum driver 450.80.02
#CUDA_VERSION=11.7.1 # minimum driver 450.80.02

# What version of llama.cpp do you want to build & run? Because llama is not semantically versioned, use the commit sha. (https://github.com/ggerganov/llama.cpp)
LLAMA_VERSION=6e7cca404748dd4b1a3affd0d1296e37f4ac0a6f

# Give your AI a personality!
PERSONALITY_NAME=HAL
PERSONALITY_DESCRIPTION="You are a AI assistant that provides factual and helpful answers to a human."
```

3. `docker compose up`