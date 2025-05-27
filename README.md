# GoPro Video Concatenator

A Python script and standalone Windows executable to concatenate GoPro MP4 files by session number into a single video. This tool groups GoPro video files, verifies their compatibility (codec, resolution, frame rate), and merges them without re-encoding, using FFmpeg.

## Features
- Groups GoPro videos by session number (e.g., `0123` in `GX010123.MP4`).
- Supports all common GoPro file naming patterns: `GX`, `GH`, `GP`, `GOPR`, `GPAA`, `GPBB`.
- Checks video compatibility using `ffprobe` to ensure seamless concatenation.
- Concatenates videos using `ffmpeg` with the `concat` demuxer, preserving original quality.
- Outputs one video per session (e.g., `output_0123.mp4`).

## Supported File Names
The script recognizes the following GoPro file naming conventions:
- `GX<chapter><session>.MP4` (e.g., `GX010123.MP4`)
- `GH<chapter><session>.MP4` (e.g., `GH010123.MP4`)
- `GP<chapter><session>.MP4` (e.g., `GP010123.MP4`)
- `GOPR<session>.MP4` (e.g., `GOPR0123.MP4`)
- `GPAA<session>.MP4`, `GPBB<session>.MP4` (e.g., `GPAA0123.MP4`, `GPBB0123.MP4`)

Files are grouped by the 4-digit session number (e.g., `0123`) and sorted by chapter number or clip order (e.g., `GOPR` followed by `GPAA`, `GPBB`).

## Usage (Executable)
The standalone `mp4_merge.exe` is for Windows 10 and up and includes `ffmpeg.exe` and `ffprobe.exe`.

1. Download `mp4_merge.exe` from the [Releases](https://github.com/B-KC/mp4_merge/releases) page.
2. Open a Command Prompt and navigate to the folder containing `mp4_merge.exe`:
3. Run the executable:
4. Enter the full path to the folder containing your GoPro MP4 files (e.g., `C:\Videos\GoPro`).
5. The script will:
- Group files by session number.
- Check compatibility (codec, resolution, frame rate).
- Create output files like `output_0123.mp4` in the specified folder.

**Note**: No additional software is required, as `ffmpeg.exe` and `ffprobe.exe` are bundled in the executable.

## Usage (Source Code)
To run the script from source, you need Python and FFmpeg installed.

1. **Install Python**:
- Download and install [Python 3.11 or later](https://www.python.org/downloads/).
- Ensure Python is added to your system PATH during installation.

2. **Install FFmpeg**:
- Download the `ffmpeg-release-essentials.zip` from [Gyan’s FFmpeg builds](https://www.gyan.dev/ffmpeg/builds/).
- Extract the zip and add the `bin/` folder (containing `ffmpeg.exe` and `ffprobe.exe`) to your system PATH.
  - On Windows, edit the PATH environment variable via `Control Panel > System > Advanced system settings > Environment Variables`.

3. **Clone the Repository**:
   git clone https://github.com/B-KC/mp4-merge.git
   cd mp4-merge
   
4. **Run the Script**:
 python mp4_merge.py
- Enter the folder path containing GoPro MP4 files when prompted.
- Output files will be created in the specified folder.

**Note**: No additional Python dependencies are required.

## Installation for Source Usage
- **Python**: Version 3.11 or later.
- **FFmpeg**: Install `ffmpeg` and `ffprobe` and ensure they are accessible in your system PATH.
- **Dependencies**: The script uses only standard Python libraries (`os`, `re`, `subprocess`, `json`, `pathlib`, `sys`).

## Project Structure
mp4-merge/
├── mp4_merge.py         # Main Python script
├── LICENSE              # MIT License for the script
├── README.md            # This file
├── .gitignore           # Git ignore file


**Note**: The `bin/` folder with `ffmpeg.exe` and `ffprobe.exe` is included in the `.exe` but excluded from the repository to reduce size. Source users must install FFmpeg separately.

## License
- **mp4_merge.py**: Licensed under the [MIT License](./LICENSE).
- **FFmpeg/FFprobe**: Licensed under the GNU General Public License (GPL) version 2 or later. See [FFmpeg License](https://ffmpeg.org/legal.html).
- **FFmpeg Source Code**: Available at [FFmpeg GitHub](https://github.com/FFmpeg/FFmpeg) or [Gyan’s FFmpeg releases](https://github.com/GyanD/codexffmpeg/releases).

**GPL Compliance**: The `mp4_merge.exe` executable includes `ffmpeg.exe` and `ffprobe.exe` and is distributed under the GPL due to FFmpeg’s licensing. The source code for FFmpeg is linked above, as required by the GPL.

## Contributing
Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## Issues
If you encounter issues (e.g., unsupported file names or errors with the `.exe`), please:
- Check the [Issues](https://github.com/yourusername/mp4-merge/issues) page.
- Submit a new issue with details (e.g., error messages, file names).

## Contact
For questions or support, contact [yourusername] via GitHub Issues.

## Acknowledgments
- Built with [Python](https://www.python.org/) and [FFmpeg](https://ffmpeg.org/).
- Thanks to [Gyan’s FFmpeg builds](https://www.gyan.dev/ffmpeg/builds/) for providing Windows binaries.

