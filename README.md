# Macaroni Workspace

A modern fullscreen productivity workspace built with Python and PyQt6.
Macaroni Workspace combines a rich text editor, persistent browser session, workspace history, autosave, and lightweight telemetry into a clean developer-focused desktop environment.

## Overview

Macaroni Workspace is designed as a unified thinking environment for:

* Writing notes
* Managing prompts
* Coding
* Research workflows
* AI-assisted work
* Persistent browser-based sessions

The application ships with:

* A live editor panel
* Embedded web browser
* Workspace file history
* Session persistence
* Health metrics export
* Dark modern UI
* Fullscreen distraction-free workflow

---

# Features

## Workspace Sidebar

* Searchable recent file history
* Instant file reopening
* Persistent workspace state
* Fast filtering system

## Rich Text Editor

* Full QTextEdit integration
* Autosave support
* Large clean writing surface
* Markdown and plain text support
* UTF-8 compatible

## Embedded Browser

* Persistent browser profile
* Local storage enabled
* Cookies preserved between sessions
* JavaScript + plugin support
* Fullscreen optimized browsing

Default launch page:

```python
https://chat.com
```

## Session Persistence

Macaroni Workspace automatically restores:

* Open editor content
* Browser session URL
* File history
* Split panel sizes
* Current active file

Saved into:

```bash
sessions.json
```

## Health Metrics Export

The application continuously exports operational metrics including:

* App launches
* Browser URL
* Editor character count
* Uptime
* Theme state
* Last updated timestamp

Saved into:

```bash
health.json
```

---

# Tech Stack

* Python 3
* PyQt6
* Qt WebEngine

Core modules used:

```python
PyQt6.QtWidgets
PyQt6.QtGui
PyQt6.QtCore
PyQt6.QtWebEngineWidgets
PyQt6.QtWebEngineCore
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/mule-codex/macaroni-workspace.git
cd macaroni-workspace
```

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install PyQt6 PyQt6-WebEngine
```

---

# Running The Application

```bash
python main.py
```

The workspace launches in fullscreen mode automatically.

---

# Project Structure

```bash
macaroni-workspace/
│
├── main.py
├── sessions.json
├── health.json
├── browser_profile/
│   └── cache/
└── README.md
```

---

# Core Architecture

## Main Window

The application is built around:

```python
class MacaroniIDE(QMainWindow)
```

This class controls:

* UI layout
* Browser state
* Editor state
* Session management
* File operations
* Health telemetry

---

# Key Components

## Sidebar

```python
QListWidget
QLineEdit
```

Provides:

* File history
* Search filtering
* Workspace navigation

---

## Editor

```python
QTextEdit
```

Handles:

* Writing
* Editing
* Autosave
* Session recovery

---

## Browser Engine

```python
QWebEngineView
QWebEngineProfile
QWebEnginePage
```

Supports:

* Persistent cookies
* Local storage
* Cached sessions
* Modern web rendering

---

# Autosave System

Triggered automatically when:

* Editor content changes
* Browser URL changes
* Workspace state changes

Data persisted through:

```python
auto_save_session()
```

---

# Health Monitoring

Telemetry export runs every:

```python
5000 ms
```

Using:

```python
QTimer
```

Metrics exported via:

```python
export_health_metrics()
```

---

# UI Design

Macaroni Workspace uses a custom dark Fusion theme with:

* Minimal chrome
* Rounded panels
* Clean typography
* Developer-first layout
* High readability contrast

Primary palette:

```text
Background: #0b0b0c
Panel: #161616
Accent: #d1d5db
Text: #f5f5f5
```

---

# Current Capabilities

* Open files
* Save files
* Save As
* Session recovery
* Browser persistence
* File history management
* Workspace search
* Fullscreen workflow
* Health exports

---

# Future Improvements

Potential roadmap ideas:

* Multi-tab editing
* Markdown preview
* AI command palette
* Integrated terminal
* Git support
* Plugin architecture
* Cloud sync
* Workspace snapshots
* Local vector search
* Prompt library system

---

# Example Use Cases

## AI Research Workspace

Use the editor alongside the embedded browser for:

* Prompt engineering
* Long-form thinking
* AI chats
* Research synthesis

## Coding Companion

* Keep docs open in-browser
* Write snippets in-editor
* Persist workflows automatically

## Writing Environment

* Distraction-free fullscreen layout
* Persistent drafts
* Instant recovery after restart

---

# Security Notes

* Browser data is stored locally
* Sessions are persisted to disk
* No encryption layer is currently implemented
* Local files are accessed directly from the filesystem

---

# License

MIT License

---

# Author Raymond Simba
