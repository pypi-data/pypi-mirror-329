"""
Conditions that are optional according to the 
component configuration. These conditions, if
applicable, will be applied, but nothing will
change if they are not applicable.
"""
from yta_core.configuration.condition.mandatory import DoNeedNarration, DoNeedText, DoNeedFilenameOrUrl, DoNeedKeywords
from abc import ABC, abstractmethod


class OptionalCondition(ABC):
    """
    Class to represent a component configuration optional
    condition that will be only applied if met.
    """

    @staticmethod
    @abstractmethod
    def is_satisfied(
        configuration: 'Configuration',
        component: dict
    ):
        pass

class DoShouldBuildNarration(OptionalCondition):
    """
    Check if the configuration says that the component
    needs or can have a specific duration field and
    the provided 'component' has the fields to generate
    a voice narration so it can be done.
    """

    @staticmethod
    def is_satisfied(
        configuration: 'Configuration',
        component: dict
    ) -> bool:
        """
        Check if the configuration says that the component
        needs or can have a specific duration field and
        the provided 'component' has the fields to generate
        a voice narration so it can be done.
        """
        return (
            (
                configuration.can_have_specific_duration or
                configuration.do_need_specific_duration
            ) and
            DoNeedNarration.is_satisfied(component)
        )
    
class DoShouldBuildSpecificDuration(OptionalCondition):
    """
    Check if the configuration says that the component
    needs or can have a specific duration field and
    the provided 'component' actually need that field
    to be set.
    """

    @staticmethod
    def is_satisfied(
        configuration: 'Configuration',
        component: dict
    ) -> bool:
        """
        Check if the configuration says that the component
        needs or can have a specific duration field and
        the provided 'component' actually need that field
        to be set.
        """
        return (
            (
                configuration.can_have_specific_duration or
                configuration.do_need_specific_duration
            ) and
            DoNeedNarration.is_satisfied(component)
        )
    
class DoShouldBuildText(OptionalCondition):
    """
    Check if the configuration says that the component
    needs or can have the 'text' field set and the
    provided 'component' actually has it.
    """

    @staticmethod
    def is_satisfied(
        configuration: 'Configuration',
        component: dict
    ) -> bool:
        """
        Check if the configuration says that the component
        needs or can have the 'text' field set and the
        provided 'component' actually has it.
        """
        return (
            (
                configuration.can_have_text or
                configuration.do_need_text
            ) and
            DoNeedText.is_satisfied(component)
        )
    
class DoShouldBuildFilenameOrUrl(OptionalCondition):
    """
    Check if the configuration allows having 'filename' or
    'url' fields set and the provided 'component' actually
    has those fields set.
    """

    @staticmethod
    def is_satisfied(
        configuration: 'Configuration',
        component: dict
    ) -> bool:
        """
        Check if the configuration allows having 'filename' or
        'url' fields set and the provided 'component' actually
        has those fields set.
        """
        return (
            (
                configuration.can_have_url or
                configuration.can_have_filename or
                configuration.do_need_filename_or_url
            ) and
            DoNeedFilenameOrUrl.is_satisfied(component)
        )

class DoShouldBuildKeywords(OptionalCondition):
    """
    Check if the configuration says that the components
    needs or can have 'keywords' and it actually has that
    field set.
    """

    @staticmethod
    def is_satisfied(
        configuration: 'Configuration',
        component: dict
    ) -> bool:
        """
        Check if the configuration says that the components
        needs or can have 'keywords' and it actually has that
        field set.
        """
        return (
            (
                configuration.can_have_keywords or
                configuration.do_need_keywords
            ) and
            DoNeedKeywords.is_satisfied(component)
        )
