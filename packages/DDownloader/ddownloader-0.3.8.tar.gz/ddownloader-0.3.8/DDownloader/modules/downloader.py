import os, requests
import subprocess
import logging
import platform
import coloredlogs
from tqdm import tqdm
from colorama import Fore

logger = logging.getLogger(Fore.RED + "+ DDOWNLOADER + ")
coloredlogs.install(level='DEBUG', logger=logger)

class DOWNLOADER:
    def __init__(self):
        self.manifest_url = None
        self.output_name = None
        self.proxy = None
        self.decryption_keys = []
        self.headers = []
        self.binary_path = None

# =========================================================================================================== #

    def _get_binary_path(self, binary_type):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(base_dir)
        bin_dir = os.path.join(project_root, 'bin')

        if binary_type == 'N_m3u8DL-RE':
            binary_name = 'N_m3u8DL-RE.exe' if platform.system() == 'Windows' else 'N_m3u8DL-RE'
        elif binary_type == 'ffmpeg':
            binary_name = 'ffmpeg.exe' if platform.system() == 'Windows' else 'ffmpeg'
        else:
            raise ValueError(f"Unknown binary type: {binary_type}")

        binary_path = os.path.join(bin_dir, binary_name)

        if not os.path.isfile(binary_path):
            logger.error(f"Binary not found: {binary_path}")
            raise FileNotFoundError(f"Binary not found: {binary_path}")

        if platform.system() == 'Linux':
            chmod_command = ['chmod', '+x', binary_path]
            try:
                subprocess.run(chmod_command, check=True)
                logger.info(Fore.CYAN + f"Set executable permission for: {binary_path}" + Fore.RESET)
            except subprocess.CalledProcessError as e:
                logger.error(Fore.RED + f"Failed to set executable permissions for: {binary_path}" + Fore.RESET)
                raise RuntimeError(f"Could not set executable permissions for: {binary_path}") from e

        return binary_path

# =========================================================================================================== #

    def drm_downloader(self):
        if not self.manifest_url:
            logger.error("Manifest URL is not set.")
            return
        command = self._build_command()
        self._execute_command(command)

# =========================================================================================================== #

    def _build_command(self):
        command = [
            self._get_binary_path("N_m3u8DL-RE"),
            f'"{self.manifest_url}"',
            '-mt',
            '-M', 'format=mp4',
            '--save-dir', '"downloads"',
            '--tmp-dir', '"downloads"',
            '--del-after-done',
            '--decryption-engine', '"FFMPEG"',
            '--decryption-binary-path', f'"{self._get_binary_path("ffmpeg")}"',
            '--save-name', f'"{self.output_name}"'
        ]

        for key in self.decryption_keys:
            command.extend(['--key', f'"{key}"'])

        if self.proxy:
            if not self.proxy.startswith("http://"):
                self.proxy = f"http://{self.proxy}"
            command.extend(['--custom-proxy', f'"{self.proxy}"'])

        for header in self.headers:
            command.extend(['-H', f'"{header}"'])

        return command

# =========================================================================================================== #

    def _execute_command(self, command):
        try:
            command_str = ' '.join(command)
            result = os.system(command_str)

            if result == 0:
                logger.info(Fore.GREEN + "Downloaded successfully. Bye!" + Fore.RESET)
                print(Fore.RED + "═" * 100 + Fore.RESET + "\n")
            else:
                pass

        except Exception as e:
            logger.error(Fore.RED + f"An unexpected error occurred: {e}" + Fore.RESET)

# =========================================================================================================== #

    def re_encode_content(self, input_file, quality, codec="libx265", crf=20, preset="medium", audio_bitrate="256k"):
        resolutions = {
            "HD": "1280:720",
            "FHD": "1920:1080",
            "UHD": "3840:2160"
        }

        quality = quality.upper()
        if quality not in resolutions:
            logger.error(f"Invalid quality '{quality}'. Choose from: HD, FHD, UHD.")
            return None

        input_file = os.path.abspath(input_file)
        if not os.path.isfile(input_file):
            logger.error(f"Input file does not exist: {input_file}")
            return None

        resolution = resolutions[quality]
        base_name, ext = os.path.splitext(input_file)
        output_file = os.path.abspath(f"{base_name}_{quality.lower()}{ext}")

        self.binary_path = self._get_binary_path("ffmpeg")

        logger.info(f"Re-encoding {input_file} to {quality} ({resolution}) using codec {codec}...")
        logger.info(f"Output file: {output_file}")

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Build the ffmpeg command
        command = [
            self.binary_path,
            "-i", f"\"{input_file}\"",
            "-vf", f"scale={resolution}",
            "-c:v", codec,
            "-crf", str(crf),
            "-preset", preset,
            "-c:a", "aac",
            "-b:a", audio_bitrate,
            "-movflags", "+faststart",
            f"\"{output_file}\""
        ]

        # Execute the command using `_execute_command`
        self._execute_command(command)

        # Check if output file exists to confirm success
        if os.path.isfile(output_file):
            logger.info(f"Re-encoding to {quality} completed successfully. Output saved to: {output_file}")
            return output_file
        else:
            logger.error(f"Re-encoding failed. Output file not created: {output_file}")
            return None
        
# =========================================================================================================== #

    def normal_downloader(self, url, output_file):
        """
        Download a video file from a given URL with a progress bar.
        Automatically adds .mp4 extension if missing.

        Args:
            url (str): The video URL to download.
            output_file (str): The output file path to save the video.
        """
        try:
            # Add .mp4 extension if not already present
            if not output_file.lower().endswith(".mp4"):
                output_file += ".mp4"

            # Send a GET request to the URL with stream=True
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Get the total file size from the headers
            total_size = int(response.headers.get('content-length', 0))

            # Open the output file in binary write mode
            with open(output_file, 'wb') as file:
                # Use tqdm to show a progress bar
                with tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=f"Downloading {os.path.basename(output_file)}",
                ) as progress:
                    # Write the content in chunks
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
                        progress.update(len(chunk))

            print(f"Download complete: {output_file}")

        except requests.exceptions.RequestException as e:
            print(f"Error during download: {e}")