# Módulo blurtstorage

Este módulo maneja el almacenamiento persistente de datos para `blurtpy`, específicamente el wallet local seguro y la configuración.

## Componentes Clave

*   **`SQLiteStore` (`sqlite.py`):** Implementa el backend de almacenamiento usando SQLite. Almacena claves privadas cifradas y pares clave-valor de configuración.
*   **`MasterPassword` (`masterpassword.py`):** Maneja el cifrado y descifrado del wallet usando una contraseña proporcionada por el usuario. Asegura que las claves privadas nunca se guarden en texto plano.
*   **`DataDir`:** Gestiona el directorio donde se guarda el archivo del wallet (`blurtpy.sqlite`) (usualmente en la carpeta de datos de aplicación del usuario).

## Nota de Seguridad

Aunque este módulo cifra tus claves, la seguridad de tu wallet depende en última instancia de la fortaleza de tu **Contraseña Maestra**. Elige siempre una contraseña fuerte y única, y mantén seguro tu archivo `blurtpy.sqlite`.
