from time import sleep
from typing import IO, Optional, Dict
from splore_sdk.core.logger import sdk_logger
from splore_sdk.extractions.extractions_service import ExtractionService
from splore_sdk.agents.agents_service import AgentService
from splore_sdk.core.api_client import APIClient
from splore_sdk.utils.file_uploader import FileUploader


class SploreSDK:
    def __init__(self, api_key: str, base_id: str, agent_id: Optional[str] = None, user_id: Optional[str] = None):
        self.logger = sdk_logger
        if not api_key:
            raise ValueError("API Key is required to initialize SploreSDK.")
        self.base_id = base_id
        self.api_key = api_key
        self.agent_id = agent_id
        self.user_id = user_id
        self.client = APIClient(api_key=self.api_key, base_id=base_id)
        self.agents = AgentService(self.client)
        self.file_uploader = FileUploader(api_key=self.api_key, base_id=self.base_id, user_id=self.user_id)
        self.validate_api_key()
        self.logger.info("SploreSDK initialized with base_id: %s", self.base_id)

    def validate_api_key(self):
        try:
            self.client.validate_api_key()
        except Exception as e:
            self.logger.debug(f"API Key validation failed: {e}")
            raise ValueError(f"API Key validation failed")
    
    def get_agents(self, agentId: Optional[str]=None, agentName: Optional[str]=None):
        """Fetch the list of agents related to the base."""
        return self.agents.get_agents(agentId=agentId, agentName=agentName)

    def init_agent(self, agent_id: str) -> "AgentSDK":
        """
        Initialize and return an agent-specific instance.

        Args:
            agent_id (str): The ID of the agent to initialize.

        Returns:
            AgentSDK: An instance of AgentSDK specific to the given agent ID.
        """
        if not agent_id:
            raise ValueError("Agent ID is required to initialize an agent.")
        self.logger.info(f"Initializing agent with ID: {agent_id}")
        return AgentSDK(api_key=self.api_key, base_id=self.base_id, agent_id=agent_id)


class AgentSDK(SploreSDK):
    def __init__(self, api_key: str, base_id: str, agent_id: str):
        super().__init__(api_key, base_id, agent_id)
        self.agent_id = agent_id
        self.client = APIClient(api_key=self.api_key, base_id=base_id, agent_id=agent_id)
        self.extractions = ExtractionService(self.client, agent_id=agent_id)

    def extract(self, file_path: Optional[str] = None, file_stream: Optional[IO] = None) -> Dict:
        """
        Run the extraction pipeline for the agent by uploading a file.

        Args:
            file_path (Optional[str], optional): Local file path.
            file_stream (Optional[IO], optional): File object/blob.

        Raises:
            ValueError: If neither file_path nor file_stream is provided.

        Returns:
            Dict: Extracted response data from the file.
        """
        if not (file_path or file_stream):
            raise ValueError("One of file_path or file_stream must be provided.")
        if not self.agent_id:
            raise ValueError("Agent ID is required for extraction flow.")

        self.extractions.set_agent(agent_id=self.agent_id)
        self.logger.info(f"Starting file upload for agent {self.agent_id}, file: {file_path}")
        upload_res = self.file_uploader.upload_file(file_path=file_path, file_stream=file_stream)
        self.logger.info(f"File upload completed with file_id: {upload_res}")

        self.extractions.start(file_id=upload_res)
        self.logger.info("File extraction started")

        # Wait for extraction to complete
        extraction_completed = False
        while not extraction_completed:
            extraction_resp = self.extractions.processing_status(file_id=upload_res)
            file_processing_status = extraction_resp.get("fileProcessingStatus")
            extraction_completed = (file_processing_status == "COMPLETED")
            if not extraction_completed:
                self.logger.info("File extraction not completed, waiting...")
                sleep(10)

        extracted_resp = self.extractions.extracted_response(file_id=upload_res)
        self.logger.info("File extraction completed")
        return extracted_resp