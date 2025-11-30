# Módulo Core de blurtpy

Este directorio contiene la lógica central y las clases principales de la librería `blurtpy`. Es la interfaz de alto nivel con la que los desarrolladores interactúan más frecuentemente.

## Descripción de Archivos

| Archivo | Descripción |
| :--- | :--- |
| `__init__.py` | Inicialización del módulo y exportaciones. |
| `account.py` | **Clase `Account`**: Representa una cuenta de Blurt. Se usa para obtener balances, historial y realizar acciones de cuenta. |
| `amount.py` | **Clase `Amount`**: Maneja cantidades de moneda (ej. "10.000 BLURT") y operaciones aritméticas. |
| `asciichart.py` | Utilidades para generar gráficos ASCII, principalmente para la CLI. |
| `asset.py` | **Clase `Asset`**: Representa activos de la blockchain (BLURT, VESTS) y sus propiedades. |
| `block.py` | **Clase `Block`**: Representa un bloque en la blockchain, conteniendo transacciones. |
| `blockchain.py` | **Clase `Blockchain`**: Información general de la blockchain, bloque actual, parámetros de la cadena. |
| `blockchaininstance.py` | Gestiona la instancia compartida de `Blurt` para asegurar una única conexión entre objetos. |
| `blockchainobject.py` | Clase base para todos los objetos de la blockchain, manejando caché y carga diferida. |
| `blurt.py` | **Clase `Blurt`**: El punto de entrada principal. Conecta a la blockchain, gestiona el wallet y maneja transacciones. |
| `blurtsigner.py` | Lógica para firmar transacciones usando las claves disponibles. |
| `cli.py` | Implementación de la Interfaz de Línea de Comandos (CLI) para el comando `blurtpy`. |
| `comment.py` | **Clase `Comment`**: Representa posts y comentarios. Se usa para leer contenido, responder y votar. |
| `constants.py` | Constantes del sistema y valores por defecto de configuración. |
| `conveyor.py` | Procesa eficientemente bloques y operaciones en un flujo (stream). |
| `discussions.py` | **Clase `Discussions`**: Obtiene listas de discusiones (trending, hot, created, etc.). |
| `exceptions.py` | Clases de excepción personalizadas para `blurtpy`. |
| `imageuploader.py` | Utilidades para subir imágenes a IPFS u otros servicios de alojamiento. |
| `instance.py` | Funciones auxiliares para la gestión de instancias. |
| `market.py` | **Clase `Market`**: Interfaz para el Exchange Descentralizado (DEX). |
| `memo.py` | Utilidades para cifrar y descifrar memos de transacciones. |
| `message.py` | Herramientas para firmar y verificar mensajes de texto arbitrarios con claves privadas. |
| `nodelist.py` | **Clase `NodeList`**: Gestiona la lista de nodos RPC y realiza benchmarks de latencia. |
| `price.py` | **Clase `Price`**: Representa una tasa de cambio entre dos activos. |
| `profile.py` | Utilidades para analizar y manejar metadatos del perfil de usuario. |
| `snapshot.py` | Herramientas para tomar instantáneas de balances de cuentas u otro estado. |
| `storage.py` | Interfaz para el backend de almacenamiento local. |
| `transactionbuilder.py` | **Clase `TransactionBuilder`**: Construye, firma y transmite transacciones. |
| `utils.py` | Funciones de utilidad general (parseo de fechas, formateo, etc.). |
| `version.py` | Información de versión de la librería. |
| `vote.py` | **Clase `Vote`**: Representa un voto en un post o comentario. |
| `wallet.py` | **Clase `Wallet`**: Gestiona claves privadas locales y el bloqueo/desbloqueo de la base de datos. |
| `witness.py` | **Clase `Witness`**: Representa un productor de bloques (witness) y operaciones relacionadas. |

## Ejemplo de Uso

```python
from blurtpy import Blurt
from blurtpy.account import Account

# Inicializar instancia de Blurt
b = Blurt(node="best")

# Acceder al Wallet
if b.wallet.created():
    b.wallet.unlock("tu-contraseña")

# Acceder a la Cuenta
acc = Account("<TU_USUARIO>", blockchain_instance=b)
print(acc.balances)
```
