#
# Copyright (c) 2025 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
import argparse
from logging import Logger
from fastapi import FastAPI
import uvicorn
import os

from .logger import service_log_config

def start_server(
    app:FastAPI,
    title: str,
    logger: Logger
):
    parser = argparse.ArgumentParser(description=title)
    parser.add_argument('--host', type=str, default=os.environ.get("HOST", "0.0.0.0"), help='Host address')
    parser.add_argument('--port', type=int, default=os.environ.get("PORT", "8090"), help='Port number')
    args = parser.parse_args()

    logger.info(f"{title} - {os.getenv('VERSION')}")
    uvicorn.run(app, host=args.host, port=args.port, log_config=service_log_config())