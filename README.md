# TikTok Username Checker — Termux

Android/Termux adaptation of the original TikTok Username Checker.

This fork is adapted for Termux and includes:

- Android/Termux-compatible checking
- Ctrl+C stopping
- Resumable progress with `output/progress.txt`
- Candidate results in `output/available_usernames.txt`
- Username generation
- Optional display of unavailable usernames
- Android-friendly file handling

## Requirements

- Android
- Termux
- Python 3

## Installation

```bash
pkg update
pkg install python
termux-setup-storage
pip install -r requirements.txt
```

## Start

```bash
python main.py
```

Choose:

```text
[1] Start the TikTok Username Checker
[2] Username Generator
[3] Clear 'usernames.txt' and cache
[4] Exit
```

When checking usernames, you can choose whether unavailable usernames are displayed.

Progress is saved automatically. If Termux is interrupted, run the program again and it will resume from the saved position.

## Output

- `output/usernames.txt` — usernames to check
- `output/available_usernames.txt` — usernames classified by the checker as `Available/Banned`
- `output/progress.txt` — saved checking position

## Original project

This is a fork/adaptation of the original project by mdevio.

The original MIT license and copyright notice are preserved in `LICENSE`.

## License

MIT License. See `LICENSE`.
