# Guía de Instalación

Esta guía proporciona instrucciones detalladas para instalar `blurtpy` en Windows, Linux y macOS.

## Requisitos Previos
*   **Python 3.8** o superior.
*   **Git** (para clonar el repositorio).

---

## 🪟 Windows

1.  **Instalar Python:**
    *   Descarga e instala Python desde [python.org](https://www.python.org/downloads/windows/).
    *   **Importante:** Marca la casilla **"Add Python to PATH"** durante la instalación.

2.  **Clonar el Repositorio:**
    Abre el Símbolo del Sistema (cmd) o PowerShell y ejecuta:
    ```powershell
    git clone https://gitlab.com/tu-usuario/blurtpy.git
    cd blurtpy
    ```

3.  **Crear un Entorno Virtual (Recomendado):**
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```
    *(Verás `(venv)` al inicio de tu línea de comandos)*

4.  **Instalar blurtpy:**
    ```powershell
    pip install -e .
    ```

---

## 🐧 Linux (Ubuntu/Debian)

1.  **Instalar Dependencias del Sistema:**
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip python3-venv git build-essential libssl-dev libffi-dev python3-dev
    ```

2.  **Clonar el Repositorio:**
    ```bash
    git clone https://gitlab.com/tu-usuario/blurtpy.git
    cd blurtpy
    ```

3.  **Crear un Entorno Virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Instalar blurtpy:**
    ```bash
    pip install -e .
    ```

---

## 🍎 macOS

1.  **Instalar Dependencias (vía Homebrew):**
    Si no tienes Homebrew, instálalo desde [brew.sh](https://brew.sh).
    ```bash
    brew install python git
    ```

2.  **Clonar el Repositorio:**
    ```bash
    git clone https://gitlab.com/tu-usuario/blurtpy.git
    cd blurtpy
    ```

3.  **Crear un Entorno Virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Instalar blurtpy:**
    ```bash
    pip install -e .
    ```

---

## ⚡ Opcional: Firma Rápida (secp256k1)

Para una firma de transacciones más rápida, puedes instalar la extensión en C `secp256k1prp`.

**Windows:**
Generalmente se instala automáticamente si hay "wheels" disponibles. Si no, podrías necesitar "Visual Studio Build Tools".
```powershell
pip install secp256k1prp
```

**Linux/macOS:**
Asegúrate de tener las herramientas de compilación instaladas (gcc, automake).
```bash
pip install secp256k1prp
```
