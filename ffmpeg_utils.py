import os
import re

def get_ffmpeg_path():
    # ffmpeg.exe ile aynı klasörde çalışacak şekilde ayarlandı
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffmpeg.exe")

video_exts = (".mkv", ".mp4", ".avi")
audio_exts = (".aac", ".ac3", ".eac3", ".mp3", ".wav", ".m4a", ".dts")
subtitle_exts = (".srt", ".ass", ".sub")

def generate_clean_movie_name(original_name, mode):
    name_upper = original_name.upper()
    is_series = re.search(r"S\d{2}E\d{2}", name_upper)
    components = []

    if is_series:
        series_match = re.search(r"(.+?)(S\d{2}E\d{2})", name_upper)
        if series_match:
            clean_name = re.sub(
                r"\.(BLU-?RAY|X\d+|HEVC|H264|RARBG|WEB-DL|AMZN|NF|AAC5\.1|DDP5\.1|DD5\.1|TRUEHD|ATMOS|10BIT|\\b\\w{2,}-\\w+\\b)",
                "", series_match.group(1), flags=re.IGNORECASE)
            components.append(clean_name.strip(".").replace("..", "."))
            components.append(series_match.group(2))
    else:
        name_no_ext = os.path.splitext(name_upper)[0]
        year_match = re.search(r"(19|20)\d{2}", name_no_ext)
        quality_match = re.search(r"(2160P|1080P|720P|480P|4K)", name_no_ext)
        name_until_year = name_no_ext
        if year_match:
            name_until_year = name_no_ext.split(year_match.group(0))[0]
        final_name = name_until_year
        if year_match:
            final_name += year_match.group(0)
        if quality_match:
            final_name += "." + quality_match.group(1)
        final_name = re.sub(r"\.(BLU-?RAY|WEB[-\.]DL|HDR|10BIT|X265|HEVC|H264|AAC|DDP5\.1|TRUEHD|ATMOS|PSA|\\b\\w{2,}-\\w+\\b)", "", final_name, flags=re.IGNORECASE)
        final_name = re.sub(r"\.+", ".", final_name.strip("."))
        components.append(final_name)
    suffix = "-DUAL" if mode == "dual" else ".TRDUBLAJ"
    components.append(suffix)
    ext = os.path.splitext(original_name)[1]
    return f"{'.'.join(components)}{ext}"
