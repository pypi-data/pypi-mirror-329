import logging
import os
from typing import Optional, List, Dict, Any
from uuid import UUID

from asteroid_odyssey.api.generated.agents.asteroid_agents_api_client.api.agent.get_agents import sync as get_agents_sync
from asteroid_odyssey.api.generated.agents.asteroid_agents_api_client.api.api.get_open_api import sync_detailed as get_open_api_sync
from asteroid_odyssey.api.generated.agents.asteroid_agents_api_client.api.default.create_workflow import sync as create_workflow_sync
from asteroid_odyssey.api.generated.agents.asteroid_agents_api_client.api.default.health_check import sync as health_check_sync
from asteroid_odyssey.api.generated.agents.asteroid_agents_api_client.api.workflow.execute_workflow import sync as execute_workflow_sync
from asteroid_odyssey.api.generated.agents.asteroid_agents_api_client.api.workflow.get_workflow_executions import \
    sync as get_workflow_executions_sync
from asteroid_odyssey.api.generated.agents.asteroid_agents_api_client.client import Client as AgentsClient
from asteroid_odyssey.api.generated.agents.asteroid_agents_api_client.models import CreateWorkflowRequest, WorkflowExecutionRequest, \
    WorkflowExecution
from asteroid_odyssey.api.generated.platform.asteroid_api_client.api.api_key.validate_api_key import \
    sync_detailed as validate_api_key_sync
from asteroid_odyssey.api.generated.platform.asteroid_api_client.api.improve.create_feedback import sync_detailed as create_feedback_sync
from asteroid_odyssey.api.generated.platform.asteroid_api_client.api.run.get_run import sync as get_run_sync
from asteroid_odyssey.api.generated.platform.asteroid_api_client.api.run.get_run_status import sync as get_run_status_sync
from asteroid_odyssey.api.generated.platform.asteroid_api_client.client import Client as PlatformClient
from asteroid_odyssey.api.generated.platform.asteroid_api_client.models import Status
from asteroid_odyssey.api.generated.platform.asteroid_api_client.models.error_response import ErrorResponse
from asteroid_odyssey.api.generated.platform.asteroid_api_client.models.feedback import Feedback
from asteroid_odyssey.api.generated.platform.asteroid_api_client.models.feedback_request import FeedbackRequest
from asteroid_odyssey.exceptions import ApiError

# Logger
logger = logging.getLogger(__name__)


class Odyssey:
    """Wrapper for the generated API client."""

    def __init__(
            self,
            api_key: Optional[str] = None,
            agents_base_url: Optional[str] = None,
            platform_base_url: Optional[str] = None
    ):
        """Initialize the client.

        Args:
            api_key: Optional API key for authentication
            agents_base_url: Base URL for the agents API
            platform_base_url: Base URL for the platform API
        """
        if api_key is None:
            api_key = os.getenv("ASTEROID_API_KEY")
            if not api_key:
                raise ApiError(
                    "Asteroid API key is required, please set the ASTEROID_API_KEY environment variable. You can get one from https://platform.asteroid.com/")

        if agents_base_url is None:
            from_env = os.getenv("ASTEROID_AGENTS_API_URL")
            if not from_env:
                from_env = "https://odyssey.asteroid.ai/api/v1"
            agents_base_url = from_env

        if platform_base_url is None:
            from_env = os.getenv("ASTEROID_API_URL")
            if not from_env:
                from_env = "https://platform.asteroid.com/api/v1"
            platform_base_url = from_env

        self._agents_client = AgentsClient(
            base_url=agents_base_url,
            verify_ssl=False,
            headers={"X-Asteroid-Agents-Api-Key": f"{api_key}"}
        )

        self._platform_client = PlatformClient(
            base_url=platform_base_url,
            verify_ssl=False,
            headers={"X-Asteroid-Api-Key": f"{api_key}"}
        )

        print(f"Validating API key")
        try:
            response = validate_api_key_sync(client=self._platform_client)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error validating API key: {e}")
            raise e

    def get_agents(self) -> List[Dict[str, Any]]:
        """Retrieves a list of all agents."""
        try:
            response = get_agents_sync(client=self._agents_client)
            return response
        except Exception as e:
            logger.error(f"Error retrieving agents: {e}")
            raise e

    def create_workflow(self, agent_name: str, request: CreateWorkflowRequest) -> str:
        """Creates a new workflow for a given agent."""
        try:
            workflow_id = create_workflow_sync(client=self._agents_client, agent_name=agent_name, body=request)
            return workflow_id
        except Exception as e:
            logger.error(f"Error creating workflow: {e}")
            raise e

    def run_workflow(self, workflow_id: UUID, request: WorkflowExecutionRequest) -> str:
        """Executes a saved workflow for an agent."""
        try:
            response = execute_workflow_sync(client=self._agents_client, workflow_id=workflow_id, body=request)
            return response
        except Exception as e:
            logger.error(f"Error running workflow: {e}")
            raise e

    def get_workflow_runs(self) -> list[WorkflowExecution] | None:
        """Retrieves all workflows along with their executions."""
        try:
            response = get_workflow_executions_sync(client=self._agents_client)
            return response
        except Exception as e:
            logger.error(f"Error retrieving workflow runs: {e}")
            raise e

    def create_run_feedback(self, run_id: UUID, request: FeedbackRequest) -> Feedback:
        """Creates feedback for a run."""
        try:
            response = create_feedback_sync(client=self._platform_client, run_id=run_id, body=request)
            return response
        except Exception as e:
            logger.error(f"Error creating feedback: {e}")
            raise e

    def get_open_api_schema(self) -> Any:
        """Retrieves the OpenAPI schema from the API."""
        try:
            response = get_open_api_sync(client=self._agents_client)
            return response
        except Exception as e:
            logger.error(f"Error retrieving OpenAPI schema: {e}")
            raise e

    def health_check(self) -> Dict[str, Any]:
        """Checks the health of the API."""
        try:
            response = health_check_sync(client=self._agents_client)
            return response
        except Exception as e:
            logger.error(f"Error performing health check: {e}")
            raise e

    def get_run_status(self, run_id: UUID) -> Status:
        """Retrieves the status of a run."""
        try:
            response = get_run_status_sync(client=self._platform_client, run_id=run_id)
            if isinstance(response, ErrorResponse):
                return None
            return response
        except Exception as e:
            logger.error(f"Error retrieving run status: {e}")
            raise e

    def get_run_result(self, run_id: UUID) -> str:
        """Retrieves the result of a run."""
        try:
            run = get_run_sync(client=self._platform_client, run_id=run_id)
            metadata = run.metadata
            if not metadata:
                raise ApiError("Run metadata not found")
            result = metadata.additional_properties.get('final_result')
            if not result:
                raise ApiError("Run result not found")
            return result
        except Exception as e:
            logger.error(f"Error retrieving run result: {e}")
            raise e
