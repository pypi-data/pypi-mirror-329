# Vellum Workflow Runner Server
This package is meant for installing on container images in order to use custom docker images when using Vellum Workflows.

## Example Dockerfile Usage:
```
FROM python:3.11.6-slim-bookworm

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    ca-certificates

RUN pip install --upgrade pip

RUN pip --no-cache-dir install vellum-workflow-server==0.13.2

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
COPY ./base-image/code_exec_entrypoint.sh .
RUN chmod +x /code_exec_entrypoint.sh

CMD ["vellum_start_server"]
```
