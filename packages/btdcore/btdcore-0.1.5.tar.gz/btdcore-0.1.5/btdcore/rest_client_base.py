import abc
from collections import deque
from datetime import datetime
import logging
import multiprocessing
import threading
import time
from typing import Literal, NamedTuple
import urllib.parse

import requests

LockType = Literal["multiprocessing", "thread"]


class PersistableRequestMetadata(NamedTuple):
    host: str
    duration_seconds: float
    method: str
    path: str
    kwargs: dict
    response_content: str
    response_status: int
    response_at_ts: datetime
    pass


class RequestPersister(abc.ABC):
    @abc.abstractmethod
    def persist(self, batch: list[PersistableRequestMetadata]):
        pass
    pass


class RestClientBase:
    # so in effect, not really batching at all
    REQ_PERSIST_BATCH_SIZE = 1

    def __init__(
        self,
        base: str,
        *,
        headers: dict[str, str] | None = None,
        rate_limit_window_seconds: int | None = None,
        rate_limit_requests: int | None = None,
        lock_type: LockType = "thread",
        request_persister: RequestPersister | None = None,
    ):
        self.base = base
        self.rate_limit_window_seconds = rate_limit_window_seconds
        self.rate_limit_requests = rate_limit_requests
        self._REQ_HISTORY_LOCK = (
            threading.Lock() if lock_type == "thread"
            else multiprocessing.Lock()
        )
        self._REQ_HISTORY: deque[float] = deque([])
        self.session = requests.Session()
        if headers:
            for k, v in headers.items():
                self.session.headers[k] = v
                pass
            pass
        self.request_persister = request_persister
        self.persist_q: deque[PersistableRequestMetadata] = deque([])
        return

    def _encode_query_params(self, params: dict) -> str:
        return "&".join(
            [f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in params.items()]
        )

    def _q_req_for_persistence(
            self,
            *,
            duration: float,
            method: str,
            path: str,
            kwargs: dict,
            response: requests.models.Response
    ) -> None:
        if not self.request_persister:
            return
        self.persist_q.append(PersistableRequestMetadata(
            host=self.base,
            duration_seconds=duration,
            method=method,
            path=path,
            kwargs=kwargs,
            response_at_ts=datetime.now(),
            response_content=response.text,
            response_status=response.status_code,
        ))
        if len(self.persist_q) >= self.REQ_PERSIST_BATCH_SIZE:
            self.request_persister.persist(list(self.persist_q))
            self.persist_q = deque()
            pass
        return

    def _wait_turn_for_request(self) -> None:
        if not self.rate_limit_requests or not self.rate_limit_window_seconds:
            return
        now = time.time()
        cutoff = now - self.rate_limit_window_seconds
        with self._REQ_HISTORY_LOCK:
            while self._REQ_HISTORY and self._REQ_HISTORY[0] < cutoff:
                self._REQ_HISTORY.popleft()
            if len(self._REQ_HISTORY) < self.rate_limit_requests:
                self._REQ_HISTORY.append(now)
                return
        # otherwise, too many in-flight requests
        time.sleep(self.rate_limit_window_seconds)
        self._wait_turn_for_request()
        return

    def _req(self, method: str, path: str, *, ignore_error: bool = False, **kwargs):
        url = f"{self.base}{path}"
        self._wait_turn_for_request()
        t0 = time.time()
        res = self.session.request(method, url, **kwargs)
        t1 = time.time()
        self._q_req_for_persistence(
            duration=t1-t0,
            method=method,
            path=path,
            kwargs=kwargs,
            response=res,
        )

        if not res.ok:
            logging.error("request to %s failed: %s", url, res.text)
        if not ignore_error:
            res.raise_for_status()
        return res
