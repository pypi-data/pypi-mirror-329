# gpgdiff

A simple command-line utility for comparing two GPG keys.

## Usage

```bash
gpgdiff key1 key2 [options]
```

**Arguments:**

*   `key1`: The ID of the first GPG key.
*   `key2`: The ID of the second GPG key.

**Options:**

*   `--secret`: Compare private keys (requires appropriate permissions).
*   `--deep-analysis`: Perform a deeper analysis, including fingerprint comparison and packet analysis.

## Features

*   Compares two GPG keys using a text-based diff, highlighting differences clearly.
*   Supports comparison of both public and private keys (using the `--secret` flag).
*   Provides a rich text-based user interface (TUI) using the `rich` library for enhanced readability.
*   Offers a deep analysis option (`--deep-analysis`) for more detailed comparison, including:
    *   Fingerprint verification to confirm cryptographic identity.
    *   Packet structure analysis to compare the components of the keys.
*   Handles errors gracefully, providing informative messages to the user.
*   Uses temporary files to store exported keys, ensuring data security and preventing accidental modification of original keys.


## Installation

Install using pip:

```bash
pip install .
```

This requires Python 3.7 or higher.  The following packages are required:

*   `rich`
*   `difflib`
*   `argparse`
*   `re`
*   `subprocess`
*   `tempfile`

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

MIT License

Copyright (c) [Your Name or Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
