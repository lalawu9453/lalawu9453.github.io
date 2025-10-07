# AnyThreads

[中文版](README.md)

A highly automated blog content engine powered by Hugo and assisted by AI.

---

## About The Project

![](./branner.jpg)

This project aims to build a deluxe, highly automated, SEO-friendly blog. It's not just a content publishing platform, but a "Content Engine" that can continuously expand its content, improve site authority, and drive traffic through AI assistance and automated workflows.

### Key Features

- **Efficient Content Management**: Uses Hugo for extremely fast static site generation.
- **AI-Assisted Tagging**: Includes a built-in Python script that can automatically scan articles and suggest, enhance, and manage tags via AI.
- **Customized UI/UX**: Features a unique ambient sound control bar and has undergone a first-pass optimization for fonts, colors, and layout to improve the reading experience.
- **Versioned Development Environment**: Uses `uv` for Python environment and dependency management to ensure consistency.

## Technology Stack

- **Static Site Generation**: Hugo
- **Scripting & Automation**: Python 3
- **Python Environment**: uv
- **Theme**: loficode (with customizations)

## Getting Started

Follow these steps to set up and run the project on your local machine.

### 1. Prerequisites

Make sure you have the following software installed:
- [Git](https://git-scm.com/)
- [Hugo (extended version)](https://gohugo.io/installation/)
- [uv (Python package installer)](https://github.com/astral-sh/uv)

### 2. Project Initialization

```bash
# 1. Clone the project locally
git clone <repository-url>
cd ai-reporter

# 2. Initialize and pull the Hugo theme (if it was a submodule)
# This step might not be needed if theme files are already committed.
git submodule update --init --recursive

# 3. Sync the Python development environment
# (uv will automatically detect uv.lock and install all necessary Python libraries)
uv sync
```

### 3. Running the Local Server

After initialization, run the following command to start Hugo's local development server:

```bash
# The -D flag will also build draft pages
hugo server -D
```

Once the server is running, you can open `http://localhost:1313/` in your browser to see the site.

## Usage

### AI Tag Processor

This project includes a Python script for managing post tags. You can run it with the following command:

```bash
# The script will automatically scan posts, suggest tags, and update files
uv run python scripts/tag_processor.py
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
