#!/usr/bin/env python3

import subprocess
import sys
import tempfile
import difflib
import argparse
import re
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

console = Console()

def get_unique_key_id(key_id):
    """Ensure the key_id uniquely identifies a single key."""
    try:
        result = subprocess.run(
            ["gpg", "--list-keys", "--with-colons", key_id],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError:
        raise ValueError(f"[red]Error listing keys for {key_id}[/red]")

    lines = result.stdout.splitlines()
    pub_lines = [line for line in lines if line.startswith("pub:")]

    if len(pub_lines) == 0:
        raise ValueError(f"[red]No key found for {key_id}[/red]")
    elif len(pub_lines) > 1:
        raise ValueError(f"[red]Multiple keys found for {key_id}. Please specify a unique key ID.[/red]")
    else:
        fields = pub_lines[0].split(":")
        return fields[4]

def export_gpg_key(key_id, filename, secret=False):
    cmd = ["gpg", "--export-secret-keys" if secret else "--export", "--armor", key_id]
    try:
        with open(filename, "w") as f:
            subprocess.run(cmd, stdout=f, text=True, check=True)
    except subprocess.CalledProcessError:
        console.print(f"[red]Error: Failed to export key {key_id}[/red]")
        sys.exit(1)

def diff_keys(file1, file2):
    with open(file1, "r") as f1, open(file2, "r") as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
    diff = difflib.unified_diff(lines1, lines2, fromfile=file1, tofile=file2)
    diff_output = ''.join([f"[green]{line}[/green]" if line.startswith('+') else f"[red]{line}[/red]" if line.startswith('-') else line for line in diff])
    return diff_output

def get_fingerprint(key_id):
    try:
        result = subprocess.run(
            ["gpg", "--fingerprint", key_id],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.splitlines():
            if "fingerprint" in line.lower():
                return re.sub(r"\s+", "", line.split("=", 1)[1].strip())
        raise ValueError("Fingerprint not found")
    except subprocess.CalledProcessError:
        raise ValueError(f"[red]Error getting fingerprint for {key_id}[/red]")

def analyze_packets(file_path):
    try:
        result = subprocess.run(
            ["gpg", "--list-packets", file_path],
            capture_output=True,
            text=True,
            check=True
        )
        packets = result.stdout
        public_keys = packets.count("public key packet")
        subkeys = packets.count("public subkey packet")
        user_ids = packets.count("user ID packet")
        signatures = packets.count("signature packet")
        return {
            "Public Keys": public_keys,
            "Subkeys": subkeys,
            "User IDs": user_ids,
            "Signatures": signatures
        }
    except subprocess.CalledProcessError:
        console.print(f"[red]Error analyzing packets for {file_path}[/red]")
        return None

def main():
    parser = argparse.ArgumentParser(description="Compare two GPG keys (TUI).")
    parser.add_argument("key1", help="First GPG key ID")
    parser.add_argument("key2", help="Second GPG key ID")
    parser.add_argument("--secret", action="store_true", help="Compare private keys")
    parser.add_argument("--deep-analysis", action="store_true", help="Perform deeper analysis")
    args = parser.parse_args()

    try:
        unique_key1 = get_unique_key_id(args.key1)
        unique_key2 = get_unique_key_id(args.key2)
    except ValueError as e:
        rprint(e)
        sys.exit(1)

    with tempfile.NamedTemporaryFile(delete=False) as tmp1, tempfile.NamedTemporaryFile(delete=False) as tmp2:
        export_gpg_key(unique_key1, tmp1.name, args.secret)
        export_gpg_key(unique_key2, tmp2.name, args.secret)
        diff_result = diff_keys(tmp1.name, tmp2.name)

        if not diff_result:
            rprint(Panel("[green]The keys are identical based on their exported content.[/green]", title="Result"))
        else:
            rprint(Panel("[yellow]The keys are different.[/yellow]", title="Result"))
            rprint("[yellow]Differences in exported content:[/yellow]")
            rprint(diff_result)
            rprint("[yellow]Note: Differences may include metadata but not necessarily the cryptographic material.[/yellow]")

    if args.deep_analysis:
        rprint(Panel("[blue]Performing deeper analysis...[/blue]", title="Deeper Analysis"))
        try:
            fp1 = get_fingerprint(unique_key1)
            fp2 = get_fingerprint(unique_key2)
            table = Table(title="Fingerprints")
            table.add_column("Key", style="cyan")
            table.add_column("Fingerprint", style="magenta")
            table.add_row(args.key1, fp1)
            table.add_row(args.key2, fp2)
            rprint(table)
            if fp1 == fp2:
                rprint("[green]Fingerprints match: The keys are cryptographically identical.[/green]")
            else:
                rprint("[red]Fingerprints differ: The keys are distinct and represent different identities.[/red]")
        except ValueError as e:
            rprint(e)
            rprint("[yellow]Falling back to packet analysis...[/yellow]")
            packets1 = analyze_packets(tmp1.name)
            packets2 = analyze_packets(tmp2.name)
            if packets1 and packets2:
                packet_table = Table(title="Packet Analysis")
                packet_table.add_column("Component", style="cyan")
                packet_table.add_column(args.key1, style="magenta")
                packet_table.add_column(args.key2, style="magenta")
                for component in packets1:
                    val1 = packets1.get(component, 0)
                    val2 = packets2.get(component, 0)
                    packet_table.add_row(component, str(val1), str(val2))
                rprint(packet_table)
                if packets1 == packets2:
                    rprint("[green]Packet structures are identical.[/green]")
                else:
                    rprint("[red]Packet structures differ.[/red]")

if __name__ == "__main__":
    main()
