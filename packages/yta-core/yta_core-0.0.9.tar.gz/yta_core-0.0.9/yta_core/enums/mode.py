from yta_general_utils.programming.enum import YTAEnum as Enum


class _Mode(Enum):
    """
    The mode in which the content has to be
    displayed when built.
    """

    INLINE = 'inline'
    """
    The content will be displayed in this 'inline'
    mode when it will interrupt the main video to
    be played and then the main video will continue.
    This mode modifies the clip duration so we need
    to recalculate the other objects start times.
    """
    OVERLAY = 'overlay'
    """
    The content will be displayed in this 'overlay'
    mode when it will be shown in the foreground of
    the main clip but changing not its duration. We
    don't need to recalculate any other duration.
    """
    REPLACE = 'replace'
    """
    The content will be displayed in this 'replace'
    mode when the original video is replaced by this
    content in the specific part in which it has to
    be displayed. This means that the original video
    part will be replaced by this part, but the 
    duration will remain the same as it is a 
    replacement of just a part of its content.
    """

class SegmentMode(Enum):
    """
    The modes in which a Segment can be built
    and displayed.
    """
    pass

class EnhancementMode(Enum):
    """
    The modes in which an Enhancement can be
    built and displayed.
    """

    INLINE = _Mode.INLINE.value
    """
    The content will be displayed in this 'inline'
    mode when it will interrupt the main video to
    be played and then the main video will continue.
    This mode modifies the clip duration so we need
    to recalculate the other objects start times.
    """
    OVERLAY = _Mode.OVERLAY.value
    """
    The content will be displayed in this 'overlay'
    mode when it will be shown in the foreground of
    the main clip but changing not its duration. We
    don't need to recalculate any other duration.
    """
    REPLACE = _Mode.REPLACE.value
    """
    The content will be displayed in this 'replace'
    mode when the original video is replaced by this
    content in the specific part in which it has to
    be displayed. This means that the original video
    part will be replaced by this part, but the 
    duration will remain the same as it is a 
    replacement of just a part of its content.
    """

    @classmethod
    def get_default(cls):
        """
        Returns the default enum of this list. This value will be used when
        no valid value is found.
        """
        return cls.INLINE
    
class ShortcodeMode(Enum):
    """
    The modes in which a Shortcode can be
    built and displayed.
    """

    INLINE = _Mode.INLINE.value
    """
    The content will be displayed in this 'inline'
    mode when it will interrupt the main video to
    be played and then the main video will continue.
    This mode modifies the clip duration so we need
    to recalculate the other objects start times.
    """
    OVERLAY = _Mode.OVERLAY.value
    """
    The content will be displayed in this 'overlay'
    mode when it will be shown in the foreground of
    the main clip but changing not its duration. We
    don't need to recalculate any other duration.
    """
    REPLACE = _Mode.REPLACE.value
    """
    The content will be displayed in this 'replace'
    mode when the original video is replaced by this
    content in the specific part in which it has to
    be displayed. This means that the original video
    part will be replaced by this part, but the 
    duration will remain the same as it is a 
    replacement of just a part of its content.
    """

    @classmethod
    def get_default(cls):
        """
        Returns the default enum of this list. This value will be used when
        no valid value is found.
        """
        return cls.INLINE