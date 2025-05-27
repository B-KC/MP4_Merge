import os
import re
import subprocess
import json
from pathlib import Path
import sys

# Get the directory of the executable (or script if not frozen)
BASE_DIR = Path(getattr(sys, '_MEIPASS', Path(__file__).parent))
FFMPEG_PATH = BASE_DIR / "bin" / "ffmpeg.exe"
FFPROBE_PATH = BASE_DIR / "bin" / "ffprobe.exe"

def get_video_info(file_path):
    """Extract video stream info using ffprobe."""
    cmd = [
        str(FFPROBE_PATH),
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=codec_name,width,height,r_frame_rate",
        "-of", "json",
        file_path
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)["streams"][0]
    except subprocess.CalledProcessError as e:
        print(f"Error running ffprobe on {file_path}: {e}")
        return None
    except FileNotFoundError:
        print("Error: ffprobe.exe not found in the bin directory.")
        return None

def check_compatibility(files):
    """Verify that all files have the same codec, resolution, and frame rate."""
    if not files:
        return False
    first_info = get_video_info(files[0])
    if not first_info:
        return False
    for file in files[1:]:
        info = get_video_info(file)
        if not info:
            return False
        if (info["codec_name"] != first_info["codec_name"] or
            info["width"] != first_info["width"] or
            info["height"] != first_info["height"] or
            info["r_frame_rate"] != first_info["r_frame_rate"]):
            print(f"Incompatible file {file}: {info} vs {first_info}")
            return False
    return True

def group_gopro_files(files):
    """Group GoPro files by session number and sort by chapter or clip order."""
    groups = {}
    # Regex to match GoPro file patterns: GX/GH/GP/GOPR/GPAA/GPBB + 4-digit session, optional 2-digit chapter
    pattern = re.compile(r"^(?:GX|GH|GP|GOPR|GPAA|GPBB)(\d{2})?(\d{4})\.MP4$", re.IGNORECASE)
    for filename in files:
        match = pattern.match(filename)
        if not match:
            print(f"Skipping invalid filename: {filename}")
            continue
        chapter, session = match.groups()
        # Use session number as group key
        if session not in groups:
            groups[session] = []
        groups[session].append(filename)
    # Sort files within each group by chapter number (if present) or filename
    for session in groups:
        groups[session] = sorted(groups[session], key=lambda f: (
            # Extract chapter number (if present) or use 0 for files like GOPR
            int(re.match(r"^(?:GX|GH|GP)(\d{2})\d{4}\.MP4$", f, re.IGNORECASE).group(1)) if re.match(r"^(?:GX|GH|GP)(\d{2})\d{4}\.MP4$", f, re.IGNORECASE) else 0,
            # Secondary sort by prefix (GOPR, GPAA, GPBB) to maintain clip order
            f
        ))
    return groups

def concatenate_videos(folder_path, output_prefix="output"):
    """Concatenate GoPro videos in the specified folder, grouped by session."""
    folder = Path(folder_path)
    if not folder.is_dir():
        print(f"Error: {folder_path} is not a valid directory.")
        return
    # Find all MP4 files
    files = [f for f in folder.glob("*.MP4") if f.is_file()]
    if not files:
        print(f"No MP4 files found in {folder_path}.")
        return
    # Group files by session
    groups = group_gopro_files([f.name for f in files])
    if not groups:
        print("No valid GoPro files found.")
        return
    # Process each group
    for session, group_files in groups.items():
        group_files = [folder / f for f in group_files]
        print(f"Processing session {session}: {[f.name for f in group_files]}")
        # Check compatibility within the group
        if not check_compatibility(group_files):
            print(f"Skipping session {session}: Files are not compatible.")
            continue
        # Create file list for ffmpeg concat demuxer
        filelist_path = folder / f"filelist_{session}.txt"
        with open(filelist_path, "w") as f:
            for file in group_files:
                f.write(f"file '{file}'\n")
        # Run ffmpeg to concatenate
        output_file = folder / f"{output_prefix}_{session}.mp4"
        cmd = [
            str(FFMPEG_PATH),
            "-f", "concat",
            "-safe", "0",
            "-i", str(filelist_path),
            "-c", "copy",
            "-fflags", "+genpts",
            str(output_file)
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"Successfully created {output_file}")
            filelist_path.unlink()  # Clean up
        except subprocess.CalledProcessError as e:
            print(f"Error running ffmpeg for session {session}: {e.stderr}")
        except FileNotFoundError:
            print("Error: ffmpeg.exe not found in the bin directory.")

if __name__ == "__main__":
    while True:
        folder_path = input("Please enter the folder path containing GoPro MP4 files (e.g., C:\\Videos\\GoPro): ").strip()
        if not folder_path:
            print("Error: Folder path cannot be empty.")
            continue
        if Path(folder_path).is_dir():
            break
        else:
            print(f"Error: '{folder_path}' is not a valid directory. Please try again.")
    concatenate_videos(folder_path)