import os
import faster_whisper
from typing import Union, BinaryIO, Dict, List, Tuple
import numpy as np

import folder_paths
from comfy.utils import ProgressBar

from .utils.subtitle_utils import AVAILABLE_SUBTITLE_FORMAT, format_transcriptions_to_subtitle, get_incremented_filename

faster_whisper_script_dir_path = os.path.dirname(os.path.abspath(__file__))
faster_whisper_model_dir = os.path.join(folder_paths.models_dir, "faster-whisper")
faster_whisper_output_dir_path = folder_paths.get_output_directory()

FLOAT_NONE_VALUE = -999.0
INT_NONE_VALUE = -999


class LoadFasterWhisperModel:
    @classmethod
    def INPUT_TYPES(s):
        faster_whisper_models = [
            "tiny.en",
            "tiny",
            "base.en",
            "base",
            "small.en",
            "small",
            "medium.en",
            "medium",
            "large-v1",
            "large-v2",
            "large-v3",
            "large"
        ]

        return {
            "required": {
                "model": (faster_whisper_models,),
                "device": (['cuda', 'cpu', 'auto'],),
            },
        }

    RETURN_TYPES = ("FASTERWHISPERMODEL",)
    RETURN_NAMES = ("faster_whisper_model",)
    FUNCTION = "load_model"
    CATEGORY = "FASTERWHISPER"

    def load_model(self,
                   model: str,
                   device: str,
                   ) -> Tuple[faster_whisper.WhisperModel]:
        os.makedirs(faster_whisper_model_dir, exist_ok=True)

        faster_whisper_model = faster_whisper.WhisperModel(
            device=device,
            model_size_or_path=model,
            download_root=faster_whisper_model_dir,
        )

        return (faster_whisper_model, )


class FasterWhisperTranscription:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio": ("FILEPATH", ),
                "model": ("FASTERWHISPERMODEL", ),
            },
            "optional": {
                "language": ("STRING", {"default": "auto"}),
                "task": (["transcribe", "translate"], ),
                "beam_size": ("INT", {"default": 5}),
                "log_prob_threshold": ("FLOAT", {"default": -1.0}),
                "no_speech_threshold": ("FLOAT", {"default": 0.6}),
                "best_of": ("INT", {"default": 5}),
                "patience": ("FLOAT", {"default": 1}),
                "temperature": ("FLOAT", {"default": 0.0}),
                "compression_ratio_threshold": ("FLOAT", {"default": 2.4}),
                "length_penalty": ("FLOAT", {"default": 1.0}),
                "repetition_penalty": ("FLOAT", {"default": 1.0}),
                "no_repeat_ngram_size": ("INT", {"default": 0}),
                "prefix": ("STRING", {"default": ""}),
                "suppress_blank": ("BOOLEAN", {"default": True}),
                "suppress_tokens": ("STRING", {"default": "[-1]"}),
                "max_initial_timestamp": ("FLOAT", {"default": 1.0}),
                "word_timestamps": ("BOOLEAN", {"default": False}),
                "prepend_punctuations": ("STRING", {"default": "\"'“¿([{-"}),
                "append_punctuations": ("STRING", {"default": "\"'.。,，!！?？:：”)]}、"}),
                "max_new_tokens": ("INT", {"default": INT_NONE_VALUE}),
                "chunk_length": ("INT", {"default": INT_NONE_VALUE}),
                "hallucination_silence_threshold": ("FLOAT", {"default": FLOAT_NONE_VALUE}),
                "hotwords": ("STRING", {"default": ""}),
                "language_detection_threshold": ("FLOAT", {"default": FLOAT_NONE_VALUE}),
                "language_detection_segments": ("INT", {"default": 1}),
                "prompt_reset_on_temperature": ("FLOAT", {"default": 0.5}),
                "condition_on_previous_text": ("BOOLEAN", {"default": True}),
                "initial_prompt": ("STRING", {"default": ""}),
                "without_timestamps": ("BOOLEAN", {"default": False}),
                "vad_filter": ("BOOLEAN", {"default": False}),
                "vad_parameters": ("STRING", {"default": ""}),
                "clip_timestamps": ("STRING", {"default": "0"}),
            }
        }

    RETURN_TYPES = ("TRANSCRIPTIONS",)
    RETURN_NAMES = ("transcriptions",)
    FUNCTION = "transcribe"
    CATEGORY = "FASTERWHISPER"

    def transcribe(self,
                   audio: Union[str, BinaryIO, np.ndarray, Dict],
                   model: faster_whisper.WhisperModel,
                   **params,
                   ) -> Tuple[List]:
        params = self.collect_params(params)

        segments, info = model.transcribe(
            audio=audio,
            **params,
        )

        comfy_pbar = ProgressBar(info.duration)

        transcriptions = []
        for segment in segments:
            comfy_pbar.update_absolute(segment.end)
            transcriptions.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text
            })
        return (transcriptions, )

    @staticmethod
    def preprocess_audio(audio):
        audio, sr = audio["waveform"], audio["sample_rate"]
        audio = audio.detach().cpu().numpy()
        return audio

    @staticmethod
    def collect_params(params):
        # Set None values manually because None seems not allowed as default in ComfyUI
        if "language" in params and params["language"] == "auto":
            params["language"] = None
        if "suppress_tokens" in params:
            params["suppress_tokens"] = eval(params["suppress_tokens"])
        if "prefix" in params and not params["prefix"]:
            params["prefix"] = None
        if "hotwords" in params and not params["hotwords"]:
            params["hotwords"] = None
        if "initial_prompt" in params and not params["initial_prompt"]:
            params["initial_prompt"] = None
        if "vad_parameters" in params and not params["vad_parameters"]:
            params["vad_parameters"] = None
        if "max_new_tokens" in params and params["max_new_tokens"] == INT_NONE_VALUE:
            params["max_new_tokens"] = None
        if "chunk_length" in params and params["chunk_length"] == INT_NONE_VALUE:
            params["chunk_length"] = None
        if "hallucination_silence_threshold" in params and params["hallucination_silence_threshold"] == FLOAT_NONE_VALUE:
            params["hallucination_silence_threshold"] = None
        if "language_detection_threshold" in params and params["language_detection_threshold"] == FLOAT_NONE_VALUE:
            params["language_detection_threshold"] = None

        return params


class FasterWhisperToSubtitle:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "transcriptions": ("TRANSCRIPTIONS",),
                "subtitle_format": (AVAILABLE_SUBTITLE_FORMAT,),
            },
        }

    RETURN_TYPES = ("SUBTITLE",)
    RETURN_NAMES = ("subtitle text",)
    FUNCTION = "format_to_subtitle"
    CATEGORY = "FASTERWHISPER"

    def format_to_subtitle(self,
                           transcriptions: List[Dict],
                           subtitle_format: str,
                           ) -> Tuple[List]:
        subtitle = format_transcriptions_to_subtitle(transcriptions, subtitle_format)
        subtitle = [subtitle, subtitle_format]
        return (subtitle,)


class SaveSubtitle:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "subtitle": ("SUBTITLE", )
            },
            "optional": {
                "prefix": ("STRING", {"default": "subtitle"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_path",)
    FUNCTION = "save_subtitle"
    CATEGORY = "FASTERWHISPER"
    OUTPUT_NODE = True

    def save_subtitle(self,
                      subtitle: List,
                      prefix: str
                      ) -> Tuple[str]:
        subtitle, subtitle_format = subtitle
        if subtitle_format not in AVAILABLE_SUBTITLE_FORMAT:
            raise ValueError(f"Output format not supported. Supported formats: {AVAILABLE_SUBTITLE_FORMAT}")

        output_path = get_incremented_filename(faster_whisper_output_dir_path, prefix, subtitle_format)

        with open(output_path, "w") as f:
            f.write(subtitle)
        return (output_path,)


class InputFilePath:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "filepath": ("STRING", {"default": "", "multiline": False})
            }
        }

    RETURN_TYPES = ("FILEPATH", )
    RETURN_NAMES = ("filepath",)
    FUNCTION = "process_filepath"
    CATEGORY = "FASTERWHISPER"

    def process_filepath(self, filepath):
        if not os.path.exists(filepath):
            raise ValueError(f"File not found: {filepath}")

        return (filepath,)
