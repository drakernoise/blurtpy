# Ejemplos de Uso de `blurtpy`

Esta carpeta contiene scripts de ejemplo para realizar tareas comunes con la librería `blurtpy`.

## Requisitos
Asegúrate de tener instalada la librería y configurada tu clave privada (WIF) en las variables de entorno o en el propio script (¡con cuidado!).

```bash
pip install blurtpy
```

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
Para ejecutar cualquiera de los scripts:

```bash
python examples/social_actions.py
```
