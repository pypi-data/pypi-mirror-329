# SoundCloud Downloader

A Python library for downloading music from SoundCloud using the `scdl` tool. This library provides a simple and programmatic interface to search for and download tracks, playlists, likes, reposts, and more, without relying solely on the command-line interface of `scdl`.

## Features

- Download individual tracks, playlists, user likes, all tracks, or reposts from SoundCloud.
- Search for tracks by query and download the results.
- Perform search-only operations to retrieve track URLs without downloading.
- Customize download options such as output directory, file name format, and authentication.
- Compatible with Python 3.6+ (tested up to Python 3.12).

## Prerequisites

- Python 3.6 or higher.
- The `scdl` package installed (`pip install scdl>=2.12.3`).
- (Optional) A SoundCloud authentication token and/or client ID for private tracks or extended functionality.