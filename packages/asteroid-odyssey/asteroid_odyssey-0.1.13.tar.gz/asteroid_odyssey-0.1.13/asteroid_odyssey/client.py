"""Client wrapper for the generated API client."""

import logging
import os
import time
from typing import Optional
import uuid
from api.generated.asteroid_agents_api_client.client import Client as AgentsClient
from api.generated.asteroid_agents_api_client.models.job import Job
from api.generated.asteroid_agents_api_client.models.job_data import JobData
from api.generated.asteroid_agents_api_client.types import Response
from api.generated.asteroid_agents_api_client.api.agent.run_agent import sync as run_agent_sync
from asteroid_odyssey.exceptions import ApiError

from asteroid_sdk.api.generated.asteroid_api_client.client import Client as PlatformClient
from asteroid_sdk.api.generated.asteroid_api_client.api.run.get_run import sync as get_run_sync
from asteroid_sdk.api.generated.asteroid_api_client.api.run.get_run_status import sync as get_run_status_sync
from asteroid_sdk.api.generated.asteroid_api_client.api.api_key.validate_api_key import sync_detailed as validate_api_key_sync
from asteroid_sdk.api.generated.asteroid_api_client.models.error_response import ErrorResponse


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
            base_url: Base URL for the API
        """
        if api_key is None:
            api_key = os.getenv("ASTEROID_API_KEY")
            if not api_key:
                raise ApiError("Asteroid API key is required, please set the ASTEROID_API_KEY environment variable. You can get one from https://platform.asteroid.com/")

        if agents_base_url is None:
            from_env = os.getenv("ASTEROID_AGENTS_API_URL")
            if not from_env:
                # Fall back to the production server
                # TODO replace with the URL
                from_env = "https://odyssey.asteroid.ai/api/v1"
            agents_base_url = from_env

        if platform_base_url is None:
            from_env = os.getenv("ASTEROID_API_URL")
            if not from_env:
                # Fall back to the production server
                # TODO replace with the URL
                from_env = "https://platform.asteroid.com/api/v1"
            platform_base_url = from_env

        # Create the agents client to submit jobs to the agents server
        self._agents_client = AgentsClient(
            base_url=agents_base_url,
            verify_ssl=False,
            headers={"X-Asteroid-Agents-Api-Key": f"{api_key}"}
        )

        # Create the platform client to get the status and result of the run
        self._platform_client = PlatformClient(
            base_url=platform_base_url,
            verify_ssl=False,
            headers={"X-Asteroid-Api-Key": f"{api_key}"}
        )

        # Get the projects
        print(f"Validating API key")
        try:
            response = validate_api_key_sync(client=self._platform_client)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error validating API key: {e}")
            raise e

    def _handle_response(self, response: Response):
        """Handle API response and errors."""
        logger.info(f"Response: {response}")

        return response

    def start(self, job_data: dict, agent_name: str = "default_web"):
        """Start a new job with the specified data.
        
        Args:
            job_data: Dictionary containing the job data (must include 'task' key)
            agent_name: Name of the agent to run the job (default: 'default_web')
            
        Returns:
            API response from running the job
            
        Raises:
            ApiError: If no task is specified or if there's no response from the API
        """
        if 'task' not in job_data:
            raise ApiError("Job data must include 'task' key")

        logger.info(f"Running job with data: {job_data}")

        try:
            response = run_agent_sync(
                agent_name=agent_name,
                client=self._agents_client,
                body=Job(
                    
                    data=JobData.from_dict(job_data)
                )
            )
            logger.info(f"Response: {response}")
        except Exception as e:
            logger.error(f"Error running job: {e}")
            raise e

        if response is None:
            raise ApiError("No response from API")

        return self._handle_response(response)

    def get_run(self, run_id: str):
        """Get a run by its ID."""
        return self._handle_response(get_run_sync(client=self._platform_client, run_id=run_id))

    def get_run_status(self, run_id: str):
        """Get the status of a run by its ID."""
        try:
            response = get_run_status_sync(client=self._platform_client, run_id=run_id)
            if isinstance(response, ErrorResponse):
                # If we get a 404, the run isn't ready yet
                return None
            
            # The response itself is the Status object
            return response
        except Exception as e:
            print(f"Error getting run status: {str(e)}")
            print(f"Error type: {type(e)}")
            return None

    def get_final_result(self, run_id: str, max_retries=60, retry_delay=1):
        """Get the final result of a run by its ID."""
        retries = 0
        while retries < max_retries:
            print(f"Getting status for run {run_id} (attempt {retries + 1}/{max_retries})")
            status = self.get_run_status(run_id)
            
            if status is None:
                print("Run not ready yet, waiting...")
                time.sleep(retry_delay)
                retries += 1
                continue
            
            if status == "completed" or status == "failed":
                run = self._handle_response(get_run_sync(client=self._platform_client, run_id=run_id))
                metadata = run.metadata
                if metadata is None:
                    raise ApiError("No metadata found for run, can't get final result")
                
                # Access final_result from additional_properties
                if hasattr(metadata, 'additional_properties'):
                    final = metadata.additional_properties.get('final_result')
                    if final is None:
                        raise ApiError("No final result found in metadata additional_properties")
                    return final
                else:
                    raise ApiError("Metadata has no additional_properties")
            else:
                print(f"Run not ready yet, waiting... (status was: {status})")

            time.sleep(retry_delay)
            retries += 1

        raise ApiError(f"Timed out waiting for run to complete after {max_retries} attempts")



