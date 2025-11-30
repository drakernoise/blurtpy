# Suite de Tests Nativa de Blurtpy

Este directorio contiene la **Suite de Tests Nativa** para `blurtpy`, diseñada para verificar la funcionalidad principal, seguridad y estabilidad de la librería contra la blockchain de Blurt.

## 📂 Estructura

*   **`test_native_blurt.py`**: El archivo principal que contiene todos los casos de prueba. Utiliza `unittest` y `pytest`.

## 🧪 ¿Qué se Prueba?

La suite cubre 11 escenarios críticos para asegurar que la librería funcione como se espera:

### 1. Conectividad y Básicos
*   **`test_01_connection_and_props`**: Verifica la conexión a múltiples nodos RPC (failover) y obtiene propiedades de la blockchain (Bloque actual).

### 2. Datos de Cuenta
*   **`test_02_account_fetch_integrity`**: Obtiene una cuenta real (`draktest`) y verifica los tipos de datos (ej. los Balances son objetos `Amount`).
*   **`test_03_account_not_found`**: Asegura que la librería lance la excepción correcta `AccountDoesNotExistsException` para cuentas inexistentes.
*   **`test_06_history_resilience`**: Obtiene el historial de la cuenta para verificar el manejo de respuestas de la API y la paginación.

### 3. Seguridad y Criptografía (Dry-Run)
*   **`test_04_transaction_signing`**: Firma una transacción de transferencia usando la Active Key. **Crucial:** Usa `nobroadcast=True` para verificar la firma *sin* gastar fondos.
*   **`test_05_missing_key_protection`**: Confirma que las operaciones que requieren una clave fallen de forma segura (`MissingKeyError` o `WalletLocked`) si la clave no está presente.
*   **`test_07_memo_encryption`**: Prueba el cifrado y descifrado AES de Memos usando claves efímeras (simulando Emisor y Receptor).

### 4. Operaciones (Dry-Run)
Estos tests construyen y firman operaciones complejas para asegurar que la librería genere transacciones válidas:
*   **`test_08_power_up_dry_run`**: Transferencia a Vesting (Power Up).
*   **`test_09_claim_rewards_dry_run`**: Reclamar Recompensas.
*   **`test_10_vote_operation_dry_run`**: Votar en un post.

### 5. Validación de Entradas y Robustez
*   **`test_11_input_validation`**: Verifica que la librería rechace entradas inválidas o maliciosas, como:
    *   Montos de transferencia negativos (lanza `ValueError`).
    *   Símbolos de activos inválidos (lanza `AssetDoesNotExistsException`).

> **🛡️ Nota sobre Seguridad:** Todos los tests de transacciones están configurados como **Dry-Runs** (`nobroadcast=True`). Generan y firman la transacción para probar la corrección criptográfica pero **NO** la transmiten a la red. No se gastan fondos.

## ⚙️ Configuración

Los tests usan una cuenta por defecto (`draktest`) y una Active Key pública para verificación. **Puedes (y deberías) editar estos valores** en `tests/test_native_blurt.py` para probar con tu propia cuenta o verificar diferentes permisos.

Busca estas constantes al inicio del archivo:

```python
# User provided key for 'draktest'
ACTIVE_KEY = "5K8sEXDvidZijhKpYDyWxyKSP22T3UdU8276YEsmcDgwbmgRS6K"
ACCOUNT_NAME = "draktest"
```

## 🚀 Cómo Ejecutar los Tests

Necesitas tener `pytest` instalado. Ejecuta el siguiente comando desde la raíz del proyecto:

```bash
pytest tests/test_native_blurt.py
```

### Salida Detallada (Verbose)
Para ver logs detallados (incluyendo pasos de conexión y detalles de transacciones):

```bash
pytest tests/test_native_blurt.py -v
```
