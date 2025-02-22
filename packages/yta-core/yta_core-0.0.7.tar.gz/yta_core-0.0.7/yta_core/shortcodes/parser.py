"""
Module to include the shortcode parser instances
we need in our app.
"""
from yta_shortcodes.parser import ShortcodeParser
from yta_core.shortcodes.tag import YTAShortcodeTag
from yta_shortcodes.tag_type import ShortcodeTagType


shortcode_parser = ShortcodeParser([
    YTAShortcodeTag('meme', ShortcodeTagType.SIMPLE)
])
"""
Shortcode parser that includes all the
shortcode tags we accept in our system
and must be applied in those text that
are allowed to use the parser.
"""
empty_shortcode_parser = ShortcodeParser([])
"""
An empty shortcode parser that allows
us to discard a text if it contains
any kind of shortcode.
"""