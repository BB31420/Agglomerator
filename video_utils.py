import ffmpy
import tempfile
import os
from pathlib import Path

def combine_videos(file_paths, output_file_path):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        for path in file_paths:
            f.write(f"file '{path}'\n")
        temp_file_path = Path(f.name).as_posix()

    inputs = {temp_file_path: ["-f", "concat", "-safe", "0"]}
    outputs = {output_file_path: ["-c", "copy"]}
    ff = ffmpy.FFmpeg(inputs=inputs, outputs=outputs)
    ff.run()
    os.unlink(temp_file_path)
