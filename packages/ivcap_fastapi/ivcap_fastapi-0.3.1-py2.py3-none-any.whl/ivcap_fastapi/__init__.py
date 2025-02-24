#
# Copyright (c) 2025 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
""" A client library for accessing IVCAP """

# read version from installed package
try:  # Python < 3.10 (backport)
    from importlib_metadata import version
except ImportError:
    from importlib.metadata import version
try:
    __version__ = version("ivcap_client")
except Exception:
    __version__ = "unknown" # should only happen when running the local examples

from .json_rpc import use_json_rpc_middleware
from .try_later import TryLaterException, use_try_later_middleware
from .logger import getLogger, service_log_config, logging_init
from .server import start_server