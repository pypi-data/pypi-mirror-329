from typing import List
from pydantic import BaseModel
import subprocess

class SubtitleStream(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    index: int
    language: str

    def __str__(self) -> str:
        return f"SubtitleStream(index={self.index}, language={self.language})"

    def __repr__(self) -> str:
        return self.__str__()

def get_subtitles(video_path: str) -> List[SubtitleStream]:
    result = subprocess.run(
        [
            "ffmpeg",
            "-i", video_path,
        ],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    output = result.stderr.decode("utf-8")

    subtitle_streams = []
    for line in output.splitlines():
        if "Stream #" in line and "Subtitle" in line:
            index = int(line.split("#")[1].split(":")[0].strip())
            language = line.split("(")[1].split(")")[0].strip()
            subtitle_streams.append(SubtitleStream(index=index, language=language))

    return subtitle_streams

def count_subtitles(video_path: str) -> int:
    subtitles = get_subtitles(video_path)
    return len(subtitles)

def has_dutch_subtitles(video_path: str) -> bool:
    subtitles = get_subtitles(video_path)
    return any(subtitle.language.lower() == "nl" for subtitle in subtitles)
