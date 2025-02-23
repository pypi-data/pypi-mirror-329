import mimetypes
from typing import Dict, List, Optional

# Mapping from file extensions (without the dot) to MIME types.
EXTENSION_TO_CONTENT_TYPE: Dict[str, str] = {
    # Text
    'txt': 'text/plain',
    'htm': 'text/html',
    'html': 'text/html',
    'css': 'text/css',
    'csv': 'text/csv',
    'tsv': 'text/tab-separated-values',
    'js': 'text/javascript',
    'mjs': 'text/javascript',
    'json': 'application/json',
    'map': 'application/json',
    'xml': 'application/xml',
    # Images
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'bmp': 'image/bmp',
    'webp': 'image/webp',
    'avif': 'image/avif',
    'ico': 'image/vnd.microsoft.icon',
    'svg': 'image/svg+xml',
    'tif': 'image/tiff',
    'tiff': 'image/tiff',
    'heic': 'image/heic',
    'heif': 'image/heif',
    'jpe': 'image/jpeg',
    'ief': 'image/ief',
    'ras': 'image/x-cmu-raster',
    'pnm': 'image/x-portable-anymap',
    'pbm': 'image/x-portable-bitmap',
    'pgm': 'image/x-portable-graymap',
    'ppm': 'image/x-portable-pixmap',
    'rgb': 'image/x-rgb',
    'xbm': 'image/x-xbitmap',
    'xpm': 'image/x-xpixmap',
    'xwd': 'image/x-xwindowdump',
    # Audio
    'mp3': 'audio/mpeg',
    'ogg': 'audio/ogg',
    'wav': 'audio/wav',
    'aac': 'audio/aac',
    'flac': 'audio/flac',
    'm4a': 'audio/mp4',
    'weba': 'audio/webm',
    'ass': 'audio/aac',
    'adts': 'audio/aac',
    'rst': 'text/x-rst',
    'loas': 'audio/aac',
    'mp2': 'audio/mpeg',
    'opus': 'audio/opus',
    'aif': 'audio/x-aiff',
    'aifc': 'audio/x-aiff',
    'aiff': 'audio/x-aiff',
    'au': 'audio/basic',
    'snd': 'audio/basic',
    'ra': 'audio/x-pn-realaudio',
    # Video
    'mp4': 'video/mp4',
    'm4v': 'video/mp4',
    'mov': 'video/quicktime',
    'avi': 'video/x-msvideo',
    'wmv': 'video/x-ms-wmv',
    'mpg': 'video/mpeg',
    'mpeg': 'video/mpeg',
    'ogv': 'video/ogg',
    'webm': 'video/webm',
    'm1v': 'video/mpeg',
    'mpa': 'video/mpeg',
    'mpe': 'video/mpeg',
    'qt': 'video/quicktime',
    'movie': 'video/x-sgi-movie',
    '3gp': 'audio/3gpp',
    '3gpp': 'audio/3gpp',
    '3g2': 'audio/3gpp2',
    '3gpp2': 'audio/3gpp2',
    # Archives / Packages
    'pdf': 'application/pdf',
    'zip': 'application/zip',
    'gz': 'application/gzip',
    'tgz': 'application/gzip',
    'tar': 'application/x-tar',
    '7z': 'application/x-7z-compressed',
    'rar': 'application/vnd.rar',
    # Additional / Binary
    'bin': 'application/octet-stream',
    'a': 'application/octet-stream',
    'so': 'application/octet-stream',
    'o': 'application/octet-stream',
    'obj': 'model/obj',
    'dll': 'application/x-msdownload',
    'exe': 'application/x-msdownload',
    # Archiving/Compression Tools
    'bcpio': 'application/x-bcpio',
    'cpio': 'application/x-cpio',
    'shar': 'application/x-shar',
    'sv4cpio': 'application/x-sv4cpio',
    'sv4crc': 'application/x-sv4crc',
    'ustar': 'application/x-ustar',
    'src': 'application/x-wais-source',
    # Office / Documents
    'doc': 'application/msword',
    'xls': 'application/vnd.ms-excel',
    'ppt': 'application/vnd.ms-powerpoint',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'dot': 'application/msword',
    'wiz': 'application/msword',
    'xlb': 'application/vnd.ms-excel',
    'pot': 'application/vnd.ms-powerpoint',
    'ppa': 'application/vnd.ms-powerpoint',
    'pps': 'application/vnd.ms-powerpoint',
    'pwz': 'application/vnd.ms-powerpoint',
    # Special Applications
    'webmanifest': 'application/manifest+json',
    'nq': 'application/n-quads',
    'nt': 'application/n-triples',
    'oda': 'application/oda',
    'p7c': 'application/pkcs7-mime',
    'ps': 'application/postscript',
    'ai': 'application/postscript',
    'eps': 'application/postscript',
    'trig': 'application/trig',
    'm3u': 'application/vnd.apple.mpegurl',
    'm3u8': 'application/vnd.apple.mpegurl',
    'wasm': 'application/wasm',
    'csh': 'application/x-csh',
    'dvi': 'application/x-dvi',
    'gtar': 'application/x-gtar',
    'hdf': 'application/x-hdf',
    'h5': 'application/x-hdf5',
    'latex': 'application/x-latex',
    'mif': 'application/x-mif',
    'cdf': 'application/x-netcdf',
    'nc': 'application/x-netcdf',
    'p12': 'application/x-pkcs12',
    'pfx': 'application/x-pkcs12',
    'ram': 'application/x-pn-realaudio',
    'pyc': 'application/x-python-code',
    'pyo': 'application/x-python-code',
    'swf': 'application/x-shockwave-flash',
    'tcl': 'application/x-tcl',
    'tex': 'application/x-tex',
    'texi': 'application/x-texinfo',
    'texinfo': 'application/x-texinfo',
    'roff': 'application/x-troff',
    't': 'application/x-troff',
    'tr': 'application/x-troff',
    'man': 'application/x-troff-man',
    'me': 'application/x-troff-me',
    'ms': 'application/x-troff-ms',
    # XML-based
    'xsl': 'application/xml',
    'rdf': 'application/xml',
    'wsdl': 'application/xml',
    'xpdl': 'application/xml',
    # ODF
    'odt': 'application/vnd.oasis.opendocument.text',
    'ods': 'application/vnd.oasis.opendocument.spreadsheet',
    'odp': 'application/vnd.oasis.opendocument.presentation',
    'odg': 'application/vnd.oasis.opendocument.graphics',
    # Fonts
    'otf': 'font/otf',
    'ttf': 'font/ttf',
    'woff': 'font/woff',
    'woff2': 'font/woff2',
    # 3D
    'gltf': 'model/gltf+json',
    'glb': 'model/gltf-binary',
    'stl': 'model/stl',
    # Scripts / Misc
    'sh': 'application/x-sh',
    'php': 'application/x-httpd-php',
    # Code files
    'py': 'text/x-python',
    'c': 'text/plain',
    'h': 'text/plain',
    'ksh': 'text/plain',
    'pl': 'text/plain',
    # Markdown / Markup
    'md': 'text/markdown',
    'markdown': 'text/markdown',
    # RDF-ish / text-ish
    'n3': 'text/n3',
    'rtx': 'text/richtext',
    'rtf': 'text/rtf',
    'srt': 'text/plain',
    'vtt': 'text/vtt',
    'etx': 'text/x-setext',
    'sgm': 'text/x-sgml',
    'sgml': 'text/x-sgml',
    'vcf': 'text/x-vcard',
    # Books
    'epub': 'application/epub+zip',
}

# Build a reverse mapping: MIME type (lowercased) -> extension (with dot)
MIME_TYPE_TO_EXTENSION: Dict[str, str] = {}
for ext, mtype in EXTENSION_TO_CONTENT_TYPE.items():
    mtype_lower = mtype.lower()
    if mtype_lower not in MIME_TYPE_TO_EXTENSION:
        MIME_TYPE_TO_EXTENSION[mtype_lower] = '.' + ext

def get_extension(mime_type: str) -> str:
    """
    Given a MIME type (Content-Type), return the corresponding file extension (with a leading dot).
    
    The function is case-insensitive. If the MIME type is unknown, an empty string is returned.
    
    Args:
        mime_type: A string representing the MIME type, e.g. 'image/jpeg'
        
    Returns:
        A string with the file extension (including the leading dot), e.g. '.jpg',
        or an empty string if the MIME type is unknown.
    """
    if not isinstance(mime_type, str) or not mime_type.strip():
        return ""
    
    # Try using the built-in mimetypes module.
    ext = mimetypes.guess_extension(mime_type.strip())
    if ext:
        return ext
    
    # Fallback to our custom mapping.
    return MIME_TYPE_TO_EXTENSION.get(mime_type.lower(), ".bin") #Fallback to bin

def get_extensions(mime_type: str) -> List[str]:
    """
    Given a MIME type, return a list of possible file extensions.
    """
    if not isinstance(mime_type, str) or not mime_type.strip():
        return []
    
    mime_type_lower = mime_type.lower().strip()
    extensions = ['.' + ext for ext, mtype in EXTENSION_TO_CONTENT_TYPE.items() if mtype.lower() == mime_type_lower]
    return extensions

# Example usage:
if __name__ == '__main__':
    test_types = [
        "application/json",
        "image/jpeg",
        "audio/aac",
        "video/mp4",
        "application/pdf",
        "unknown/type",
        "",  # Empty string
        "text/javascript",  # Multiple extensions
        "IMAGE/JPEG",  # Uppercase
        " text/html ",  # Extra spaces
    ]
    for mtype in test_types:
        print(f"{mtype} -> {get_extension(mtype)}")
        print(f"{mtype} -> {get_extensions(mtype)}")
        