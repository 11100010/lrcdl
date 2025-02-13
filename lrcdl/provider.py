from importlib.metadata import version
import requests
from lrcdl.exceptions import TrackNotFound, RequestFailed

DEFAULT_HOST = "https://lrclib.net"
DEFAULT_HEADERS = {
    "User-Agent": f"lrcdl v{version('lrcdl')} (https://github.com/viown/lrcdl)"
}

def get_lyrics(track_name, artist_name, album_name, duration):
    params = {
        "track_name": track_name.strip() if track_name else None,
        "artist_name": artist_name.strip() if artist_name else None,
        "album_name": album_name.strip() if album_name else None,
        "duration": duration
    }
    
    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}

    r = requests.get(f"{DEFAULT_HOST}/api/get", params=params, headers=DEFAULT_HEADERS)

    if r.ok:
        return r.json()
    elif r.status_code == 404:
        raise TrackNotFound()
    else:
        raise RequestFailed(r.text)