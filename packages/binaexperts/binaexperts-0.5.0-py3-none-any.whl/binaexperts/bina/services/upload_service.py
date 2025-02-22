# services/upload_service.py

from binaexperts.common.loadhelpers import encode_file_to_base64  # <-- Correct import
from binaexperts.settings import BASE_IMPORT_DATASET_URI, IMPORT_DATASET_FILE_ENDPOINT, IMPORT_DATASET_URL_ENDPOINT
from binaexperts.http_client import HttpClient
from binaexperts.common.logger import get_logger

logger = get_logger(__name__)

class UploadService:
    def __init__(self, http_client: HttpClient, organization_id: str):
        self.organization_id = organization_id
        self.http_client = http_client

    def upload_file(self, file_path, dataset_name, dataset_type):
        """Upload a local file."""
        logger.info("Starting file encoding.")
        encoded_file = encode_file_to_base64(file_path)  # <-- Using the function here

        logger.info("Starting file upload.")
        import_url = BASE_IMPORT_DATASET_URI.format(organization_id=self.organization_id) + IMPORT_DATASET_FILE_ENDPOINT
        data = {
            "zip_file": encoded_file,
            "dataset_name": dataset_name,
            "dataset_type": dataset_type
        }
        response = self.http_client.post(import_url, json=data)

        logger.debug(f"Response status code: {response.status_code}, Response text: {response.text}")
        logger.info("File upload process finished.")

        if response.status_code in [200, 204]:
            logger.info("File uploaded successfully!")
            return response.json() if response.status_code == 200 else {"message": "Upload successful with no content."}
        else:
            logger.error(f"File upload failed: {response.status_code}, {response.text}")
            raise Exception(f"File upload failed: {response.status_code}, {response.text}")

    def upload_from_url(self, url, dataset_name, dataset_type):
        """Upload a file from a URL."""
        logger.info("Starting file upload from URL.")
        import_url = BASE_IMPORT_DATASET_URI.format(organization_id=self.organization_id) + IMPORT_DATASET_URL_ENDPOINT
        data = {
            "url": url,
            "dataset_name": dataset_name,
            "dataset_type": dataset_type
        }
        response = self.http_client.post(import_url, json=data)

        logger.debug(f"Response status code: {response.status_code}, Response text: {response.text}")

        if response.status_code in [200, 204]:
            logger.info("File uploaded successfully from URL!")
            return response.json() if response.status_code == 200 else {"message": "Upload successful with no content."}
        else:
            logger.error(f"File upload from URL failed: {response.status_code}, {response.text}")
            raise Exception(f"File upload from URL failed: {response.status_code}, {response.text}")
