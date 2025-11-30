# blurtpy: Librería Python para Blurt

`blurtpy` es una librería Python moderna, robusta y segura para interactuar con la blockchain de **Blurt**.
Es un fork directo de la popular librería `beem`, optimizada y limpiada específicamente para el ecosistema Blurt.

## Características Principales

*   **Nativa para Blurt:** Sin código muerto de Steem o Hive. Optimizada para las reglas de consenso de Blurt.
*   **Segura:** Auditoría de seguridad realizada. Manejo de claves privadas endurecido para prevenir fugas accidentales.
*   **Completa:** Soporta operaciones de cuenta, transferencias, votación, testigos, y más.
*   **Alto Rendimiento:** Soporte para nodos WebSocket y HTTP. Firma de transacciones rápida (soporte opcional para `secp256k1`).

## Instalación

### Requisitos Previos
*   Python 3.8 o superior.
*   `pip` y `setuptools`.

### Instalación desde el código fuente
```bash
git clone https://gitlab.com/tu-usuario/blurtpy.git
cd blurtpy
pip install -e .
```

### Dependencias Opcionales (Recomendadas)
Para mayor velocidad en la firma de transacciones:
```bash
pip install secp256k1prp
```
o
```bash
pip install cryptography
```

## Uso Rápido

### Conexión a Blurt
```python
from blurtpy import Blurt

# Conectar a un nodo público (ver docs/nodes.md para una lista)
b = Blurt(node=["<URL_NODO_RPC>"])

print(b.info())
```

### Gestión de Cuentas
```python
from blurtpy.account import Account

# Leer información de una cuenta
acc = Account("<TU_USUARIO>", blockchain_instance=b)
print(f"Balance: {acc.balances['available']}")
print(f"Voting Power: {acc.vp:.2f}%")
```

### Enviar Transferencia
```python
from blurtpy import Blurt

# Usar el wallet local seguro (recomendado)
b = Blurt(node=["<URL_NODO_RPC>"])
b.wallet.unlock("tu-contraseña-de-wallet")

b.transfer("<DESTINATARIO>", 10, "BLURT", "memo de prueba", account="<TU_USUARIO>")
```

### Votar un Post
```python
from blurtpy import Blurt

# Usar el wallet local seguro (recomendado)
b = Blurt(node=["<URL_NODO_RPC>"])
b.wallet.unlock("tu-contraseña-de-wallet")

# Votar al 100%
b.vote("@<USUARIO_AUTOR>/<PERMLINK>", 100, account="<TU_USUARIO>")
```

## Seguridad

`blurtpy` ha sido auditada para asegurar un manejo responsable de las claves privadas.
*   **Protección de Logs:** Los objetos `PrivateKey` no muestran el WIF (clave privada) al ser impresos o convertidos a string, evitando fugas en logs.
*   **Firma Determinista:** Soporte para firmas ECDSA robustas.

> **Nota:** Nunca compartas tus claves privadas. Si usas el wallet local (`blurtpy.sqlite`), asegúrate de protegerlo con una contraseña fuerte.

## Documentación Adicional

En la carpeta `docs/` encontrarás:
*   [Guía de Migración y Walkthrough](docs/walkthrough.md)
*   [Reporte de Auditoría de Seguridad](docs/security_audit_report.md)

## Créditos

`blurtpy` es un fork de la librería modificada por [Samuel Alphée Richard (Saboin)](https://gitlab.com/saboin), la cual es un fork de [beem](https://github.com/holgern/beem) creado por [Holger Hattendorf](https://github.com/holgern), quien a su vez se basó en `python-bitshares` de [Fabian Schuh](https://github.com/xeroc).
Agradecemos a la comunidad de código abierto por sentar las bases de este proyecto.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.
