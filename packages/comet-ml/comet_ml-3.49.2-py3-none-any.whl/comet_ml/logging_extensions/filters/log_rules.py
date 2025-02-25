# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2024 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
import logging
from abc import ABC, abstractmethod
from typing import Optional

from ...rate_limiter.exceptions import LimitRateExceededError
from ...rate_limiter.limiter import OpRateLimiter


class LogRecordRule(ABC):

    @abstractmethod
    def apply(
        self, record: logging.LogRecord, record_type: str
    ) -> Optional[logging.LogRecord]:
        """Allies this rule to the provided LogRecord and returns modified original LogRecord
        or new one.
        If provided LogRecord should be blocked from logging then None returned."""
        pass


class RateLimitedLogRecordRule(LogRecordRule):
    """The rule to limit log records to be issued with specific rate"""

    def __init__(self, rate_limiter: OpRateLimiter, drop_excess_records: bool = False):
        self._rate_limiter = rate_limiter
        self._drop_excess_records = drop_excess_records

    def apply(
        self, record: logging.LogRecord, record_type: str
    ) -> Optional[logging.LogRecord]:
        try:
            self._rate_limiter.try_acquire(record_type)
            return record
        except LimitRateExceededError:
            if self._drop_excess_records:
                return None
            else:
                record.levelno = logging.DEBUG
                record.levelname = logging.getLevelName(logging.DEBUG)
                return record
