# Ejemplos de Uso de `blurtpy`

Esta carpeta contiene scripts de ejemplo para realizar tareas comunes con la librería `blurtpy`.

## Requisitos
Asegúrate de tener instalada la librería y configurada tu clave privada (WIF) en las variables de entorno o en el propio script (¡con cuidado!).

```bash
pip install blurtpy
```

## Configuración Inicial (¡IMPORTANTE!)

Antes de ejecutar los ejemplos, debes configurar tu **Wallet Seguro**. Esto creará una base de datos local cifrada (`blurtpy.sqlite`) para almacenar tus claves privadas, evitando tener que escribirlas en el código.

1.  Ejecuta el script de configuración:
    ```bash
    python examples/secure_wallet_setup.py
    ```
2.  Sigue las instrucciones para crear una contraseña maestra y añadir tus claves (WIF).

## Índice de Ejemplos

### 1. Interacción Social (`social_actions.py`)
-   Comentar en un post.
-   Contar comentarios y listar autores.
-   Votar comentarios.
-   Encontrar el último post de un usuario.
-   Buscar posts recientes por criterios (tags).

### 2. Gestión de Fondos (`wallet_actions.py`)
-   Power Up (Transfer to Vesting).
-   Delegar Blurt Power (BP).
-   Transferencia múltiple (batch).
-   Transferencia recurrente (ejemplo de lógica).
-   Transferir a Ahorros (Savings).

### 3. Gestión de Cuenta (`account_management.py`)
-   Establecer cuenta de recuperación.
-   Cambiar claves de la cuenta.

## Ejecución
Para ejecutar cualquiera de los scripts (te pedirá la contraseña del wallet):

```bash
python examples/social_actions.py
```

## Optimización de Nodos
La librería incluye una función para encontrar automáticamente el nodo más rápido. Puedes usarla en tus propios scripts así:

```python
from blurtpy import Blurt
# Se conectará automáticamente al nodo con menor latencia
b = Blurt(node="best")
```
