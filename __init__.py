from .nodes import *


NODE_CLASS_MAPPINGS = {
    "LoadFasterWhisperModel": LoadFasterWhisperModel,
    "FasterWhisperTranscription": FasterWhisperTranscription,
    "FasterWhisperToSubtitle": FasterWhisperToSubtitle,
    "SaveSubtitle": SaveSubtitle,
    "InputFilePath": InputFilePath,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadFasterWhisperModel": "(Down)Load FasterWhisper Model",
    "FasterWhisperTranscription": "FasterWhisper Transcription",
    "FasterWhisperToSubtitle": "FasterWhisper To Subtitle",
    "InputFilePath": "Input FilePath",
}


import os
# Temporal fix of the bug : https://github.com/jhj0517/Whisper-WebUI/issues/144
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'