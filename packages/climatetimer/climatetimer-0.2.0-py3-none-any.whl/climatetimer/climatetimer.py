# climatetimer/climatetimer.py
import warnings
from datetime import datetime, timedelta, timezone
from math import floor
from typing import Tuple

from .constants import (
    REFERENCES,
    REFERENCE_INFO,
    SECOND_DURATION,
    MINUTE_DURATION,
    QUARTER_DURATION,
    HOUR_DURATION,
    DAY_DURATION,
    WEEK_DURATION,
)

# Supported block types and their durations (in seconds)
TIME_BLOCKS = {
    "second": SECOND_DURATION,
    "minute": MINUTE_DURATION,
    "quarter": QUARTER_DURATION,
    "hour": HOUR_DURATION,
    "day": DAY_DURATION,
    "week": WEEK_DURATION,
}


class ClimateTimer:
    """
    Computes time block IDs (blockid) and time periods (period) for various time units
    since a selected climate agreement (Paris Agreement or Kyoto Protocol).

    The reference timestamp is specified as a positional argument:
        - "paris": April 22, 2016 (UTC)
        - "kyoto": February 16, 2005 (UTC)

    Methods:
      - blockid(date, blocktype="quarter") -> int
      - period(block_id, blocktype="quarter") -> Tuple[datetime, datetime]
      - info() -> str
    """

    def __init__(self, reference: str):
        """
        Initialize ClimateTimer with a reference timestamp.

        Args:
            reference (str): Must be either "paris" or "kyoto".

        Raises:
            ValueError: If an invalid reference is provided.
        """
        if reference not in REFERENCES:
            raise ValueError(f"Invalid reference '{reference}'. Choose from {list(REFERENCES.keys())}.")
        self.reference = REFERENCES[reference]
        self.refkey = reference  # Save the key for info() lookup

    def _validate_datetime(self, dt: datetime) -> datetime:
        """
        Ensure dt is a timezone-aware datetime.

        Args:
            dt (datetime): Datetime to validate.

        Returns:
            datetime: A timezone-aware datetime.

        Raises:
            TypeError: If dt is not a datetime object.
        """
        if not isinstance(dt, datetime):
            raise TypeError(f"Expected a datetime object, got {type(dt).__name__}.")
        if dt.tzinfo is None:
            warnings.warn("Naive datetime provided; assuming UTC.", UserWarning)
            return dt.replace(tzinfo=timezone.utc)
        return dt

    def _validate_blocktype(self, blocktype: str):
        """
        Validate that blocktype is supported.

        Args:
            blocktype (str): The block type to validate.

        Raises:
            ValueError: If blocktype is not supported.
        """
        if blocktype not in TIME_BLOCKS:
            raise ValueError(f"Invalid blocktype '{blocktype}'. Choose from {list(TIME_BLOCKS.keys())}.")

    def _validate_block_id(self, block_id: int) -> int:
        """
        Validate that block_id is a positive integer.

        Args:
            block_id (int): The block ID to validate.

        Returns:
            int: The validated block ID.

        Raises:
            ValueError: If block_id is not a positive integer.
        """
        if not isinstance(block_id, int) or block_id < 1:
            raise ValueError(f"Invalid block_id {block_id}. Must be a positive integer.")
        return block_id

    def blockid(self, date: datetime, blocktype: str = "quarter") -> int:
        """
        Compute the time block ID for the given datetime and block type.

        Args:
            date (datetime): The datetime for which to compute the block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            int: The computed block ID.
        """
        self._validate_blocktype(blocktype)
        date = self._validate_datetime(date)
        delta = date - self.reference
        return floor(delta.total_seconds() / TIME_BLOCKS[blocktype]) + 1

    def period(self, block_id: int, blocktype: str = "quarter") -> Tuple[datetime, datetime]:
        """
        Get the start and end datetimes for the given block ID and block type.

        Args:
            block_id (int): The time block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            Tuple[datetime, datetime]: The start and end of the block period.
        """
        self._validate_blocktype(blocktype)
        block_id = self._validate_block_id(block_id)
        start = self.reference + timedelta(seconds=(block_id - 1) * TIME_BLOCKS[blocktype])
        return start, start + timedelta(seconds=TIME_BLOCKS[blocktype])

    def info(self) -> str:
        """
        Return a plain-text description of the instantiated time reference.

        Returns:
            str: A description of the reference event.
        """
        return REFERENCE_INFO[self.refkey]
