# HeadlessAgents

Types:

```python
from headlessagents.types import CallAgentResponse, CheckHealthResponse, RetrieveAgentStatsResponse
```

Methods:

- <code title="post /call/{agent_id}">client.<a href="./src/headlessagents/_client.py">call_agent</a>(agent_id, \*\*<a href="src/headlessagents/types/client_call_agent_params.py">params</a>) -> <a href="./src/headlessagents/types/call_agent_response.py">CallAgentResponse</a></code>
- <code title="get /health">client.<a href="./src/headlessagents/_client.py">check_health</a>() -> <a href="./src/headlessagents/types/check_health_response.py">CheckHealthResponse</a></code>
- <code title="get /agent/{agent_id}/stats">client.<a href="./src/headlessagents/_client.py">retrieve_agent_stats</a>(agent_id) -> <a href="./src/headlessagents/types/retrieve_agent_stats_response.py">RetrieveAgentStatsResponse</a></code>
