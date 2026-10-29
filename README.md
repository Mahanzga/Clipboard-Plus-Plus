# Clipboard++

A Python desktop application that keeps track of copied text, allowing you to search, revisit, and reuse clipboard history.

## Features

- **Clipboard History** — Automatically detects copied text and stores previous entries.
- **Timestamps** — Displays when each item was copied.
- **Search** — Find previously copied text using the search bar.
- **Pinned Entries** — Pin important entries to keep them at the top of the list.
- **Quick Copy** — Double-click an entry to copy its text again.
- **Persistent Storage** — Saves clipboard history in a JSON file.
- **System Tray Integration** — Minimize the application to the system tray and restore it when needed.
- **Custom Interface** — A desktop GUI built with PyQt5.

## Technologies

- Python
- PyQt5
- Pyperclip
- JSON

## Getting Started

### Requirements

- Python
- PyQt5
- Pyperclip

### Installation

Install the required packages:

```bash
pip install PyQt5 pyperclip
```

Run the application:

```bash
python main.pyw
```

**Note:** The application currently uses local file paths that need to be configured for your environment before running it on another computer.

## About the Project

Clipboard++ is a personal project built to develop my skills in Python, GUI development, event handling, file handling, and application logic.

This project is a work in progress, with potential improvements planned as development continues.