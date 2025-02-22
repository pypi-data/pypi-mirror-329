from yta_audio.voice.transcription.objects import AudioTranscription as BaseAudioTranscription, AudioTranscriptionWord as BaseAudioTranscriptionWord, AudioTranscriptionWordTimestamp as BaseAudioTranscriptionWordTimestamp
from yta_general_utils.programming.validator.parameter import ParameterValidator

import json


class AudioTranscriptionWord(BaseAudioTranscriptionWord):
    """
    Wrapper to include MongoDB serialization.
    """

    @staticmethod
    def from_mongo(
        object: dict
    ) -> 'BaseAudioTranscriptionWord':
        """
        Get an object from MongoDB and rebuild it
        as a python instance.
        """
        ParameterValidator.validate_mandatory_dict('object', object)
        ParameterValidator.validate_dict_has_keys('object', object, ['word', 'start', 'end', 'confidence'])
        
        return BaseAudioTranscriptionWord(
            object.word,
            BaseAudioTranscriptionWordTimestamp(
                object.start,
                object.end
            ),
            object.confidence
        )
    
    @property
    def for_mongo(
        self
    ) -> str:
        """
        Serialization to be stored in MongoDB.
        """
        return self.as_json
    
class AudioTranscription(BaseAudioTranscription):
    """
    Wrapper to include MongoDB serialization.
    """

    @staticmethod
    def from_mongo(
        object: list[dict]
    ) -> 'AudioTranscriptionWord':
        """
        Get an object from MongoDB and rebuild it
        as a python instance.

        The 'object' must be an array of words.
        """
        ParameterValidator.validate_mandatory_list_of_these_instances('object', object, dict)

        return AudioTranscription([
            AudioTranscriptionWord.from_mongo(item)
            for item in object
        ])
    
    @property
    def for_mongo(
        self
    ) -> str:
        """
        Serialization to be stored in MongoDB.
        """
        return json.dumps(self.as_dict['words'])
        