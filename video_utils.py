import ffmpy
import tempfile
import os
from pathlib import Path

class VideoProcessor:
    """
    A utility class for video processing operations.

    Methods:
        combine_videos(file_paths, output_file_path): Combines multiple video files into a single video.
    """

    @staticmethod
    def combine_videos(file_paths, output_file_path):
        """
        Combines multiple video files into a single video.

        Args:
            file_paths (list): A list of input file paths.
            output_file_path (str): The output file path for the combined video.

        Returns:
            str: The output file path of the combined video if successful, None otherwise.
        """
        try:
            temp_file_path = VideoProcessor._create_temp_file(file_paths)

            inputs = {temp_file_path: ["-f", "concat", "-safe", "0"]}
            outputs = {output_file_path: ["-c", "copy"]}
            ff = ffmpy.FFmpeg(inputs=inputs, outputs=outputs)
            ff.run()
            os.unlink(temp_file_path)

            return output_file_path
        except Exception as e:
            print(f"Error occurred during video combining: {str(e)}")
            return None

    @staticmethod
    def _create_temp_file(file_paths):
        """
        Creates a temporary file listing the input file paths.

        Args:
            file_paths (list): A list of input file paths.

        Returns:
            str: The path of the temporary file.
        """
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            for path in file_paths:
                f.write(f"file '{path}'\n")
            return Path(f.name).as_posix()
