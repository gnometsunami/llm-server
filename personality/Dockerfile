# Build env
FROM debian:11-slim AS build-env
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip setuptools wheel

# Build venv
FROM build-env AS build-venv
COPY ./requirements.txt /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

# Run app using distroless
FROM gcr.io/distroless/python3-debian11:nonroot
WORKDIR /app
COPY --from=build-venv /venv /venv
COPY ./src .
USER nonroot:nonroot
EXPOSE 9000
ENTRYPOINT ["/venv/bin/python", "app.py"]
