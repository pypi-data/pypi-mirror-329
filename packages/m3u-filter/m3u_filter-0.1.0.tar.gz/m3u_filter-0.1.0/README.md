# M3U Filter

A cross-platform GUI application for filtering and managing M3U playlists with support for live TV, movies, and series.

## Features
- Filter M3U playlists by content type (Live TV, Movies, Series)
- Built-in HTTP server for serving filtered playlists
- VLC integration for preview
- Group-based channel management
- Export filtered playlists
- Support for various M3U sources (URL, Xtream, local file)

## System Requirements

1. Python 3.8 or higher
2. VLC media player (for preview functionality, not required)
   - Windows: Download and install from videolan.org
   - Linux: Install via your package manager
   - macOS: Install via homebrew or videolan.org

## Installation

1. Install VLC media player if not already installed
2. Install m3u-filter using pip:
```bash
# Windows
py -m pip install m3u-filter

# Linux/macOS
pip install m3u-filter
# or
pip3 install m3u-filter
# or
python3 -m pip install m3u-filter
```

## Usage
```bash
m3u-filter
```

## Requirements
- Python 3.8 or higher
- VLC media player (for preview functionality)

# License note
I would prefer to be using MIT, but I have to follow Qt, thus this is GPL-3