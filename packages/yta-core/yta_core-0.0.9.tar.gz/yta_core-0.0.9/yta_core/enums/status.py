from yta_general_utils.programming.enum import YTAEnum as Enum


class _Status(Enum):
    """
    Enum class to represent the different
    statuses an item can have.

    For internal use only. Use a more specific
    Enum class to interact with the different
    statuses.
    """

    TO_START = 'to_start'
    """
    It has not started yet.
    """
    IN_PROGRESS = 'in_progress'
    """
    It has not been built completely yet but it
    is being built.
    """
    FINISHED = 'finished'
    """
    It has been built and applied completely.
    """

class ProjectStatus(Enum):
    """
    Enum class to represent the different
    statuses that a project can have.
    """

    TO_START = _Status.TO_START.value
    """
    It has not started yet.
    """
    IN_PROGRESS = _Status.IN_PROGRESS.value
    """
    It has not been built completely yet but it
    is being built.
    """
    FINISHED = _Status.FINISHED.value
    """
    It has been built and applied completely.
    """

class SegmentStatus(Enum):
    """
    The current segment status defined by this string.
    """

    TO_START = _Status.TO_START.value
    """
    It has not started yet.
    """
    IN_PROGRESS = _Status.IN_PROGRESS.value
    """
    It has not been built completely yet but it
    is being built.
    """
    FINISHED = _Status.FINISHED.value
    """
    It has been built and applied completely.
    """

class EnhancementStatus(Enum):
    """
    The current enhancement status defined by this string.
    """

    TO_START = _Status.TO_START.value
    """
    It has not started yet.
    """
    IN_PROGRESS = _Status.IN_PROGRESS.value
    """
    It has not been built completely yet but it
    is being built.
    """
    FINISHED = _Status.FINISHED.value
    """
    It has been built and applied completely.
    """