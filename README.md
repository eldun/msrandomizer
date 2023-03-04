# msrandomizer
A workaround script to create random kits for Elektron's Model:Samples. To be used with [Elektron Transfer](https://www.elektron.se/us/download-support-transfer)(Windows/MacOS) or [Elektroid](https://github.com/dagargo/elektroid)(Linux).

# Usage (from --help)
python3 msrandomizer.py [-h] [--kits [KITS]] sources [sources ...] dest

Create seqeuntially named directories - each containing six random audio files(.wav, .mp3, .aiff) collated from the provided source directories

positional arguments:
  sources
  dest

options:
  -h, --help            show this help message and exit
  --kits [KITS], -k [KITS]
                        The number of output folders('kits') to create. Default: 25

