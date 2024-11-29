# macOS Audio Tagger

A desktop application for editing audio file metadata on macOS. Built with Python, PyQt6, and Mutagen.

## Features

- Edit common audio metadata fields:
  - Title
  - Artist
  - Album Artist
  - Album
  - Disc Number
  - Track Number
  - Year
  - Genre
  - Comment
  - Composer
- Supports multiple audio formats:
  - MP3 (ID3 tags)
  - M4A (iTunes metadata)
  - FLAC

## Requirements

- Python 3.9 or higher
- PyQt6
- Mutagen

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/barneephife/macos-audio-tagger.git
   cd macos-audio-tagger
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python src/main.py
   ```

2. Click 'Select File' to choose an audio file
3. Edit the metadata fields as needed
4. Click 'Save Changes' to update the file

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
=======

