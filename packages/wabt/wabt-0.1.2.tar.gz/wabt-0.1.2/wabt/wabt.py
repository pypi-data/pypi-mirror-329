import os
import subprocess
import platform
from appdirs import user_data_dir
from .github import GitHub

class Wabt:
    """
    A Python wrapper for the WebAssembly Binary Toolkit (WABT).
    """
    APP_NAME = "wabt-py"
    DOWNLOAD_DIR = user_data_dir(APP_NAME)

    def __init__(self, skip_update: bool = False):
        """
        Initialize the Wabt class. Optionally skip the update process.

        Args:
            skip_update (bool): If True, skip checking for updates.
        """
        if not skip_update:
            self.update()

        self.bin_dir = os.path.join(self.DOWNLOAD_DIR, f"wabt-{self.get_current_version()}", "bin")
        if not os.path.exists(self.bin_dir):
            self.update()
            if not os.path.exists(self.bin_dir):
                raise FileNotFoundError(f"Binary directory still not found: {self.bin_dir}")

    def get_current_version(self):
        """
        Get the currently installed version of WABT by checking the folder name.

        Returns:
            str: The current version (e.g., "1.0.36"), or None if no version is installed.
        """
        if not os.path.exists(self.DOWNLOAD_DIR):
            return None

        for folder_name in os.listdir(self.DOWNLOAD_DIR):
            if folder_name.startswith("wabt-"):
                return folder_name.split("-")[1]
        
        return None

    def update(self):
        """
        Update WABT if the latest version is not already installed.
        """
        try:
            latest_release = GitHub.get_latest_release()
            latest_version = latest_release["tag_name"]

            current_version = self.get_current_version()
            if current_version == latest_version: return

            os.makedirs(self.DOWNLOAD_DIR, exist_ok=True)

            downloaded_file = GitHub.download_and_extract_latest_for_os(output_dir=self.DOWNLOAD_DIR)
            os.remove(downloaded_file)
        except Exception as e:
            raise Exception(f"Failed to update WABT: {e}")

    def get_executable_name(self, executable_name):
        """
        Get the correct executable name based on the operating system.

        Args:
            executable_name (str): The base name of the executable (e.g., "spectest-interp").

        Returns:
            str: The full executable name with the appropriate extension for the OS.
        """
        if platform.system().lower() == "windows":
            return f"{executable_name}.exe"
        
        return executable_name

    def run_executable(self, executable_name, args):
        """
        Run a WABT executable with the given arguments.

        Args:
            executable_name (str): The name of the executable (e.g., "spectest-interp").
            args (list): A list of arguments to pass to the executable.

        Returns:
            str: The stdout output of the executable.
        """
        executable_name = self.get_executable_name(executable_name)
        executable_path = os.path.join(self.bin_dir, executable_name)

        if not os.path.exists(executable_path):
            raise FileNotFoundError(f"Executable not found: {executable_path}")

        try:
            result = subprocess.run(
                [executable_path, *args],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(
                f"Error running {executable_name}:\n"
                f"STDOUT:\n{e.stdout}\n"
                f"STDERR:\n{e.stderr}"
            )

    # Explicit methods for each WABT executable with detailed argument handling

    def spectest_interp(self, filename, options=None):
        """
        Run the `spectest-interp` executable.

        Args:
            filename (str): The Spectest JSON file to process.
            options (list): Additional options to pass to the executable.

        Returns:
            str: The stdout output of the executable.
        """
        args = [filename]
        if options:
            args.extend(options)
        return self.run_executable("spectest-interp", args)

    def wasm_decompile(self, filename, output=None, options=None):
        """
        Run the `wasm-decompile` executable.

        Args:
            filename (str): The input WebAssembly binary file.
            output (str): The output decompiled text file.
            options (list): Additional options to pass to the executable.

        Returns:
            str: The stdout output of the executable.
        """
        args = [filename]
        if output:
            args.extend(["-o", output])
        if options:
            args.extend(options)
        return self.run_executable("wasm-decompile", args)

    def wasm_interp(self, filename, options=None):
        """
        Run the `wasm-interp` executable.

        Args:
            filename (str): The input WebAssembly binary file.
            options (list): Additional options to pass to the executable.

        Returns:
            str: The stdout output of the executable.
        """
        args = [filename]
        if options:
            args.extend(options)
        return self.run_executable("wasm-interp", args)

    def wasm_objdump(self, filename, options=None):
        """
        Run the `wasm-objdump` executable.

        Args:
            filename (str): The input WebAssembly binary file.
            options (list): Additional options to pass to the executable.

        Returns:
            str: The stdout output of the executable.
        """
        args = [filename]
        if options:
            args.extend(options)
        return self.run_executable("wasm-objdump", args)

    def wasm_validate(self, filename, options=None):
        """
        Run the `wasm-validate` executable.

        Args:
            filename (str): The input WebAssembly binary file.
            options (list): Additional options to pass to the executable.

        Returns:
            str: The stdout output of the executable.
        """
        args = [filename]
        if options:
            args.extend(options)
        return self.run_executable("wasm-validate", args)

    def wat_to_wasm(self, filename, output=None, options=None):
        """
        Run the `wat2wasm` executable.

        Args:
            filename (str): The input WebAssembly text file.
            output (str): The output WebAssembly binary file.
            options (list): Additional options to pass to the executable.

        Returns:
            str: The stdout output of the executable.
        """
        args = [filename]
        if output:
            args.extend(["-o", output])
        if options:
            args.extend(options)
        return self.run_executable("wat2wasm", args)

    def wasm_to_wat(self, filename, output=None, options=None):
        """
        Run the `wasm2wat` executable.

        Args:
            filename (str): The input WebAssembly binary file.
            output (str): The output WebAssembly text file.
            options (list): Additional options to pass to the executable.

        Returns:
            str: The stdout output of the executable.
        """
        args = [filename]
        if output:
            args.extend(["-o", output])
        if options:
            args.extend(options)
        return self.run_executable("wasm2wat", args)