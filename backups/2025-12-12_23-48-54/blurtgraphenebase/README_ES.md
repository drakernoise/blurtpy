# Módulo blurtgraphenebase

Este módulo contiene las primitivas criptográficas de bajo nivel, utilidades de codificación y tipos de datos que forman la base del protocolo Blurt. Maneja los "tuercas y tornillos" de la interacción con la blockchain.

## Descripción de Archivos

| Archivo | Descripción |
| :--- | :--- |
| `__init__.py` | Inicialización del módulo. |
| `account.py` | **`PasswordKey` / `BrainKey`**: Utilidades para generar claves desde contraseñas o brain keys (mnemónicos). |
| `aes.py` | Utilidades de cifrado/descifrado AES. |
| `base58.py` | Implementación de codificación/decodificación Base58 (estándar para direcciones y WIFs). |
| `bip32.py` | Implementación de BIP32 (Wallets Deterministas Jerárquicos). |
| `bip38.py` | Implementación de BIP38 (Claves privadas protegidas por contraseña). |
| `chains.py` | Configuración para redes blockchain conocidas (Chain IDs, prefijos de dirección). |
| `dictionary.py` | Listas de palabras para generación de Brain Keys. |
| `ecdsasig.py` | **Firmas ECDSA**: Lógica central para firmar datos con la curva SECP256k1. |
| `objects.py` | Objetos Graphene de bajo nivel. |
| `objecttypes.py` | Definiciones de tipos de objetos Graphene. |
| `operationids.py` | Constantes de IDs de operación. |
| `operations.py` | Definiciones base de operaciones. |
| `prefix.py` | Manejo de prefijos de dirección. |
| `py23.py` | Utilidades de compatibilidad Python 2/3 (legacy). |
| `signedtransactions.py` | Estructura de transacción firmada de bajo nivel. |
| `types.py` | **Tipos de Serialización**: Define `Int64`, `String`, `Array`, `PointInTime`, etc., para serialización binaria. |
| `unsignedtransactions.py` | Estructura de transacción no firmada. |
| `version.py` | Información de versión del módulo. |

## Uso

Este módulo es usado extensivamente por `blurtbase` para serializar operaciones y por `blurtpy` para firmar transacciones. Raramente es usado directamente por usuarios finales.
