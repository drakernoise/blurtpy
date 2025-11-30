# Módulo Core de blurtpy

Este directorio contiene la lógica central y las clases principales de la librería `blurtpy`. Es la interfaz de alto nivel con la que los desarrolladores interactúan más frecuentemente.

## Clases Clave

*   **`Blurt` (`blurt.py`):** El punto de entrada principal. Conecta a la blockchain, gestiona el wallet y maneja transacciones.
*   **`Account` (`account.py`):** Representa una cuenta de Blurt. Se usa para obtener balances, historial y realizar acciones específicas de la cuenta.
*   **`Wallet` (`wallet.py`):** Gestiona las claves privadas locales y el bloqueo/desbloqueo de la base de datos.
*   **`TransactionBuilder` (`transactionbuilder.py`):** Construye y firma transacciones.
*   **`NodeList` (`nodelist.py`):** Gestiona la lista de nodos RPC y el benchmarking.

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
acc = Account("tekraze", blockchain_instance=b)
print(acc.balances)
```
