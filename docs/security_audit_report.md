# Reporte de Auditoría de Seguridad: `blurtpy`

## Resumen Ejecutivo
Se ha realizado una auditoría de seguridad y endurecimiento de la librería `blurtpy`, con foco en la protección de claves privadas y la integridad de las transacciones.

**Resultado:** La librería ha sido **endurecida**. Se han mitigado riesgos críticos de exposición de claves.

## Hallazgos y Correcciones

### 1. Exposición de Claves Privadas (WIF)
- **Estado Inicial:** `CRÍTICO`. Los objetos `PrivateKey` exponían el WIF (clave privada en formato Base58) al ser convertidos a string (`str()`) o impresos (`print()`).
- **Acción:** Se modificó `blurtgraphenebase/account.py` para censurar la salida de `__str__` y `__repr__`.
- **Estado Actual:** `SEGURO`. Ahora muestran la clave pública asociada (ej. `<PrivateKey: BLT5...>`).
    - *Nota:* Para obtener el WIF explícitamente, el desarrollador debe usar `format(pk, "WIF")` o acceder a métodos internos, lo cual previene fugas accidentales.

### 2. Firma de Transacciones (ECDSA)
- **Estado:** `VALIDADO`.
- **Determinismo:** La implementación por defecto (usando `cryptography` o `ecdsa` puro) añade entropía (`time.time()`) al generar el nonce `k`.
    - Esto significa que firmar el mismo mensaje dos veces produce firmas diferentes.
    - **Evaluación:** Esto es seguro (evita reutilización de nonce), aunque difiere del estándar RFC6979 estricto (determinista). Es un comportamiento aceptable y seguro.
- **Verificación:** Las firmas generadas son válidas y verificables correctamente contra la clave pública.

### 3. Dependencias Internas
- Se detectaron y corrigieron dependencias internas que confiaban en `repr(priv_key)` para obtener el secreto (en `ecdsasig.py` y `account.py`). Estas han sido refactorizadas para acceder al secreto de forma segura y explícita.

## Recomendaciones para el Usuario
1.  **Gestión de Claves:** Evite imprimir objetos `PrivateKey` en logs de producción (aunque ahora es seguro, es buena práctica evitarlo).
2.  **Entorno:** Instale `secp256k1` (librería C) si es posible para mayor rendimiento y determinismo en las firmas, aunque la implementación en Python puro es segura.
3.  **Wallet Local:** Si usa el wallet local (`sqlite`), asegúrese de usar una contraseña fuerte, ya que el cifrado depende de ella.

## Próximos Pasos
- Considerar implementar una limpieza de memoria segura (zeroing) para las claves después de su uso, aunque esto es difícil en Python debido al recolector de basura.
