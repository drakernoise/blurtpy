# Blurt RPC Nodes

Here is a list of known public RPC nodes for the Blurt blockchain. You can use any of these nodes to connect to the network using `blurtpy`.

| Node URL | Maintainer |
| :--- | :--- |
| `https://rpc.beblurt.com` | beblurt |
| `https://rpc.blurt.world` | Official |
| `https://blurt-rpc.saboin.com` | Saboin |
| `https://blurtrpc.actifit.io` | Actifit |
| `https://kentzz.blurt.world` | Kentzz |
| `https://rpc.blurt.live` | Blurt.live |
| `https://blurtdev.techcoderx.com` | TechCoderx |

## Usage Example

```python
from blurtpy import Blurt

# Connect to a specific node
b = Blurt(node=["https://rpc.beblurt.com"])
```

> **Note:** Node availability and performance may vary. If one node is down, try another from the list.
