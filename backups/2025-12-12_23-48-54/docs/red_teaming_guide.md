# Guía de Red Teaming para Blurtpy

Esta guía describe cómo realizar pruebas de seguridad ofensiva ("Red Teaming") contra la librería `blurtpy` de manera ética y efectiva.

**Objetivo:** Encontrar vulnerabilidades en el código del *cliente* (la librería), no en los nodos de la red.

## ¿Por qué atacar la librería?
Atacar un nodo público es ilegal y dañino. Sin embargo, atacar tu propia librería es vital para asegurar que:
1.  No crashee ante datos malformados.
2.  No filtre claves privadas.
3.  No firme transacciones manipuladas.

## Vectores de Ataque (Client-Side)

### 1. Fuzzing de Entradas
Enviar datos aleatorios o malformados a las funciones críticas para provocar fallos.

**Ejemplo:**
```python
from blurtpy.amount import Amount
# Intentar desbordar el parser de cantidades
try:
    a = Amount("999999999999999999999999999.999999999 BLURT")
except Exception as e:
    print(f"Capturado: {e}")
```

### 2. Mocking de Nodos Maliciosos (Man-in-the-Middle Simulado)
Simular que el nodo devuelve datos corruptos o maliciosos para ver si la librería los procesa ciegamente.

**Estrategia:**
Usar `unittest.mock` para interceptar las llamadas RPC y devolver JSONs manipulados.

**Escenario de Ataque:**
*   El nodo devuelve un historial de operaciones con campos extraños.
*   El nodo devuelve un bloque con una fecha en el futuro lejano.
*   El nodo devuelve un ID de transacción falso.

### 3. Ataques de Dependencias
Verificar si las librerías que usamos (`requests`, `ecdsa`) tienen vulnerabilidades conocidas.
*   **Herramienta:** `pip-audit` o `safety`.

### 4. Pruebas de Fuga de Memoria / Claves
Intentar recuperar claves privadas de la memoria RAM o del disco después de "borrarlas".

**Prueba:**
1.  Crear una billetera y borrar una clave.
2.  Inspeccionar el archivo `.sqlite` crudo para ver si quedan trazas.
3.  (Ya cubierto parcialmente por `test_audit_wallet.py`).

## Cómo ejecutar tus propias pruebas
Puedes crear scripts en la carpeta `tests/red_team/` (creala si no existe) y usar el framework de pruebas existente.

**Ejemplo de Script de Ataque (`tests/red_team/attack_amount.py`):**
```python
import unittest
from blurtpy.amount import Amount

class TestAmountFuzzing(unittest.TestCase):
    def test_overflow(self):
        # Intentar causar un MemoryError o OverflowError
        huge_str = "1" * 10000 + " BLURT"
        with self.assertRaises(ValueError):
            Amount(huge_str)
```
