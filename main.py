"""QR Code Generator.

Generates a PNG QR code for a URL and saves it to a folder.

Usage:
    python main.py --url https://www.njit.edu

Configuration (environment variables, all optional):
    QR_CODE_DIR   folder for generated QR codes   (default: qr_codes)
    LOG_DIR       folder for log files            (default: logs)
    FILL_COLOR    QR code color                   (default: black)
    BACK_COLOR    background color                (default: white)
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import qrcode
import validators
from dotenv import load_dotenv

# Load variables from a .env file if one exists (handy for local runs)
load_dotenv()

QR_CODE_DIR = os.getenv("QR_CODE_DIR", "qr_codes")
LOG_DIR = os.getenv("LOG_DIR", "logs")
FILL_COLOR = os.getenv("FILL_COLOR", "black")
BACK_COLOR = os.getenv("BACK_COLOR", "white")


def setup_logging() -> None:
    """Log to the console (for `docker logs`) and to logs/app.log."""
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(Path(LOG_DIR) / "app.log"),
        ],
    )


def is_valid_url(url: str) -> bool:
    if validators.url(url):
        return True
    logging.error(f"Invalid URL provided: {url}")
    return False


def generate_qr_code(data: str, path: Path, fill_color: str, back_color: str) -> bool:
    """Create the QR code image and save it to `path`."""
    if not is_valid_url(data):
        return False
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(path)
        logging.info(f"QR code successfully saved to {path}")
        return True
    except Exception as e:
        logging.error(f"An error occurred while generating or saving the QR code: {e}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a QR code for a URL.")
    parser.add_argument(
        "--url",
        default="https://github.com/kaw393939",
        help="The URL to encode in the QR code",
    )
    args = parser.parse_args()

    setup_logging()
    logging.info(f"Generating QR code for: {args.url}")
    logging.info(f"Settings: QR_CODE_DIR={QR_CODE_DIR}, FILL_COLOR={FILL_COLOR}, BACK_COLOR={BACK_COLOR}")

    out_dir = Path.cwd() / QR_CODE_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = f"QRCode_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"

    ok = generate_qr_code(args.url, out_dir / filename, FILL_COLOR, BACK_COLOR)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
