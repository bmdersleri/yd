# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🏛️ High-Level Architecture & Data Flow

This project is an automated media processing pipeline. The core objective is to ingest a list of video URLs from a JSON file and output a set of organized, downloaded video assets. The system is designed with the Model Context Protocol (MCP) as the primary service interface.

**Data Flow:**
1.  **Input Source:** A JSON file, located at `input_urls/`, which contains one or more video URLs.
2.  **Orchestration Core:** The primary logic resides in `main_downloader.py`. This script manages the entire multi-stage process.
3.  **Processing Stages (Managed by `main_downloader.py`):**
    *   **Metadata Extraction:** Uses `yt-dlp` to gather video details from the URLs.
    *   **High-Speed Downloading:** Uses `aria2c` to efficiently download the media files.
    *   **Organization:** Moves and names the downloaded files into the final destination directory.
4.  **Tool Interface (The Goal):** The entire pipeline is being encapsulated into a single tool: `video_downloader_organizer`. This tool will expose the functionality via the MCP framework, accepting `json_file_path` and `target_directory` as its only required inputs.

## 🛠️ Development Commands & Workflow

### 🚀 Setup & Development
1.  **Environment Activation:** Always start by activating the virtual environment:
    ```bash
    source venv/bin/activate
    ```
2.  **Dependencies:** Ensure all necessary tools are installed.
    ```bash
    pip install -r requirements.txt
    # Critical external tools: yt-dlp, aria2c must be available in PATH.
    ```
3.  **Directory Structure:** Confirm the presence of these key directories:
    *   `input_urls/`: Source JSON files.
    *   `downloads/`: Temporary staging area for raw files.
    *   `organized_output/`: Final, user-facing destination.

### 🧪 Running Tests
The project structure is not fully covered by existing unit tests, but for newly added utilities or functions, writing tests in a dedicated `tests/` directory is mandatory.
*   **Running Specific Tests:** Use `pytest tests/test_module.py::test_function_name`
*   **Linting:** `black --check .`
*   **Type Checking:** `mypy .`

### 🏗️ Implementing Changes (Feature Development)
When adding new features:
1.  First, draft the change conceptually.
2.  Use the `feature-dev:feature-dev` agent to map out the necessary file changes and dependencies.
3.  Always keep the `main_downloader.py` and the MCP tool definition in sync.

## ⚠️ Important Constraints
*   **Scope Limitation:** Do not attempt to manage the *user interaction* layer (e.g., writing a web UI). Your scope is strictly confined to optimizing the *backend processing logic* callable by an LLM tool.
*   **External Dependencies:** The reliability of `yt-dlp` and `aria2c` is paramount. Any changes to the downloading process must be tested against their specific CLI options and exit codes.