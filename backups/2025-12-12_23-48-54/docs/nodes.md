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

## Automatic Node Selection (Recommended for Performance)

`blurtpy` has a built-in feature to automatically benchmark known nodes and connect to the fastest one. To use this, set `node="best"`.

```python
from blurtpy import Blurt

# Automatically find and connect to the best node
b = Blurt(node="best")
```

## Manual Node Selection

If you prefer to connect to a specific node (e.g., for consistency or debugging), you can pass a list of URLs. The library will try to connect to them in order.

```python
from blurtpy import Blurt

# Connect to a specific node
b = Blurt(node=["https://rpc.beblurt.com"])
```

> **Note:** Node availability and performance may vary. Using `node="best"` is generally more reliable as it adapts to network conditions.
