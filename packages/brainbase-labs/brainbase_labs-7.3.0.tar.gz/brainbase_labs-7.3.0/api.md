# Team

Types:

```python
from brainbase_labs.types import TeamRetrieveResponse
```

Methods:

- <code title="get /api/team">client.team.<a href="./src/brainbase_labs/resources/team/team.py">retrieve</a>(\*\*<a href="src/brainbase_labs/types/team_retrieve_params.py">params</a>) -> <a href="./src/brainbase_labs/types/team_retrieve_response.py">TeamRetrieveResponse</a></code>

## Assets

Types:

```python
from brainbase_labs.types.team import AssetRegisterPhoneNumberResponse
```

Methods:

- <code title="delete /api/team/assets/phone_numbers/{phoneNumberId}/delete">client.team.assets.<a href="./src/brainbase_labs/resources/team/assets.py">delete_phone_number</a>(phone_number_id) -> None</code>
- <code title="post /api/team/assets/register_phone_number">client.team.assets.<a href="./src/brainbase_labs/resources/team/assets.py">register_phone_number</a>(\*\*<a href="src/brainbase_labs/types/team/asset_register_phone_number_params.py">params</a>) -> <a href="./src/brainbase_labs/types/team/asset_register_phone_number_response.py">AssetRegisterPhoneNumberResponse</a></code>

## Integrations

### Twilio

Types:

```python
from brainbase_labs.types.team.integrations import TwilioCreateResponse
```

Methods:

- <code title="post /api/team/integrations/twilio/create">client.team.integrations.twilio.<a href="./src/brainbase_labs/resources/team/integrations/twilio.py">create</a>(\*\*<a href="src/brainbase_labs/types/team/integrations/twilio_create_params.py">params</a>) -> <a href="./src/brainbase_labs/types/team/integrations/twilio_create_response.py">TwilioCreateResponse</a></code>
- <code title="delete /api/team/integrations/twilio/{integrationId}/delete">client.team.integrations.twilio.<a href="./src/brainbase_labs/resources/team/integrations/twilio.py">delete</a>(integration_id) -> None</code>

# Workers

Types:

```python
from brainbase_labs.types import Workers, WorkerListResponse
```

Methods:

- <code title="post /api/workers">client.workers.<a href="./src/brainbase_labs/resources/workers/workers.py">create</a>(\*\*<a href="src/brainbase_labs/types/worker_create_params.py">params</a>) -> <a href="./src/brainbase_labs/types/workers/workers.py">Workers</a></code>
- <code title="get /api/workers/{id}">client.workers.<a href="./src/brainbase_labs/resources/workers/workers.py">retrieve</a>(id) -> <a href="./src/brainbase_labs/types/workers/workers.py">Workers</a></code>
- <code title="patch /api/workers/{id}">client.workers.<a href="./src/brainbase_labs/resources/workers/workers.py">update</a>(id, \*\*<a href="src/brainbase_labs/types/worker_update_params.py">params</a>) -> <a href="./src/brainbase_labs/types/workers/workers.py">Workers</a></code>
- <code title="get /api/workers">client.workers.<a href="./src/brainbase_labs/resources/workers/workers.py">list</a>() -> <a href="./src/brainbase_labs/types/worker_list_response.py">WorkerListResponse</a></code>
- <code title="delete /api/workers/{id}">client.workers.<a href="./src/brainbase_labs/resources/workers/workers.py">delete</a>(id) -> None</code>

## Deployments

### Voice

Types:

```python
from brainbase_labs.types.workers.deployments import VoiceDeployment, VoiceListResponse
```

Methods:

- <code title="post /api/workers/{workerId}/deployments/voice">client.workers.deployments.voice.<a href="./src/brainbase_labs/resources/workers/deployments/voice.py">create</a>(worker_id, \*\*<a href="src/brainbase_labs/types/workers/deployments/voice_create_params.py">params</a>) -> <a href="./src/brainbase_labs/types/workers/deployments/voice_deployment.py">VoiceDeployment</a></code>
- <code title="get /api/workers/{workerId}/deployments/voice/{deploymentId}">client.workers.deployments.voice.<a href="./src/brainbase_labs/resources/workers/deployments/voice.py">retrieve</a>(deployment_id, \*, worker_id) -> <a href="./src/brainbase_labs/types/workers/deployments/voice_deployment.py">VoiceDeployment</a></code>
- <code title="put /api/workers/{workerId}/deployments/voice/{deploymentId}">client.workers.deployments.voice.<a href="./src/brainbase_labs/resources/workers/deployments/voice.py">update</a>(deployment_id, \*, worker_id, \*\*<a href="src/brainbase_labs/types/workers/deployments/voice_update_params.py">params</a>) -> <a href="./src/brainbase_labs/types/workers/deployments/voice_deployment.py">VoiceDeployment</a></code>
- <code title="get /api/workers/{workerId}/deployments/voice">client.workers.deployments.voice.<a href="./src/brainbase_labs/resources/workers/deployments/voice.py">list</a>(worker_id) -> <a href="./src/brainbase_labs/types/workers/deployments/voice_list_response.py">VoiceListResponse</a></code>
- <code title="delete /api/workers/{workerId}/deployments/voice/{deploymentId}">client.workers.deployments.voice.<a href="./src/brainbase_labs/resources/workers/deployments/voice.py">delete</a>(deployment_id, \*, worker_id) -> None</code>

## Flows

Types:

```python
from brainbase_labs.types.workers import Flows, FlowListResponse
```

Methods:

- <code title="post /api/workers/{workerId}/flows">client.workers.flows.<a href="./src/brainbase_labs/resources/workers/flows.py">create</a>(worker_id, \*\*<a href="src/brainbase_labs/types/workers/flow_create_params.py">params</a>) -> <a href="./src/brainbase_labs/types/workers/flows.py">Flows</a></code>
- <code title="get /api/workers/{workerId}/flows/{flowId}">client.workers.flows.<a href="./src/brainbase_labs/resources/workers/flows.py">retrieve</a>(flow_id, \*, worker_id) -> <a href="./src/brainbase_labs/types/workers/flows.py">Flows</a></code>
- <code title="put /api/workers/{workerId}/flows/{flowId}">client.workers.flows.<a href="./src/brainbase_labs/resources/workers/flows.py">update</a>(flow_id, \*, worker_id, \*\*<a href="src/brainbase_labs/types/workers/flow_update_params.py">params</a>) -> <a href="./src/brainbase_labs/types/workers/flows.py">Flows</a></code>
- <code title="get /api/workers/{workerId}/flows">client.workers.flows.<a href="./src/brainbase_labs/resources/workers/flows.py">list</a>(worker_id) -> <a href="./src/brainbase_labs/types/workers/flow_list_response.py">FlowListResponse</a></code>
- <code title="delete /api/workers/{workerId}/flows/{flowId}">client.workers.flows.<a href="./src/brainbase_labs/resources/workers/flows.py">delete</a>(flow_id, \*, worker_id) -> None</code>

## Resources

Types:

```python
from brainbase_labs.types.workers import RagResource
```

Methods:

- <code title="get /api/workers/{workerId}/resources/{resourceId}">client.workers.resources.<a href="./src/brainbase_labs/resources/workers/resources/resources.py">retrieve</a>(resource_id, \*, worker_id) -> <a href="./src/brainbase_labs/types/workers/rag_resource.py">RagResource</a></code>
- <code title="delete /api/workers/{workerId}/resources/{resourceId}">client.workers.resources.<a href="./src/brainbase_labs/resources/workers/resources/resources.py">delete</a>(resource_id, \*, worker_id) -> None</code>

### Link

Types:

```python
from brainbase_labs.types.workers.resources import LinkListResponse
```

Methods:

- <code title="post /api/workers/{workerId}/resources/link">client.workers.resources.link.<a href="./src/brainbase_labs/resources/workers/resources/link.py">create</a>(worker_id, \*\*<a href="src/brainbase_labs/types/workers/resources/link_create_params.py">params</a>) -> <a href="./src/brainbase_labs/types/workers/rag_resource.py">RagResource</a></code>
- <code title="get /api/workers/{workerId}/resources/link">client.workers.resources.link.<a href="./src/brainbase_labs/resources/workers/resources/link.py">list</a>(worker_id) -> <a href="./src/brainbase_labs/types/workers/resources/link_list_response.py">LinkListResponse</a></code>

### File

Types:

```python
from brainbase_labs.types.workers.resources import FileListResponse
```

Methods:

- <code title="post /api/workers/{workerId}/resources/file">client.workers.resources.file.<a href="./src/brainbase_labs/resources/workers/resources/file.py">create</a>(worker_id, \*\*<a href="src/brainbase_labs/types/workers/resources/file_create_params.py">params</a>) -> <a href="./src/brainbase_labs/types/workers/rag_resource.py">RagResource</a></code>
- <code title="get /api/workers/{workerId}/resources/file">client.workers.resources.file.<a href="./src/brainbase_labs/resources/workers/resources/file.py">list</a>(worker_id) -> <a href="./src/brainbase_labs/types/workers/resources/file_list_response.py">FileListResponse</a></code>

## Tests

Types:

```python
from brainbase_labs.types.workers import TestCreateResponse
```

Methods:

- <code title="post /api/workers/{workerId}/tests">client.workers.tests.<a href="./src/brainbase_labs/resources/workers/tests.py">create</a>(worker_id, \*\*<a href="src/brainbase_labs/types/workers/test_create_params.py">params</a>) -> <a href="./src/brainbase_labs/types/workers/test_create_response.py">TestCreateResponse</a></code>
- <code title="put /api/workers/{workerId}/tests/{testId}">client.workers.tests.<a href="./src/brainbase_labs/resources/workers/tests.py">update</a>(test_id, \*, worker_id, \*\*<a href="src/brainbase_labs/types/workers/test_update_params.py">params</a>) -> None</code>
- <code title="delete /api/workers/{workerId}/tests/{testId}">client.workers.tests.<a href="./src/brainbase_labs/resources/workers/tests.py">delete</a>(test_id, \*, worker_id) -> None</code>
- <code title="get /api/workers/{workerId}/tests/{testId}/runs">client.workers.tests.<a href="./src/brainbase_labs/resources/workers/tests.py">list_runs</a>(test_id, \*, worker_id) -> None</code>
- <code title="post /api/workers/{workerId}/tests/{testId}/run">client.workers.tests.<a href="./src/brainbase_labs/resources/workers/tests.py">run</a>(test_id, \*, worker_id) -> None</code>
