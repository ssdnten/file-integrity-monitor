# File Integrity Monitor

Build SHA-256 file baselines and report added, removed, and modified files without changing the monitored directory.

Educational cybersecurity portfolio project. Built with AI assistance and supplied with synthetic fixtures and automated tests. It is a learning implementation, not a production security product.

## Quick start

Requires Python 3.11 or newer. Uses only the Python standard library; no pip installation or network access is needed.

From this repository's directory:

```console
python main.py baseline samples/watched baseline.json
python main.py check samples/watched baseline.json
```

On Windows, use `py` in place of `python` if that is your installed launcher. Output is JSON on stdout. To save it, append `> report.json` in your terminal. Paths are relative to your current working directory.

## How it works

Stream each regular file through SHA-256, store relative paths, and compare dictionary key sets. Baselines are created exclusively and must sit outside the monitored root. Check exits 1 when changes exist.

## Input and example

The `samples/` directory contains the complete minimal input schema and fictional data. The checked `samples/expected-output.json` records the output of the quick-start command (for the integrity monitor, the final check command).

## Tests

```console
python -m unittest discover -s tests -v
```

Tests cover core behavior, boundary cases and invalid input. GitHub Actions is configured to run them on Windows and Ubuntu with Python 3.11–3.13; see the Actions tab for actual remote results.

## Limitations

Metadata, ACLs and timestamps are not monitored. Symlinks are skipped. Snapshots are not atomic: files can change during a scan. Protect the baseline separately; hashes do not authenticate it.

Successful analysis exits 0 unless stated otherwise above; command/input errors exit 2. Findings are not automatically remediated. Only use data you are authorized to analyze. Do not commit real credentials, customer logs or personal data.

## Learning notes

See [LEARNING_RU.md](LEARNING_RU.md) for an exercise and interview questions. Explain the algorithm, run the demo and implement an extension before presenting this as a skill you can use independently.
