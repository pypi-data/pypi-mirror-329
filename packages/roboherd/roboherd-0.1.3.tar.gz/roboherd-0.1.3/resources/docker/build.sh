#!/usr/bin/env bash

set -eux

uv build --wheel
mv dist/* resources/docker/
rm -rf dist

cd resources/docker

docker buildx build --push -t helgekr/roboherd .
