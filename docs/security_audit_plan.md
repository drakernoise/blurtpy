# Plan de Auditoría de Seguridad: `blurtpy`

## Objetivo
Evaluar la seguridad de la librería `blurtpy`, enfocándose en la protección de claves privadas y la integridad de las transacciones.

## Áreas de Evaluación

### 1. Manejo de Claves Privadas (WIF)
- **Riesgo:** Exposición accidental de claves en logs, excepciones o salida estándar.
- **Prueba:**
    - Búsqueda de patrones `print(.*key.*)` o `log.*(.*key.*)`.
    - Verificar que `__repr__` de objetos `PrivateKey` no muestre la clave en texto plano.

### 2. Criptografía y Firma (ECDSA)
- **Riesgo:** Firmas inválidas o uso de entropía débil (nonces repetidos).
- **Prueba:**
    - Verificar que se usa `ecdsa` con curva `SECP256k1`.
    - Verificar implementación de RFC6979 (firmas deterministas) para evitar ataques de recuperación de clave privada.
    - Test de firma: Firmar un mensaje/transacción y recuperar la clave pública.

### 3. Almacenamiento Local (Wallet)
- **Riesgo:** Claves guardadas en texto plano o con cifrado débil en `blurtpy.sqlite` (o similar).
- **Prueba:**
    - Crear un wallet protegido por contraseña.
    - Inspeccionar el archivo de base de datos SQL para asegurar que las claves WIF están cifradas (AES-256).

### 4. Dependencias
- **Riesgo:** Uso de librerías criptográficas obsoletas o vulnerables.
- **Prueba:** Revisar `setup.py` y versiones de `ecdsa`, `pycryptodomex`.

## Ejecución
Se crearán scripts de prueba específicos para cada área.
