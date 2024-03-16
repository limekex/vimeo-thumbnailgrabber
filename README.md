# Vimeo Thumbnail Downloader

Vimeo Thumbnail Downloader is a Python script that allows users to download all video thumbnails from a specified Vimeo channel. It provides a simple interface to input a Vimeo channel name or ID and saves the thumbnails locally for easy access.

## Features

- Download all thumbnails from a Vimeo channel
- Securely store Vimeo access token
- Automatically handle pagination for channels with many videos
- Save thumbnails in a dedicated `downloads` folder
- User-friendly setup for first-time use

## Getting Started

### Prerequisites

- Python 3.6 or later
- `requests` and `cryptography` libraries

### Installation

1. Clone the repository:
git clone https://github.com/yourusername/vimeo-thumbnailgrabber.git
2. Navigate to the project directory:
cd vimeo-thumbnailgrabber
3. Install the required packages:
pip install -r requirements.txt

### Usage

Run the script from the command line:

python download_thumbnails.py


Follow the on-screen instructions to input your Vimeo access token and the channel name or ID from which you want to download thumbnails.

## Configuration

The script uses a `config.txt` file to store the encrypted Vimeo access token securely. On first run, you'll be prompted to enter your access token, which will be saved for future use.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to suggest improvements or add new features.

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to Vimeo for providing the API that made this project possible.
- Special thanks to all contributors who have helped improve this tool.
