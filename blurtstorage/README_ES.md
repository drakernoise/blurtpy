# Módulo blurtstorage

Este módulo maneja el almacenamiento persistente de datos para `blurtpy`, específicamente el wallet local seguro y la configuración.

## Descripción de Archivos

| Archivo | Descripción |
| :--- | :--- |
| `__init__.py` | Inicialización del módulo. |
| `base.py` | Clase base para implementaciones de almacenamiento. |
| `exceptions.py` | Excepciones específicas de almacenamiento (ej. `WrongMasterPasswordException`). |
| `interfaces.py` | Define las interfaces abstractas para Store, ConfigStore y KeyStore. |
| `masterpassword.py` | **Clase `MasterPassword`**: Maneja el cifrado y descifrado del wallet usando una contraseña proporcionada por el usuario. |
| `ram.py` | **Clase `RamStore`**: Una implementación de almacenamiento en memoria (no persistente), útil para pruebas. |
| `sqlite.py` | **Clase `SQLiteStore`**: El backend de almacenamiento persistente por defecto usando SQLite. Almacena claves cifradas y configuración. |

## Nota de Seguridad

Aunque este módulo cifra tus claves, la seguridad de tu wallet depende en última instancia de la fortaleza de tu **Contraseña Maestra**. Elige siempre una contraseña fuerte y única, y mantén seguro tu archivo `blurtpy.sqlite`.
