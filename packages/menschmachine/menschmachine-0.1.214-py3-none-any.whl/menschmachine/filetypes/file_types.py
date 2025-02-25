import os
from enum import Enum

code_suffixes = ["ts", "js", "java", "py", "c", "cc", "rb", "kt", "html"]
with open(os.path.dirname(os.path.realpath(__file__)) + '/code-file-extensions.txt') as f:
    code_suffixes.extend([x.strip() for x in f.read().splitlines()])

config_suffixes = ["properties", "yaml", "cfg", "conf", "xml"]
documentation_suffixes = ["md", "txt", "rst", "adoc"]
script_suffixes = ["sh", "bat", "cmd"]
asset_suffixes = ['jpg', 'jpeg', 'jpe', 'jif', 'jfif', 'jfi',  # JPEG images
                  'png',  # PNG images
                  'gif',  # GIF images
                  'webp',  # WebP images
                  'tiff', 'tif',  # TIFF images
                  'bmp', 'dib',  # BMP images
                  'jp2', 'j2k', 'jpf', 'jpx', 'jpm', 'mj2',  # JPEG 2000 images
                  'svg', 'svgz',  # SVG images
                  'ico', 'cur',  # Icon files
                  'heic', 'heif',  # High Efficiency Image Format
                  'psd',  # Adobe Photoshop files
                  'ai',  # Adobe Illustrator files
                  'raw', 'arw', 'cr2', 'nrw', 'k25',  # RAW images
                  'webp',  # WebP images
                  'tga',  # Truevision TGA
                  'pcx',  # PCX images
                  'ttf',  # TrueType Font
                  'otf',  # OpenType Font
                  'woff',  # Web Open Font Format
                  'woff2',  # Web Open Font Format 2
                  'eot',  # Embedded OpenType
                  'pfb',  # Type 1 Font (Printer Font Binary)
                  'pfm',  # Printer Font Metrics
                  'afm',  # Adobe Font Metrics
                  'tfm',  # TeX Font Metrics
                  'fon',  # Windows Font File
                  'fnt',  # Windows Font File
                  'bdf',  # Bitmap Distribution Format
                  'pcf',  # Portable Compiled Format
                  'snf',  # Server Normal Format
                  'otb',  # OpenType Bitmap
                  'cff',  # Compact Font Format
                  'psf',  # PC Screen Font
                  'ttc',  # TrueType Collection
                  'sfd',  # FontForge Spline Font Database
                  'ufo',  # Unified Font Object
                  'pfa',  # Printer Font ASCII
                  'dfont'  # Mac OS X Data Fork Font
                  ]
binary_suffixes = ["exe", "dll", "so", "lib", "bin"]
test_suffixes = ["test", "spec"]
data_suffixes = ["csv", "tsv", "json", "yml", "xls", "xlsx", "ods", "tsv"]


class FileType(Enum):
    CODE = "CODE"
    CONFIG = "CONFIG"
    DOCUMENTATION = "DOCUMENTATION"
    SPEC = "SPEC"
    SCRIPT = "SCRIPT"
    ASSET = "ASSET"
    BINARY = "BINARY"
    TEST = "TEST"
    HELPER = "HELPER"
    DATA = "DATA"
    UNKNOWN = "UNKOWN"


def get_file_type(filename: str) -> FileType:
    _, suffix = os.path.splitext(filename)
    if suffix.startswith("."):
        suffix = suffix[1:]
    suffix = suffix.lower()
    if suffix in documentation_suffixes:
        return FileType.DOCUMENTATION
    if suffix in script_suffixes:
        return FileType.SCRIPT
    if suffix in asset_suffixes:
        return FileType.ASSET
    if suffix in binary_suffixes:
        return FileType.BINARY
    if suffix in test_suffixes:
        return FileType.TEST
    if suffix in data_suffixes:
        return FileType.DATA
    if suffix in config_suffixes:
        return FileType.CONFIG
    if suffix in code_suffixes:
        return FileType.CODE
    return FileType.UNKNOWN
