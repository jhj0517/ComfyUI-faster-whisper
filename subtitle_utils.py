from typing import List, Union

AVAILABLE_SUBTITLE_FORMAT = ['.srt', '.vtt']


def format_transcriptions_to_subtitle(
    transcriptions: List,
    output_format: str
):
    if output_format not in AVAILABLE_SUBTITLE_FORMAT:
        raise ValueError(f"Output format not supported. Supported formats: {AVAILABLE_SUBTITLE_FORMAT}")
    subtitle = ""

    if output_format == '.srt':
        initial_text = ""

    elif output_format == '.vtt':
        initial_text = "WEBVTT\n\n"

    subtitle += initial_text
    for i, transcription in enumerate(transcriptions):
        formatted_start_time = format_to_subtitle_time(transcription['start'], output_format)
        formatted_end_time = format_to_subtitle_time(transcription['end'], output_format)
        text = transcription['text'].strip()

        subtitle += f"{i + 1}\n"
        subtitle += f"{formatted_start_time} --> {formatted_end_time}\n"
        subtitle += f"{text}\n\n"

    return subtitle


def parse_timestamp(timestamp: Union[float, int]):
    hours = timestamp // 3600
    minutes = (timestamp - hours * 3600) // 60
    seconds = timestamp - hours * 3600 - minutes * 60
    milliseconds = (timestamp - int(timestamp)) * 1000
    return hours, minutes, seconds, milliseconds


def format_to_subtitle_time(timestamp: Union[float, int],
                            output_format: str):
    hours, minutes, seconds, milliseconds = parse_timestamp(timestamp)
    if output_format == ".srt":
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{int(milliseconds):03d}"
    elif output_format == ".vtt":
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{int(milliseconds):03d}"
    else:
        raise ValueError(f"Output format not supported. Supported formats: {AVAILABLE_SUBTITLE_FORMAT}")
