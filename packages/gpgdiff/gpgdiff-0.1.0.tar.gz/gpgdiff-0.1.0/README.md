# GPG Command Prompter | rofi / fzf launcher


<a href="https://www.buymeacoffee.com/ubuntupunk" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>


This project provides two helpers to access to **GPG commands** and **shortcuts** via an **interactive manual** extracted from the official GnuGPG manul. 40 commands are made available from the GPG code-base in this way, allowing users to reference and learn the craft of GPG. Using the helpers may assist those wanting to learn more about GPG. This version is for posix-compliant systems that are able to install fzf/rofi, a seperate ulauncher extension is also available.

## Versions

There are two versions to suit different user preferences:

1. **CLI Version**: Ideal for users who prefer interacting through the command line.
2. **Rofi Popup Version**: Designed for users who prefer a graphical interface, providing a visually appealing and intuitive experience, great for tiling window managers like [i3](https://i3wm.org/) and [bspwm](https://github.com/baskerville/bspwm).

## Usage

| Keyword        | Description                                                                    | Example     |
| -------------- | ------------------------------------------------------------------------------ | ----------- |
| `fzf-gpg` | Search for gpg**commands** and **shortcuts** for a given `query` | enter to open GPG Manual |
| `rofi-gpg` | Search for gog**commands** and **shortcuts** for a given `query` | enter to open GPG Manual |

## Features

* Search for GPG Commands either by their description or their Hotkey.
* Hitting enter on a command will redirect to [GPG Manual](gpg.md) on the same command.

## Disclaimer
* This project is not related to the GnuPG Project and does not make any claims about the GPG software.
* Since the Commands Database and its description fragments have not been fully tested and validated, they may not be functional, please report any issue here if any don't map the GnuPGP official manual.
* If you have issues with GnuPG (GPG) please report that via the official GPG channels.

## Installation

### Manual Installation

* Download the [Latest Release](https://github.com/ubuntpunk/gpg-prompt/releases/latest)
* Extract the archive and copy the files to `~/.local/share/gpg-prompt`

### System requirements
- Rofi
- Fzf

### Recommended Installation

```python
pip install gpg-prompt
```
### Install Helpers for Ubuntu/Debian

```bash
sudo apt install rofi fzf
```

### Operation
`fzf-gpg`  `# Uses fzf interface`

`rofi-gpg`  `# Uses rofi interface`



