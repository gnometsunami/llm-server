ARG CUDA_VERSION=12.2.0
ARG LLAMA_VERSION=6e7cca404748dd4b1a3affd0d1296e37f4ac0a6f
FROM nvidia/cuda:${CUDA_VERSION}-devel-ubuntu22.04 as build

RUN apt-get update && apt-get install --no-install-recommends -y git build-essential cmake

WORKDIR /source
RUN git clone -n https://github.com/ggerganov/llama.cpp . && \
     git checkout ${LLAMA_VERSION}

RUN mkdir build && cd build && cmake -DLLAMA_BUILD_SERVER=ON .. -DLLAMA_CUBLAS=ON && cmake --build . --config Release

FROM nvidia/cuda:${CUDA_VERSION}-runtime-ubuntu22.04

WORKDIR /llama
COPY --from=build /source/build/bin .
COPY start.sh .

RUN groupadd --gid 10001 non-root \
    && useradd --uid 10001 --gid 10001 -m non-root \
    && chmod 755 start.sh

USER non-root
EXPOSE 8080
