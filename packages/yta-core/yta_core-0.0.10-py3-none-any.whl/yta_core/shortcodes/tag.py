from yta_core.shortcodes import Shortcode
from yta_shortcodes.tag import ShortcodeTag


class YTAShortcodeTag(ShortcodeTag):
    """
    Custom Shortcode tag for Youtube Autonomous
    that uses the also custom shortcode.
    """

    def handler(
        self,
        shortcodes,
        pargs,
        kwargs,
        context,
        **extra_args
    ):
        """
        The function that handles the shortcode, fills the provided
        'shortcodes' list with a new shortcode object and all the
        required attributes and values.

        :param shortcodes: A list with the shortcodes that have been
        found previously, so we are able to store the new one.
        :param pargs: The positional arguments found in the shortcode
        tag.
        :param kwargs: The key and value arguments found in the
        shortcode tag.
        :param context: The context (I don't know what this is for...)
        :param **extra_args: Extra arguments we want to pass to this
        function.
        """
        # Fill the attributes
        attributes = {}

        for parg in pargs:
            attributes[parg] = None

        if kwargs:
            for kwarg in kwargs:
                attributes[kwarg] = kwargs[kwarg]

        # We handle the 'content' like this to avoid
        # being an strict parameter
        content = extra_args.get('content', None)

        # Here you can customize it a little bit
        # before storing the final Shortcode entity
        self.custom_handler(shortcodes, attributes, context, content)

        shortcodes.append(Shortcode(
            tag = self.name,
            type = self._type,
            context = context,
            content = content,
            attributes = attributes
        ))

        """
        We will remove all the attributes but keep 
        the shortcode tags and the content (if
        existing) to be able to detect it again in
        the text so we can extract the position for
        extra purposes
        """
        return (
            f'[{self.name}]'
            if self.is_simple_scoped else
            f'[{self.name}]{content}[/{self.name}]'
        )