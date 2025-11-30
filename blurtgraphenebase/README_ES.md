# Módulo blurtgraphenebase

Este módulo contiene las primitivas criptográficas de bajo nivel, utilidades de codificación y tipos de datos que forman la base del protocolo Blurt. Maneja los "tuercas y tornillos" de la interacción con la blockchain.

## Componentes Clave

*   **`ecdsasig.py`:** Implementa el Algoritmo de Firma Digital de Curva Elíptica (ECDSA) para firmar transacciones.
*   **`base58.py`:** Utilidades para codificación y decodificación Base58 (usado para direcciones y claves).
*   **`types.py`:** Define tipos de serialización de bajo nivel (ej. `Int64`, `String`, `Array`) para asegurar que los datos coincidan con el formato binario esperado por la blockchain.
*   **`chains.py`:** Contiene la configuración para cadenas conocidas (Chain IDs, prefijos de dirección).
*   **`bip32.py` / `bip38.py`:** Implementa Propuestas de Mejora de Bitcoin (BIPs) para claves deterministas jerárquicas y claves protegidas por contraseña.

## Uso

Este módulo es usado extensivamente por `blurtbase` para serializar operaciones y por `blurtpy` para firmar transacciones. Raramente es usado directamente por usuarios finales.
