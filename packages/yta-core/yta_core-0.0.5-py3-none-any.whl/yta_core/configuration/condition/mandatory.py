"""
Conditions that are mandatory according to the 
component configuration. These conditions, if
applicable, will raise an exception if not met.
"""
from yta_core.enums.field import _Field
from yta_general_utils.programming.validator.parameter import ParameterValidator
from abc import ABC, abstractmethod


class MandatoryCondition(ABC):
    """
    Class to representa a component configuration 
    mandatory condition that will raise an Exception
    if not met or will be applied if met.
    """

    @staticmethod
    @abstractmethod
    def is_satisfied(
        component: dict
    ):
        pass

class DoNeedKeywords(MandatoryCondition):
    """
    Check if the 'do_need_keywords' mandatory condition
    is satisfied or not.
    """

    _attribute: str = 'do_need_keywords'

    @staticmethod
    def is_satisfied(
        component: dict
    ) -> bool:
        """
        Check if the 'do_need_keywords' mandatory condition
        is satisfied or not.
        """
        ParameterValidator.validate_mandatory_dict('component', component)

        # TODO: Should this be different from 'is not None' (?)
        return component.get(_Field.KEYWORDS.value, None) is not None
    
class DoNeedFilenameOrUrl(MandatoryCondition):
    """
    Check if the 'do_need_filename_or_url' mandatory
    condition is satisfied or not.
    """

    _attribute: str = 'do_need_filename_or_url'

    @staticmethod
    def is_satisfied(
        component: dict
    ) -> bool:
        """
        Check if the 'do_need_filename_or_url' mandatory
        condition is satisfied or not.
        """
        ParameterValidator.validate_mandatory_dict('component', component)

        # TODO: Should this be different from 'is not None' (?)
        return (
            component.get(_Field.FILENAME.value, None) is not None or
            component.get(_Field.URL.value, None) is not None
        )
    
class DoNeedText(MandatoryCondition):
    """
    Check if the 'do_need_text' mandatory
    condition is satisfied or not.
    """

    _attribute: str = 'do_need_text'

    @staticmethod
    def is_satisfied(
        component: dict
    ) -> bool:
        """
        Check if the 'do_need_text' mandatory
        condition is satisfied or not.
        """
        ParameterValidator.validate_mandatory_dict('component', component)

        # TODO: Should this be different from 'is not None' (?)
        return component.get(_Field.TEXT.value, None) is not None
    
class DoNeedSpecificDuration(MandatoryCondition):
    """
    Check if the 'do_need_specific_duration' mandatory
    condition is satisfied or not.
    """

    _attribute: str = 'do_need_specific_duration'

    @staticmethod
    def is_satisfied(
        component: dict
    ) -> bool:
        """
        Check if the 'do_need_specific_duration' mandatory
        condition is satisfied or not.
        """
        ParameterValidator.validate_mandatory_dict('component', component)

        return (
            component.get(_Field.DURATION.value, None) is not None or
            DoNeedNarration.is_satisfied(component)
        )
    
class DoNeedNarration(MandatoryCondition):
    """
    Check if the 'do_need_narration' mandatory
    condition is satisfied or not.
    """

    _attribute: str = 'do_need_narration'

    @staticmethod
    def is_satisfied(
        component: dict
    ) -> bool:
        """
        Check if the 'do_need_narration' mandatory
        condition is satisfied or not.
        """
        ParameterValidator.validate_mandatory_dict('component', component)

        return (
            component.get(_Field.AUDIO_NARRATION_FILENAME, None) is not None or
            (
                component.get(_Field.VOICE, None) is not None and
                component.get(_Field.TEXT_TO_NARRATE, None) is not None
            )
        )