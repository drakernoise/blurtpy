# Módulo blurtapi

Este módulo es responsable de la comunicación RPC (Remote Procedure Call) de bajo nivel con los nodos de la blockchain de Blurt.

## Componentes Clave

*   **`GrapheneRPC` (`graphenerpc.py`):** Maneja el protocolo JSON-RPC para enviar solicitudes y recibir respuestas de la blockchain.
*   **`NodeRPC` (`noderpc.py`):** Un envoltorio para interacciones específicas con nodos.
*   **`Node` (`node.py`):** Representa una conexión a un nodo específico de la blockchain.

## Uso

Este módulo es usado principalmente de forma interna por la clase `Blurt` en `blurtpy/blurt.py`. Los desarrolladores raramente necesitan interactuar con `blurtapi` directamente a menos que estén construyendo conectores RPC personalizados o herramientas de bajo nivel.
