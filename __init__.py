from .nodes import *

NODE_CLASS_MAPPINGS = {
    "LoadFasterWhisperModel": LoadFasterWhisperModel,
    "FasterWhisperTranscription": FasterWhisperTranscription,
    "FasterWhisperToSubtitle": FasterWhisperToSubtitle,
    "SaveSubtitle": SaveSubtitle,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadFasterWhisperModel": "(Down)Load FasterWhisper Model",
    "FasterWhisperTranscription": "FasterWhisper Transcription",
    "FasterWhisperToSubtitle": "FasterWhisper To Subtitle",
    "SaveSubtitle": "Save Subtitle",
}