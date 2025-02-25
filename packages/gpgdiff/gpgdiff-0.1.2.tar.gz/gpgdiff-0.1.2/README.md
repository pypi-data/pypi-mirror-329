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
pip install gpgdiff
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

[GPL License](LICENSE)