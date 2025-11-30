# Installation Guide

This guide provides detailed instructions for installing `blurtpy` on Windows, Linux, and macOS.

## Prerequisites
*   **Python 3.8** or higher.
*   **Git** (to clone the repository).

---

## 🪟 Windows

1.  **Install Python:**
    *   Download and install Python from [python.org](https://www.python.org/downloads/windows/).
    *   **Important:** Check the box **"Add Python to PATH"** during installation.

2.  **Clone the Repository:**
    Open Command Prompt (cmd) or PowerShell and run:
    ```powershell
    git clone https://gitlab.com/your-username/blurtpy.git
    cd blurtpy
    ```

3.  **Create a Virtual Environment (Recommended):**
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```
    *(You will see `(venv)` at the start of your command line)*

4.  **Install blurtpy:**
    ```powershell
    pip install -e .
    ```

---

## 🐧 Linux (Ubuntu/Debian)

1.  **Install System Dependencies:**
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip python3-venv git build-essential libssl-dev libffi-dev python3-dev
    ```

2.  **Clone the Repository:**
    ```bash
    git clone https://gitlab.com/your-username/blurtpy.git
    cd blurtpy
    ```

3.  **Create a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install blurtpy:**
    ```bash
    pip install -e .
    ```

---

## 🍎 macOS

1.  **Install Dependencies (via Homebrew):**
    If you don't have Homebrew, install it from [brew.sh](https://brew.sh).
    ```bash
    brew install python git
    ```

2.  **Clone the Repository:**
    ```bash
    git clone https://gitlab.com/your-username/blurtpy.git
    cd blurtpy
    ```

3.  **Create a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install blurtpy:**
    ```bash
    pip install -e .
    ```

---

## ⚡ Optional: Fast Signing (secp256k1)

For faster transaction signing, you can install the C-extension `secp256k1prp`.

**Windows:**
Usually installs automatically if wheels are available. If not, you may need "Visual Studio Build Tools".
```powershell
pip install secp256k1prp
```

**Linux/macOS:**
Ensure you have build tools installed (gcc, automake).
```bash
pip install secp256k1prp
```
