# Lam

Types:

```python
from raccoonai.types import LamExtractResponse, LamIntegrationRunResponse, LamRunResponse
```

Methods:

- <code title="post /lam/extract">client.lam.<a href="./src/raccoonai/resources/lam.py">extract</a>(\*\*<a href="src/raccoonai/types/lam_extract_params.py">params</a>) -> <a href="./src/raccoonai/types/lam_extract_response.py">LamExtractResponse</a></code>
- <code title="post /lam/{app_name}/run">client.lam.<a href="./src/raccoonai/resources/lam.py">integration_run</a>(app_name, \*\*<a href="src/raccoonai/types/lam_integration_run_params.py">params</a>) -> <a href="./src/raccoonai/types/lam_integration_run_response.py">LamIntegrationRunResponse</a></code>
- <code title="post /lam/run">client.lam.<a href="./src/raccoonai/resources/lam.py">run</a>(\*\*<a href="src/raccoonai/types/lam_run_params.py">params</a>) -> <a href="./src/raccoonai/types/lam_run_response.py">LamRunResponse</a></code>

# Fleet

Types:

```python
from raccoonai.types import (
    FleetCreateResponse,
    FleetLogsResponse,
    FleetStatusResponse,
    FleetTerminateResponse,
)
```

Methods:

- <code title="post /sessions/create">client.fleet.<a href="./src/raccoonai/resources/fleet.py">create</a>(\*\*<a href="src/raccoonai/types/fleet_create_params.py">params</a>) -> <a href="./src/raccoonai/types/fleet_create_response.py">FleetCreateResponse</a></code>
- <code title="get /sessions/{session_id}/logs">client.fleet.<a href="./src/raccoonai/resources/fleet.py">logs</a>(session_id) -> <a href="./src/raccoonai/types/fleet_logs_response.py">FleetLogsResponse</a></code>
- <code title="get /sessions/{session_id}/status">client.fleet.<a href="./src/raccoonai/resources/fleet.py">status</a>(session_id) -> <a href="./src/raccoonai/types/fleet_status_response.py">FleetStatusResponse</a></code>
- <code title="delete /sessions/{session_id}/terminate">client.fleet.<a href="./src/raccoonai/resources/fleet.py">terminate</a>(session_id) -> <a href="./src/raccoonai/types/fleet_terminate_response.py">FleetTerminateResponse</a></code>
