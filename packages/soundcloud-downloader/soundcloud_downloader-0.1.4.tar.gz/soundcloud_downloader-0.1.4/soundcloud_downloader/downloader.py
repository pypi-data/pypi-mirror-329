import subprocess
import os
from typing import Optional, Literal, List

class SoundCloudDownloader:
    def __init__(
        self,
        output_dir: Optional[str] = None,
        auth_token: Optional[str] = None,
        client_id: Optional[str] = None,
        name_format: str = "{user[username]} - {title}",  # Updated default format
        playlist_name_format: str = "{tracknumber} - {user[username]} - {title}"  # Updated default format
    ):
        """
        Initialize the SoundCloud downloader.

        :param output_dir: Directory to save downloaded files (default is current directory).
        :param auth_token: SoundCloud authentication token (optional).
        :param client_id: SoundCloud API client ID (optional).
        :param name_format: File name format for individual tracks.
        :param playlist_name_format: File name format for tracks in playlists.
        """
        self.output_dir = output_dir or os.getcwd()
        self.auth_token = auth_token
        self.client_id = client_id
        self.name_format = name_format
        self.playlist_name_format = playlist_name_format

        # Check if scdl is installed
        if not self._is_scdl_installed():
            raise RuntimeError("scdl is not installed. Install it with 'pip install scdl'")

    def _is_scdl_installed(self) -> bool:
        """Check if scdl is available on the system."""
        try:
            subprocess.run(["scdl", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _build_command(
        self,
        url_or_query: str,
        action_type: Literal["track", "playlist", "likes", "all_tracks", "reposts", "search", "search_only"],
        continue_on_error: bool = True,
        overwrite: bool = False,
        only_mp3: bool = False,
        original_art: bool = False,
        max_tracks: Optional[int] = None,
        offset: int = 0
    ) -> list[str]:
        """Build the scdl command based on parameters."""
        print(f"Building command for {action_type} with URL/query: {url_or_query}")
        if action_type == "search" or action_type == "search_only":
            cmd = ["scdl", "-s", url_or_query]
            if max_tracks:
                cmd.extend(["-n", str(max_tracks)])  # Limit search results
            if action_type == "search_only":
                cmd.extend(["--debug"])
        else:
            cmd = ["scdl", "-l", url_or_query]

            # Download type
            if action_type == "playlist":
                cmd.append("-p")
            elif action_type == "likes":
                cmd.append("-f")
            elif action_type == "all_tracks":
                cmd.append("-t")
            elif action_type == "reposts":
                cmd.append("-r")
            # "track" doesn't need a flag

            # Common parameters for downloads
            if continue_on_error:
                cmd.append("-c")
            if overwrite:
                cmd.append("--overwrite")
            if only_mp3:
                cmd.append("--onlymp3")
            if original_art:
                cmd.append("--original-art")
            if max_tracks and action_type != "search":
                cmd.extend(["-n", str(max_tracks)])  # Limit number of tracks
            if offset > 0 and action_type != "search":
                cmd.extend(["-o", str(offset)])
            if self.output_dir != os.getcwd():
                cmd.extend(["--path", self.output_dir])

        # Authentication and formatting
        if self.auth_token:
            cmd.extend(["--auth-token", self.auth_token])
        if self.client_id:
            cmd.extend(["--client-id", self.client_id])
        if action_type != "search_only":
            cmd.extend(["--name-format", self.name_format])
            cmd.extend(["--playlist-name-format", self.playlist_name_format])

        return cmd

    def _execute_command(self, cmd: list[str]) -> str:
        """Execute the scdl command and return its output."""
        print(f"Executing command: {' '.join(cmd)}")
        try:
            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30  # Added timeout to prevent hanging
            )
            output = result.stdout + result.stderr
            print("Command output:", output)
            return output
        except subprocess.TimeoutExpired as e:
            raise RuntimeError(f"scdl timed out after 30 seconds: {e.stderr}")
        except subprocess.CalledProcessError as e:
            error_msg = f"Error executing scdl: {e.stderr}"
            raise RuntimeError(error_msg)

    def download_track(self, url: str, **kwargs) -> str:
        """
        Download a single track.

        :param url: SoundCloud track URL.
        :param kwargs: Additional parameters (continue_on_error, overwrite, only_mp3, original_art).
        :return: Command output.
        """
        cmd = self._build_command(url, "track", **kwargs)
        return self._execute_command(cmd)

    def download_playlist(self, url: str, max_tracks: Optional[int] = None, offset: int = 0, **kwargs) -> str:
        """
        Download a playlist.

        :param url: SoundCloud playlist URL.
        :param max_tracks: Maximum number of tracks to download.
        :param offset: Offset (starting track index).
        :param kwargs: Additional parameters.
        :return: Command output.
        """
        cmd = self._build_command(url, "playlist", max_tracks=max_tracks, offset=offset, **kwargs)
        return self._execute_command(cmd)

    def download_likes(self, url: str, max_tracks: Optional[int] = None, offset: int = 0, **kwargs) -> str:
        """
        Download a user's likes.

        :param url: SoundCloud user profile URL.
        :param max_tracks: Maximum number of tracks.
        :param offset: Offset.
        :param kwargs: Additional parameters.
        :return: Command output.
        """
        cmd = self._build_command(url, "likes", max_tracks=max_tracks, offset=offset, **kwargs)
        return self._execute_command(cmd)

    def download_all_tracks(self, url: str, max_tracks: Optional[int] = None, offset: int = 0, **kwargs) -> str:
        """
        Download all tracks by a user (excluding reposts).

        :param url: SoundCloud user profile URL.
        :param max_tracks: Maximum number of tracks.
        :param offset: Offset.
        :param kwargs: Additional parameters.
        :return: Command output.
        """
        cmd = self._build_command(url, "all_tracks", max_tracks=max_tracks, offset=offset, **kwargs)
        return self._execute_command(cmd)

    def download_reposts(self, url: str, max_tracks: Optional[int] = None, offset: int = 0, **kwargs) -> str:
        """
        Download all reposts by a user.

        :param url: SoundCloud user profile URL.
        :param max_tracks: Maximum number of tracks.
        :param offset: Offset.
        :param kwargs: Additional parameters.
        :return: Command output.
        """
        cmd = self._build_command(url, "reposts", max_tracks=max_tracks, offset=offset, **kwargs)
        return self._execute_command(cmd)

    def search(self, query: str, limit: int = 1) -> List[str]:
        """
        Search for tracks on SoundCloud and return their URLs without downloading.

        :param query: Search query (e.g., song title, artist name).
        :param limit: Number of results to return (default is 1).
        :return: List of URLs found in the search results.
        """
        cmd = self._build_command(query, "search_only", max_tracks=limit)
        output = self._execute_command(cmd)

        urls = []
        for line in output.splitlines():
            if "Search resolved to url" in line:
                url = line.split("Search resolved to url")[-1].strip()
                urls.append(url)
            if len(urls) >= limit:
                break
        
        if not urls:
            raise RuntimeError(f"No results found for query: {query}")
        
        return urls

    def search_and_download(self, query: str, limit: int = 1, **kwargs) -> str:
        """
        Search for tracks and download the results.

        :param query: Search query (e.g., song title, artist name).
        :param limit: Number of results to download (default is 1).
        :param kwargs: Additional parameters (continue_on_error, overwrite, only_mp3, original_art).
        :return: Command output.
        """
        cmd = self._build_command(query, "search", max_tracks=limit, **kwargs)
        return self._execute_command(cmd)