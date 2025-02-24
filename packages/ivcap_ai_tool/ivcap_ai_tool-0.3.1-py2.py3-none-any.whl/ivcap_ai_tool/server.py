#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
import argparse
from logging import Logger
from typing import Any, Callable
from fastapi import FastAPI
import uvicorn
import os
import sys

from ivcap_fastapi import service_log_config
from .tool_definition import print_tool_definition

def start_tool_server(
    app:FastAPI,
    title: str,
    tool_fn: Callable[..., Any],
    logger: Logger
):
    parser = argparse.ArgumentParser(description=title)
    parser.add_argument('--host', type=str, default=os.environ.get("HOST", "0.0.0.0"), help='Host address')
    parser.add_argument('--port', type=int, default=os.environ.get("PORT", "8090"), help='Port number')
    if tool_fn:
        parser.add_argument('--print-tool-description', action="store_true", help='Print tool description to stdout')
    args = parser.parse_args()

    if args.print_tool_description:
        print_tool_definition(tool_fn)
        sys.exit(0)

    logger.info(f"{title} - {os.getenv('VERSION')}")
    uvicorn.run(app, host=args.host, port=args.port, log_config=service_log_config())