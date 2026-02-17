# Módulo blurtapi

Este módulo es responsable de la comunicación RPC (Remote Procedure Call) de bajo nivel con los nodos de la blockchain de Blurt.

## Descripción de Archivos

| Archivo | Descripción |
| :--- | :--- |
| `__init__.py` | Inicialización del módulo. |
| `exceptions.py` | Clases de excepción específicas de RPC (ej. `RPCError`, `NumRetriesReached`). |
| `graphenerpc.py` | **Clase `GrapheneRPC`**: Maneja el protocolo JSON-RPC para enviar solicitudes y recibir respuestas. Gestiona el ciclo de vida de la conexión y el manejo de errores. |
| `node.py` | **Clase `Node`**: Representa una conexión a una URL de nodo específica. |
| `noderpc.py` | **Clase `NodeRPC`**: Un envoltorio para interacciones específicas con nodos, a menudo usado para agrupar llamadas API relacionadas. |
| `rpcutils.py` | Funciones de utilidad para comunicación RPC (ej. esperar entre reintentos). |
| `version.py` | Información de versión del módulo. |

## Uso

Este módulo es usado principalmente de forma interna por la clase `Blurt` en `blurtpy/blurt.py`. Los desarrolladores raramente necesitan interactuar con `blurtapi` directamente a menos que estén construyendo conectores RPC personalizados o herramientas de bajo nivel.
