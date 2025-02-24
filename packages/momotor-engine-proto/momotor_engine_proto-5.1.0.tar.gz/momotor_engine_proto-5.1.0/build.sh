#!/usr/bin/env bash
python3 -m grpc_tools.protoc -Isrc --python_out=src --python_grpc_out=src --pyi_out=src src/momotor/rpc/proto/*.proto
