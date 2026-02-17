# Módulo blurtbase

Este módulo define las estructuras de datos fundamentales y las operaciones del protocolo de la blockchain de Blurt. Mapea objetos de Python a las estructuras binarias requeridas por la blockchain.

## Descripción de Archivos

| Archivo | Descripción |
| :--- | :--- |
| `__init__.py` | Inicialización del módulo. |
| `ledgertransactions.py` | Soporte para firmar transacciones con wallets de hardware Ledger. |
| `memo.py` | **Clase `Memo`**: Implementa el cifrado y descifrado de memos de transacciones usando secretos compartidos. |
| `objects.py` | Define objetos básicos de la blockchain como `Amount`, `Asset`, `PublicKey`, `Permission`, etc. |
| `objecttypes.py` | Enumeración de tipos de objetos usados en el protocolo Graphene (ej. `account_object`, `asset_object`). |
| `operationids.py` | Constantes que mapean nombres de operaciones a sus IDs numéricos (ej. `TRANSFER`, `VOTE`). |
| `operations.py` | **Clases de Operación**: Definiciones para todas las operaciones de la blockchain (ej. `Transfer`, `Vote`, `AccountUpdate`). Maneja la serialización. |
| `signedtransactions.py` | **Clase `SignedTransaction`**: Lógica para crear, firmar y verificar transacciones. |
| `transactions.py` | Definiciones base de transacciones. |
| `version.py` | Información de versión del módulo. |

## Uso

Este módulo es la "gramática" de la librería. Cuando llamas a `b.transfer()` en `blurtpy`, este usa `blurtbase.operations.Transfer` para crear el objeto de operación que será firmado y transmitido.
