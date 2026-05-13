# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Standalone Python scripts for managing lyrics files and file naming. No package manager, no virtualenv, no tests — just run the scripts directly with `python <script>.py`.

## Scripts

- **`formatter.py`** — Walks directories from `config.json`, opens every `.lrc` file, rounds 3-digit centisecond timestamps (`[01:23.456]`) down to 2-digit (`[01:23.45]`) with standard rounding, and enforces monotonically increasing timestamps (later timestamps cannot be earlier than prior ones). Only writes back if changes were made.

- **`renamer.py`** — Walks directories from `config.json`, matches lyrics files to music files by track number prefix (e.g., `01` or `01-02`), and renames lyrics files to share the music file's base name (keeping the lyrics extension).

- **`quote_fixer.py`** — Walks directories from `config.json`, scans file and directory names for straight single quotes (`'`, U+0027) and writes paths to `straight_quotes.txt` for manual review.

## Configuration

`config.json` drives both scripts:

- `directories` — list of root directories to walk
- `music_formats` — file extensions considered music files (e.g., `["mp3", "flac", "m4a"]`)
- `lyrics_formats` — file extensions considered lyrics files (e.g., `["lrc", "txt"]`)

## Running

```bash
python formatter.py
python renamer.py
python quote_fixer.py
```

All scripts read `config.json` from the current working directory and print summary statistics on completion.
