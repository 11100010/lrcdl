import os
import mutagen
from lrcdl import provider
from lrcdl.utils import get_metadata
from lrcdl.utils import extract_metadata_from_filename
from lrcdl.exceptions import (
    LyricsAlreadyExists,
    UnsupportedExtension,
    LyricsNotAvailable,
    NotEnoughMetadata
)

SUPPORTED_EXTENSIONS = [".mp3", ".flac", ".m4a"]

class Track:
    def __init__(self, path):
        self.path = path
        self.split_path = os.path.splitext(self.path)

        if not os.path.exists(self.path):
            raise FileNotFoundError()
        if not os.path.isfile(self.path):
            raise IsADirectoryError()
        if self.split_path[1].lower() not in SUPPORTED_EXTENSIONS:
            raise UnsupportedExtension()
        
        self.file = mutagen.File(self.path)

    def download_lyrics(self, options):
        metadata = get_metadata(self.file)
        filename_metadata = extract_metadata_from_filename(os.path.basename(self.path))
        
        title = options.title or metadata.get("title") or filename_metadata.get("title")
        album = options.album or metadata.get("album")
        artist = options.artist or metadata.get("artist") or filename_metadata.get("artist")
        download_path = options.download_path or self.split_path[0] + ".lrc"

        if os.path.exists(download_path):
            raise LyricsAlreadyExists()

        # Ensure at least title and artist are available
        if not title:
            raise NotEnoughMetadata(["title"])
        if not artist:
            raise NotEnoughMetadata(["artist"])

        try:
            lyrics = provider.get_lyrics(title, artist, album, round(self.file.info.length))
        except LyricsNotAvailable:
            if options.include_plain:
                raise LyricsNotAvailable()
            else:
                raise

        lyrics_text = None

        if lyrics["syncedLyrics"]:
            lyrics_text = lyrics["syncedLyrics"]
        elif lyrics["plainLyrics"] and options.include_plain:
            lyrics_text = lyrics["plainLyrics"]
        else:
            raise LyricsNotAvailable()

        with open(download_path, "w") as f:
            f.write(lyrics_text)