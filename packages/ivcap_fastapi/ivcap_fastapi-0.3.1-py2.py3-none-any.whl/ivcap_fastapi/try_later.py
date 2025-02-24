#
# Copyright (c) 2025 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
from fastapi import Response, Request

class TryLaterException(Exception):
    """An exception to raise if a computation will take longer and the result
    should be collected later at a different method."""
    def __init__(self, location, wait_time):
        super().__init__(location)
        self.location = location
        self.wait_time = wait_time

    def response(self):
        r = Response(status_code=204)  # No Content
        r.headers["Location"] = self.location
        r.headers["Retry-Later"] = f"{self.wait_time}"
        return r

async def _try_later(request: Request, call_next) -> Response:
    try:
        return await call_next(request)
    except TryLaterException as e:
        return e.response()

def use_try_later_middleware(app):
    app.middleware("http")(_try_later)