# Asteroid Odyssey

A Python SDK for exploring the far reaches of the known web.

## Installation

```bash
pip install asteroid-odyssey
```

## Usage

```python
from asteroid_odyssey import Odyssey

odyssey = Odyssey()
odyssey.run_workflow()
```

## Regenerate the client

Assuming your structure is like this:
```
asteroid-odyssey/<you are here>
agents/server/api/openapi.yaml
```

```bash
openapi-python-client generate --path ../agents/server/api/openapi.yaml --output-path src/api/generated/agents --overwrite
openapi-python-client generate --path ../platform/server/openapi.yaml --output-path src/api/generated/platform --overwrite
```
