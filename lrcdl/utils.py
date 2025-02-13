import os
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

metadata_mapping = {
    MP3: {
        "title": "TIT2",
        "album": "TALB",
        "artist": "TPE1"
    },
    FLAC: {
        "title": "title",
        "album": "album",
        "artist": "artist"
    },
    MP4: {
        "title": "©nam",
        "album": "©alb",
        "artist": "©ART"
    }
}


def extract_metadata_from_filename(filename):
    """
    Extract artist and title from a filename in the format "Artist - Title.ext".
    The title ends prematurely by the first occurrence of "(".
    """
    name, _ = os.path.splitext(filename)
    parts = name.split(" - ")

    if len(parts) == 2:
        artist = parts[0]
        title = parts[1].split("(")[0].strip()  # Cut off the title at the first "("
        return {"artist": artist, "title": title}

    return {}