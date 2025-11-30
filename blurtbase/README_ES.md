# Módulo blurtbase

Este módulo define las estructuras de datos fundamentales y las operaciones del protocolo de la blockchain de Blurt. Mapea objetos de Python a las estructuras binarias requeridas por la blockchain.

## Componentes Clave

*   **`operations.py`:** Contiene las definiciones de clase para todas las operaciones de la blockchain (ej. `Transfer`, `Vote`, `AccountUpdate`). Estas clases manejan la serialización de datos para la firma.
*   **`objects.py`:** Define objetos básicos de la blockchain como `Amount`, `Asset`, `PublicKey`, etc.
*   **`signedtransactions.py`:** Lógica para crear y firmar transacciones.
*   **`memo.py`:** Implementa el cifrado y descifrado de memos de transacciones.

## Uso

Este módulo es la "gramática" de la librería. Cuando llamas a `b.transfer()` en `blurtpy`, este usa `blurtbase.operations.Transfer` para crear el objeto de operación que será firmado y transmitido.
