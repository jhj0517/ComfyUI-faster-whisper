from .nodes import *

NODE_CLASS_MAPPINGS = {
    "LoadFasterWhisperModel": LoadFasterWhisperModel,
    "FasterWhisperTranscription": FasterWhisperTranscription,
    "FasterWhisperToSubtitle": FasterWhisperToSubtitle,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadFasterWhisperModel": "(Down)Load FasterWhisper Model",
    "FasterWhisperTranscription": "FasterWhisper Transcription",
    "FasterWhisperToSubtitle": "FasterWhisper To Subtitle",
}

print("\n\nFaster-Whisper is loaded maybe?\n\n")