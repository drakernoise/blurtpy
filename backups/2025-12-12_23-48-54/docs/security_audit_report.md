# Reporte de Auditoría de Seguridad - Blurtpy

**Fecha:** 30 de Noviembre de 2025
**Estado:** Completado
**Resultado:** Seguro (tras correcciones)

## Resumen Ejecutivo

Se realizó una auditoría de seguridad exhaustiva sobre la librería `blurtpy`, enfocándose en el manejo de claves privadas, criptografía, almacenamiento de billetera y dependencias.

**Hallazgo Crítico:** Se descubrió que la representación de depuración (`__repr__`) de la clase `PrivateKey` exponía la clave privada en texto plano (hexadecimal). Esto fue corregido inmediatamente.

**Estado Actual:** Todas las vulnerabilidades identificadas han sido corregidas y verificadas mediante nuevos tests de seguridad.

## Detalle de Hallazgos y Correcciones

### 1. Exposición de Clave Privada (CRÍTICO)
*   **Problema:** `PrivateKey.__repr__` devolvía la clave privada en formato hexadecimal. Cualquier log de error o impresión de depuración podría filtrar la clave.
*   **Corrección:** Se modificó `blurtgraphenebase/account.py` para redactar la salida de `__repr__` a `<PrivateKey: ...>`.
*   **Impacto Colateral:** La corrección rompió funciones internas que dependían inseguramente de `repr()` para obtener la clave (firma en `ecdsasig.py`, derivación en `account.py`, encriptación en `bip38.py`).
*   **Resolución:** Se refactorizaron todos los componentes afectados para usar métodos seguros (`bytes()`, `hexlify()`) en lugar de `repr()`.
*   **Verificación:** `tests/test_audit_keys.py` (Pasa).

### 2. Criptografía (ECDSA & RFC6979)
*   **Curva:** Se verificó el uso de `SECP256k1`.
*   **Determinismo:**
    *   Backends `secp256k1` (C-lib) y `cryptography` son generalmente deterministas (RFC6979).
    *   Backend `ecdsa` (Python puro) añade entropía basada en tiempo (`time.time()`) para evitar ataques de reuso de `k`. Esto es seguro pero no determinista.
*   **Verificación:** `tests/test_audit_crypto.py` confirma que las firmas son válidas y recuperables.

### 3. Almacenamiento de Billetera
*   **Mecanismo:** `SqliteEncryptedKeyStore` utiliza `MasterPassword`.
*   **Encriptación:**
    *   Las claves privadas se encriptan usando **BIP38** (AES-256) antes de guardarse en SQLite.
    *   La clave maestra se encripta con la contraseña del usuario (AES-256).
*   **Verificación:** `tests/test_audit_wallet.py` confirma que las claves en la base de datos están encriptadas (empiezan con `6P`) y no en texto plano.

### 4. Dependencias
*   **Estado:** Las versiones instaladas son seguras y recientes.
    *   `ecdsa`: 0.18.0 (Seguro >= 0.13)
    *   `cryptography`: 46.0.3 (Seguro)
    *   `requests`: 2.31.0 (Seguro)
*   **Recomendación:** Se recomienda fijar estas versiones mínimas en `setup.py` para evitar regresiones futuras.
*   **Verificación:** `tests/test_audit_dependencies.py` (Pasa).

## Conclusión

La librería `blurtpy` ahora cuenta con mecanismos robustos para proteger las claves privadas. La vulnerabilidad de exposición en logs ha sido eliminada y se han añadido tests de regresión para asegurar que no vuelva a ocurrir.
