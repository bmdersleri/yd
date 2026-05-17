## 🚀 Project Handoff Documentation

This project is an automation system designed to process a list of video URLs, extract video metadata, download the videos at high speed, and organize the downloaded files into a designated target folder.

---

### 🎯 Project Goal

The ultimate goal is to enable a user to process video links from a JSON file through a single interface (Model Context Protocol - MCP); ensuring that the core steps of downloading, metadata extraction, and organization are managed seamlessly.

### ✅ Current Status Summary

1.  **Architectural Design:** A stable download pipeline has been designed using robust tools like `yt-dlp` and `aria2c`.
2.  **Code Structure:** The main orchestration logic (e.g., `main_downloader.py`) is defined to manage all steps.
3.  **Data Flow:** The data flow (JSON $\rightarrow$ Link List $\rightarrow$ Downloading $\rightarrow$ Organizing) is logically complete.
4.  **Environment Setup:** The project directory structure has been established and the virtual environment (venv) is ready.

### 🛠️ Setup Instructions (For a New Session)

When starting a new session, the following steps must be followed:

1.  **Activate the Environment:**
    ```bash
    source venv/bin/activate
    ```
2.  **Install Dependencies:** (Ensure all required libraries are installed.)
    ```bash
    pip install -r requirements.txt # If requirements.txt exists
    # or manual dependencies:
    # pip install yt-dlp aria2
    ```
3.  **Directory Check:** Ensure the project contains the following basic directories:
    *   `input_urls/`: Directory containing JSON files with URLs to be processed.
    *   `downloads/`: Temporary storage area for raw downloaded files.
    *   `organized_output/`: Destination directory for the final, organized files presented to the user.

### ⏭️ Next Steps (Task Workflow)

The project is currently paused at the following stage: **The core logic is complete, but this logic has not yet been packaged as a tool for an LLM.**

**The Priority Task:**
Create a function that wraps (wraps) all the downloading and organizational logic from `main_downloader.py` within a **Model Context Protocol (MCP) Server** framework.

**Target Tool Definition:**
*   **Tool Name:** `video_downloader_organizer`
*   **Description:** "Takes a list of video URLs from a given JSON file, extracts video metadata from these URLs, downloads the videos at high speed, and organizes the files into a specified target directory after completion."
*   **Parameters:**
    *   `json_file_path` (string): The path to the JSON file containing the URLs.
    *   `target_directory` (string): The target folder path where the downloaded files should be moved.

Upon completing these steps, the project will be transformed into a fully functional, callable tool for the LLM.

---
**Note:** Please ensure you continue working within the `(venv)` environment at all times.