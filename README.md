# Lyrics Tools

A set of scripts for managing lyrics files in a local music library.

## Tools

| Script               | Purpose                                                                                                                                                                                                                         |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`formatter.py`**   | Processes `.lrc` lyrics files to round 3-digit centisecond timestamps (`[01:23.456]`) down to 2-digit (`[01:23.45]`) with standard rounding, and corrects non-monotonic timestamps so they appear in strictly increasing order. |
| **`renamer.py`**     | Matches lyrics files to their corresponding music files by track number prefix (e.g., `01`, `01-02`) and renames the lyrics file to share the music file's base name.                                                           |
| **`quote_fixer.py`** | Scans file and directory names for straight single quotes (`'`) and writes the results to `straight_quotes.txt` for manual correction.                                                                                          |

## Configuration

All tools read from `config.json`:

- `directories` — list of root directories to walk
- `music_formats` — file extensions considered music files (e.g., `["mp3", "flac", "m4a"]`)
- `lyrics_formats` — file extensions considered lyrics files (e.g., `["lrc", "txt"]`)

## Usage

```bash
python formatter.py
python renamer.py
python quote_fixer.py
```

Make sure `config.json` is configured with the correct directory paths and file formats before running.
