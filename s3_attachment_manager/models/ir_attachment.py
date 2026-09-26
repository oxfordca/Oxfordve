import logging
import os
import random
import time

import boto3
from botocore.exceptions import ClientError

from odoo import api, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.model
    def _get_s3_credentials(self):
        """Retrieve S3 credentials from System Parameters or environment variables as fallback."""
        ICP = self.env["ir.config_parameter"].sudo()

        s3_bucket = ICP.get_param("s3_attachment_manager.bucket") or os.environ.get("S3_ATTACHMENT_MANAGER_BUCKET")
        s3_access_key_id = ICP.get_param("s3_attachment_manager.access_key_id") or os.environ.get("S3_ATTACHMENT_MANAGER_ACCESS_KEY_ID")
        s3_secret_access_key = ICP.get_param("s3_attachment_manager.secret_access_key") or os.environ.get("S3_ATTACHMENT_MANAGER_SECRET_ACCESS_KEY")
        s3_endpoint_url = ICP.get_param("s3_attachment_manager.endpoint_url") or os.environ.get("S3_ATTACHMENT_MANAGER_ENDPOINT_URL")

        if not s3_bucket or not s3_access_key_id or not s3_secret_access_key:
            raise ValidationError(
                "S3 credentials not configured correctly. Please set them in System Parameters (s3_attachment_manager.*) or environment variables."
            )

        return s3_bucket, s3_access_key_id, s3_secret_access_key, s3_endpoint_url

    @api.model
    def _store_file_write(self, fname, bin_data):
        """Write binary data to an S3 bucket with retry logic."""
        # Get S3 credentials
        s3_bucket, s3_access_key_id, s3_secret_access_key, s3_endpoint_url = self._get_s3_credentials()

        # Create an S3 client
        client_kwargs = {
            "aws_access_key_id": s3_access_key_id,
            "aws_secret_access_key": s3_secret_access_key,
        }
        if s3_endpoint_url:
            client_kwargs["endpoint_url"] = s3_endpoint_url

        s3 = boto3.client("s3", **client_kwargs)

        # Configuration for retry attempts and exponential backoff
        max_retries = 3
        base_delay = 2  # seconds
        max_delay = 10  # seconds

        # Loop through retry attempts
        for attempt in range(max_retries):
            try:
                # Try to upload the binary data to the S3 bucket
                s3.put_object(Bucket=s3_bucket, Key=fname, Body=bin_data)
                _logger.info(
                    f"Successfully uploaded file '{fname}' to S3 bucket '{s3_bucket}'."
                )
                return fname
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                _logger.exception(
                    f"Error writing to S3 (attempt {attempt + 1}): {error_code} - {e}"
                )
            except Exception as e:
                _logger.exception(
                    f"Unexpected error writing to S3 (attempt {attempt + 1}): {e}"
                )

            # If there are remaining retry attempts, sleep using exponential backoff with jitter
            if attempt < max_retries - 1:
                sleep_time = min(
                    max_delay,
                    (base_delay * 2**attempt) * (1 + random.uniform(-0.1, 0.1)),
                )
                time.sleep(sleep_time)
            else:
                # If all retry attempts have been exhausted, return False
                return False

    def _file_read(self, fname):
        """Read a file from S3 or fall back to the local file system."""
        s3_bucket, s3_access_key_id, s3_secret_access_key, s3_endpoint_url = self._get_s3_credentials()
        client_kwargs = {
            "aws_access_key_id": s3_access_key_id,
            "aws_secret_access_key": s3_secret_access_key,
        }
        if s3_endpoint_url:
            client_kwargs["endpoint_url"] = s3_endpoint_url

        s3 = boto3.client("s3", **client_kwargs)


        max_retries = 3
        base_delay = 2  # seconds
        max_delay = 10  # seconds

        for attempt in range(max_retries):
            try:
                response = s3.get_object(Bucket=s3_bucket, Key=fname)
                return response["Body"].read()
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "NoSuchKey":
                    return super()._file_read(fname)
                _logger.exception(
                    f"Error reading from S3 (attempt {attempt + 1}): {error_code} - {e}"
                )
            except Exception as e:
                _logger.exception(
                    f"Unexpected error reading from S3 (attempt {attempt + 1}): {e}"
                )
            if attempt < max_retries - 1:
                sleep_time = min(
                    max_delay,
                    (base_delay * 2**attempt) * (1 + random.uniform(-0.1, 0.1)),
                )
                time.sleep(sleep_time)
            else:
                super()._file_read(fname)

    def _file_write(self, value, checksum):
        """Write a file to S3, falling back to the local file system if the upload fails."""
        fname, full_path = self._get_path(value, checksum)
        res = self._store_file_write(fname, value)
        if not res:
            fname = super()._file_write(value, checksum)
            _logger.warning(f"Attachment stored locally due to S3 upload failure.")
        return fname
