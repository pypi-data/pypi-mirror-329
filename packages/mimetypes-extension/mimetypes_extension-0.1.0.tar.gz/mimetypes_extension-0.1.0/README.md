---

# Mimetypes Extension 🗃️🔎

---

[![PyPI](https://img.shields.io/pypi/v/mimetypes-extension)](https://pypi.org/project/mimetypes-extension/)
[![License](https://img.shields.io/pypi/l/mimetypes-extension)](https://github.com/prono69/mimetypes-extension/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/mimetypes-extension)](https://pypi.org/project/mimetypes-extension/)

A Python package to get file extensions from MIME types, with support for additional formats not covered by Python's built-in `mimetypes` module.

---

## Features

- **Extended MIME Type Support**: Adds support for many MIME types not included in Python's standard `mimetypes` module.
- **Simple API**: Provides easy-to-use functions like `get_extension` and `get_extensions`.
- **Case Insensitive**: Handles MIME types in any case (e.g., `image/jpeg`, `IMAGE/JPEG`).
- **Multiple Extensions**: Returns all possible file extensions for a given MIME type.

---

## Installation

### You can install the package via pip:

```bash
pip install mimetypes-extension
```

---

## Usage

### Get a Single File Extension

Use `get_extension` to get the most common file extension for a given MIME type:

```python
from mime_ext import get_extension

# Get the extension for a MIME type
extension = get_extension("image/jpeg")
print(extension)  # Output: .jpg
```

### Get All File Extensions

Use `get_extensions` to get all possible file extensions for a given MIME type:

```python
from mime_ext import get_extensions

# Get all extensions for a MIME type
extensions = get_extensions("text/javascript")
print(extensions)  # Output: ['.js', '.mjs']
```

### Handle Unknown MIME Types

If the MIME type is unknown, the functions return an `.bin` as a fallback or list:

```python
unknown_extension = get_extension("unknown/type")
print(unknown_extension)  # Output: ".bin"

unknown_extensions = get_extensions("unknown/type")
print(unknown_extensions)  # Output: []
```

---

## Supported MIME Types

The package supports a wide range of MIME types, including but not limited to:

- **Text**: `text/plain`, `text/html`, `text/css`, `text/javascript`, etc.
- **Images**: `image/jpeg`, `image/png`, `image/gif`, `image/webp`, etc.
- **Audio**: `audio/mpeg`, `audio/ogg`, `audio/wav`, etc.
- **Video**: `video/mp4`, `video/quicktime`, `video/webm`, etc.
- **Archives**: `application/zip`, `application/gzip`, `application/x-tar`, etc.
- **Documents**: `application/pdf`, `application/json`, `application/xml`, etc.

For a full list of supported MIME types, check the [source code](https://github.com/prono69/mimetypes-extension/blob/main/mime_ext/core.py).

---

## Contributing

Contributions are welcome! If you'd like to add support for more MIME types or improve the package, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and write tests if applicable.
4. Submit a pull request.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Inspired by Python's built-in `mimetypes` module.
- Thanks to me only!

---

## Support

If you find this package useful, please consider giving it a ⭐️ on [GitHub](https://github.com/prono69/mimetypes-extension) or supporting the developer.

---

## Happy coding! 🚀


---
