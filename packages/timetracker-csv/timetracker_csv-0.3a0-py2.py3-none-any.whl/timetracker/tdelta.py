"""Local project configuration parser for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

# from os import remove
from os.path import exists
# from os.path import basename
# from os.path import join
# from os.path import abspath
# from os.path import dirname
# from os.path import normpath
from datetime import timedelta
from datetime import datetime
from logging import debug
from csv import reader

from timetracker.utils import orange
# from timetracker.consts import DIRTRK
from timetracker.consts import FMTDT
# from timetracker.cfg.utils import get_username


class TimeDelta:
    """Manage time delta"""

    def __init__(self, tdelta):
        self.tdelta = tdelta

    def get_hours(self):
        """Get hours in floating point"""
        secs = self.tdelta.total_seconds()
        hours = secs/3600


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
