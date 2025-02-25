import requests
import os
import platform
import zipfile
import tarfile

class GitHub:
    GITHUB_AUTHOR = "WebAssembly"
    GITHUB_REPOSITORY = "wabt"
    BASE_URL = f"https://api.github.com/repos/{GITHUB_AUTHOR}/{GITHUB_REPOSITORY}"

    @staticmethod
    def get_latest_release():
        """
        Get the latest release data from the GitHub repository.
        """
        try:
            response = requests.get(f"{GitHub.BASE_URL}/releases/latest")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Failed to get latest release from GitHub: {e}")

    @staticmethod
    def detect_os():
        """
        Detect the current operating system and return a string identifier.
        """
        os_name = platform.system().lower()
        if os_name == "windows":
            return "windows"
        elif os_name == "darwin":
            return "macos"
        elif os_name == "linux":
            return "ubuntu"
        else:
            raise Exception(f"Unsupported operating system: {os_name}")

    @staticmethod
    def find_asset_for_os(assets, os_identifier):
        """
        Find the correct asset for the detected operating system.

        Args:
            assets (list): List of assets from the GitHub release.
            os_identifier (str): OS identifier (e.g., "windows", "macos", "ubuntu").

        Returns:
            dict: The asset dictionary for the correct OS.
        """
        for asset in assets:
            if os_identifier in asset["name"].lower():
                return asset
        raise Exception(f"No suitable asset found for OS: {os_identifier}")

    @staticmethod
    def download_asset(asset, output_dir="."):
        """
        Download the specified asset.

        Args:
            asset (dict): The asset dictionary containing the download URL.
            output_dir (str): Directory to save the downloaded file.

        Returns:
            str: Path to the downloaded file.
        """
        try:
            download_url = asset["browser_download_url"]
            file_name = asset["name"]
            output_path = os.path.join(output_dir, file_name)

            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                with open(output_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            return output_path
        except Exception as e:
            raise Exception(f"Failed to download asset: {e}")

    @staticmethod
    def extract_file(file_path, output_dir="."):
        """
        Extract the downloaded file if it is a .zip, .tar.gz, or .tar.xz file.

        Args:
            file_path (str): Path to the file to be extracted.
            output_dir (str): Directory to extract the contents to.

        Returns:
            str: Path to the extracted directory.
        """
        try:
            if file_path.endswith(".zip"):
                with zipfile.ZipFile(file_path, "r") as zip_ref:
                    zip_ref.extractall(output_dir)
            elif file_path.endswith(".tar.gz") or file_path.endswith(".tar.xz"):
                with tarfile.open(file_path, "r:*") as tar_ref:
                    tar_ref.extractall(output_dir)
            else:
                raise Exception(f"Unsupported file format for extraction: {file_path}")

            return output_dir
        except Exception as e:
            raise Exception(f"Failed to extract file: {e}")

    @staticmethod
    def download_and_extract_latest_for_os(output_dir="."):
        """
        Download and extract the latest release asset for the current operating system.

        Args:
            output_dir (str): Directory to save and extract the downloaded file.

        Returns:
            str: Path to the extracted directory.
        """
        try:
            release_data = GitHub.get_latest_release()
            os_identifier = GitHub.detect_os()

            assets = release_data.get("assets", [])
            if not assets:
                raise Exception("No assets found in the latest release.")
            asset = GitHub.find_asset_for_os(assets, os_identifier)

            downloaded_file = GitHub.download_asset(asset, output_dir)
            _ = GitHub.extract_file(downloaded_file, output_dir)

            return downloaded_file
        except Exception as e:
            raise Exception(f"Failed to download and extract the latest release for OS: {e}")