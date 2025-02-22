# SoundCloud Downloader

`soundcloud_downloader` is a Python library that simplifies downloading music from SoundCloud using the `scdl` tool. It provides a programmatic interface to download tracks, playlists, user likes, reposts, and search for tracks without relying solely on the `scdl` command-line interface.

## Features

- Download individual tracks, playlists, all tracks, likes, or reposts from SoundCloud.
- Search for tracks by query and optionally download the results.
- Retrieve track URLs without downloading using the search-only feature.
- Customizable options like output directory, file name format, and authentication.
- Compatible with Python 3.6+ (tested up to Python 3.12).

## Installation

### Prerequisites

- Python 3.6 or higher.
- `scdl` package (installed automatically as a dependency).
- Optional: A SoundCloud authentication token for private tracks or extended functionality.

### Install Locally

1. Clone or download the repository:
   ```bash
   git clone https://github.com/ATHStudioo/soundcloud_downloader.git
   cd soundcloud_downloader
   ```
2. Install in editable mode:
   ```bash
   pip install -e .
   ```
   This links the local source code to your Python environment, allowing changes to take effect without reinstallation.

## Usage

### Basic Examples

#### Initialize the Downloader
```python
from soundcloud_downloader import SoundCloudDownloader

downloader = SoundCloudDownloader(
    output_dir="C:/Music",           # Directory to save files
    auth_token="your_auth_token"     # Optional: for private tracks
)
```

#### Download a Track
```python
track_url = "https://soundcloud.com/sadsvit/molodist"
result = downloader.download_track(track_url, overwrite=True)
print("Download result:", result)
```

#### Download a Playlist
```python
playlist_url = "https://soundcloud.com/pandadub/sets/the-lost-ship"
result = downloader.download_playlist(playlist_url, max_tracks=5)
print(result)
```

#### Search for Tracks
```python
urls = downloader.search("lofi beats", limit=2)
print("Found URLs:", urls)
```

#### Search and Download Tracks
```python
result = downloader.search_and_download("chill beats", limit=3)
print("Search and download result:", result)
```

### Advanced Examples

#### Download User Likes
```python
user_url = "https://soundcloud.com/kobiblastoyz"
result = downloader.download_likes(user_url, max_tracks=10, offset=2)
print(result)
```

#### Download All Tracks by a User
```python
user_url = "https://soundcloud.com/kobiblastoyz"
result = downloader.download_all_tracks(user_url, max_tracks=5)
print(result)
```

#### Download User Reposts
```python
user_url = "https://soundcloud.com/kobiblastoyz"
result = downloader.download_reposts(user_url, max_tracks=3)
print(result)
```

#### Custom File Naming
```python
downloader = SoundCloudDownloader(
    output_dir="C:/Music",
    name_format="{user[username]}_{title}",         # Custom format for tracks
    playlist_name_format="{tracknumber}_{title}"    # Custom format for playlists
)

track_url = "https://soundcloud.com/sadsvit/molodist"
result = downloader.download_track(track_url, overwrite=True)
print(result)
```

#### Handle Errors
```python
try:
    urls = downloader.search("nonexistent track", limit=1)
    if urls:
        result = downloader.download_track(urls[0])
        print(result)
    else:
        print("No tracks found")
except RuntimeError as e:
    print("Error:", e)
```

## API Reference

### SoundCloudDownloader Class

#### Initialization
```python
SoundCloudDownloader(
    output_dir: Optional[str] = None, 
    auth_token: Optional[str] = None, 
    client_id: Optional[str] = None, 
    name_format: str = "{user[username]} - {title}", 
    playlist_name_format: str = "{tracknumber} - {user[username]} - {title}"
)
```
- `output_dir`: Directory to save downloaded files (defaults to current directory).
- `auth_token`: SoundCloud authentication token (optional).
- `client_id`: SoundCloud API client ID (optional).
- `name_format`: File name format for individual tracks.
- `playlist_name_format`: File name format for tracks in playlists.

### Methods

#### `download_track(url: str, **kwargs) -> str`
Download a single track by URL.
Returns the command output from `scdl`.

#### `download_playlist(url: str, max_tracks: Optional[int] = None, offset: int = 0, **kwargs) -> str`
Download a playlist with an optional limit and offset.

#### `download_likes(url: str, max_tracks: Optional[int] = None, offset: int = 0, **kwargs) -> str`
Download a user's liked tracks.

#### `download_all_tracks(url: str, max_tracks: Optional[int] = None, offset: int = 0, **kwargs) -> str`
Download all tracks uploaded by a user (excluding reposts).

#### `download_reposts(url: str, max_tracks: Optional[int] = None, offset: int = 0, **kwargs) -> str`
Download all reposts by a user.

#### `search(query: str, limit: int = 1) -> List[str]`
Search for tracks and return their URLs without downloading.

#### `search_and_download(query: str, limit: int = 1, **kwargs) -> str`
Search for tracks and download the results.

### Keyword Arguments (`**kwargs`)

- `continue_on_error: bool = True`: Continue if a file already exists.
- `overwrite: bool = False`: Overwrite existing files.
- `only_mp3: bool = False`: Download only MP3 files.
- `original_art: bool = False`: Use original artwork instead of 500x500 JPEG.

### Notes

- The `search` method parses `scdl` debug output, which may break if `scdl`'s logging changes.
- Ensure `scdl` is installed and accessible in your PATH.
- Authentication (`auth_token`) is optional but required for private tracks.
