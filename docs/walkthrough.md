# Walkthrough: Migración a `blurtpy`

Hemos creado con éxito una nueva librería nativa para Blurt, llamada **`blurtpy`**, derivada de `beem` pero limpiada de la deuda técnica de Steem y Hive.

## Resumen de Cambios

1.  **Nueva Estructura de Paquete:**
    -   La librería reside en la carpeta `blurtpy/`.
    -   El paquete principal se llama `blurtpy`.
    -   Subpaquetes renombrados: `blurtapi`, `blurtbase`, `blurtgraphenebase`, etc.

2.  **Limpieza de Código (The Purge):**
    -   Eliminados archivos específicos de Hive: `hive.py`, `rc.py` (Resource Credits), `community.py`.
    -   Eliminados tests irrelevantes de la suite de pruebas.
    -   Eliminadas referencias a `RC` en `account.py`.

3.  **Modernización y Refactorización (Deep Cleaning):**
    -   **DeprecationWarnings Corregidos:** Se reemplazaron todas las llamadas a `datetime.utcnow()` por `datetime.now(timezone.utc)` en todo el proyecto. La ejecución de tests ahora es limpia (0 warnings).
    -   **Renombrado de Constantes:** Se renombraron las constantes heredadas `STEEM_*` a `BLURT_*` (ej. `BLURT_100_PERCENT`) en `constants.py` y en todo el código base.

4.  **Instalación:**
    -   `setup.py` actualizado con metadatos de Blurt.
    -   Instalable vía `pip install -e .`.

## Verificación

Se ha verificado la funcionalidad principal ejecutando la suite de tests `test_account_blurt.py` contra la nueva librería.

### Resultados de Tests
```
tests/blurtpy/test_account_blurt.py::Testcases::test_account PASSED
...
tests/blurtpy/test_account_blurt.py::Testcases::test_withdraw_vesting PASSED
============================= 24 passed in 32.48s =============================
```

## Cómo Usar `blurtpy`

```python
from blurtpy import Blurt
from blurtpy.account import Account

# Conectar a Blurt
b = Blurt(node=["https://rpc.blurt.world"])

# Obtener cuenta
acc = Account("tekraze", blockchain_instance=b)
print(acc.balances)
```

## Estado Final
La librería está lista para ser usada y extendida. La deuda técnica de Steem/Hive ha sido drásticamente reducida.
