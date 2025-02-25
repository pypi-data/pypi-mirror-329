#
# utils.py: support utilities
#
# Copyright DeGirum Corporation 2024
# All rights reserved
#

# Functionality:
# set up environment config
# set up task config
# utility to download file from s3 or from file system
# utility to update progress to stdout and optionally to CS/database
# utility to put the result somewhere (bucket/cs/filesystem)

import os
import sys
import traceback
import dotenv
import json
import requests
import logging
import signal
import multiprocessing
from enum import Enum
from typing import Callable, Any, Dict
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from botocore.client import Config as BotoConfig


logger = logging.getLogger(__name__)


class TaskStatus(str, Enum):
    UNKNOWN = "unknown"
    CREATED = "created"
    STARTED = "started"
    IN_PROGRESS = "inprogress"
    DONE = "done"
    FAILED = "failed"


EXIT_CODE_MESSAGES = {
    0: "Process completed successfully.",
    1: "Process terminated with a general error.",
    -signal.SIGTERM: "Process terminated by SIGTERM signal.",
    -signal.SIGSEGV: "Process terminated by SIGSEGV (segmentation fault).",
    -signal.SIGABRT: "Process terminated by SIGABRT signal.",
}
if sys.platform != "win32":
    EXIT_CODE_MESSAGES[-signal.SIGKILL] = "Process killed by SIGKILL signal."


class Config:
    """
    System configuration (obtained from environment variables)
    """

    def __init__(self, config_dir):
        if os.path.isfile(config_dir + "/.env"):
            dotenv.load_dotenv(config_dir + "/.env")

        self.in_cloud: bool = os.environ.get("IN_CLOUD", False) in [
            "True",
            "true",
            "TRUE",
            "1",
        ]
        """ True if running in the cloud, False otherwise """

        self.task_id: str = os.environ.get("TASK_ID", "")
        """ Unique task ID string """

        self.cloud_server_token: str = os.environ.get("CLOUD_SERVER_TOKEN", "")
        """ Cloud API access token """

        self.cloud_server_hostname: str = os.environ.get("CLOUD_SERVER_HOSTNAME", "")
        """ Cloud server hostname """

        self.s3_bucket: str = os.environ.get("S3_BUCKET", "")
        """ S3 bucket path """

        self.s3_access_key_id: str = os.environ.get("S3_ACCESS_KEY_ID", "")
        """ S3 bucket access key ID """

        self.s3_secret_access_key: str = os.environ.get("S3_SECRET_ACCESS_KEY", "")
        """ S3 bucket secret access key """

        self.s3_region_name: str = os.environ.get("S3_REGION_NAME", "")
        """ S3 bucket region name """

        self.s3_endpoint_url: str = os.environ.get("S3_ENDPOINT_URL", "")
        """ S3 bucket endpoint URL """


class TaskRunner:
    """
    Task runner class: provides task running functionality as a separate process
    with proper error handling, and a set of helper methods for interacting with
    the cloud server and S3 buckets.
    """

    def __init__(self, data_dir: str, config_dir: str):
        """
        Constructor: initialize the task runner with the given data and config directories.
        Args:
            data_dir (str): The directory where task data is stored
            config_dir (str): The directory where task configuration is stored
        """

        self.data_dir: str = data_dir
        self.config_dir: str = config_dir
        self.current_status: TaskStatus = TaskStatus.UNKNOWN

        self.config = Config(self.config_dir)  # load config from environment variables

        # load task parameters from JSON file
        with open(self.config_dir + "/parameters.json") as f:
            self.parameters = json.load(f)

        # initialize S3 client when in cloud
        if self.config.in_cloud:
            self.s3 = boto3.client(
                "s3",
                endpoint_url=self.config.s3_endpoint_url,
                aws_access_key_id=self.config.s3_access_key_id,
                aws_secret_access_key=self.config.s3_secret_access_key,
                config=BotoConfig(signature_version="s3v4"),
                region_name=self.config.s3_region_name,
            )
        else:
            self.s3 = None

    def update_status(
        self,
        status: TaskStatus,
        progress: float,
        details: str,
        result: Dict[str, Any] = {},
    ):
        """
        Update the task status in the cloud server with the given parameters.
        Args:
            status (TaskStatus): The task status
            progress (float): The task progress (0-100%)
            details (str): Additional details about the task status (arbitrary string)
            result (dict): The task result dictionary (pass when task status is DONE)
        """

        logger.info(
            f"---------\nSTATUS: {status}\nPROGRESS: {progress}\nDETAILS: {details}\nRESULT: {result}\n---------"
        )
        self.current_status = status

        if self.config.in_cloud:
            # update progress in cloud server
            assert self.config.cloud_server_token
            headers = {"token": self.config.cloud_server_token}
            data = {
                "progress": progress,
                "status": status.value,
                "progress_details": details,
                "result": json.dumps(result),
            }
            r = requests.patch(
                f"{self.config.cloud_server_hostname}/tasks/api/v1/altb/tasks/{self.config.task_id}",
                headers=headers,
                json=data,
            )
            r.raise_for_status()

    def upload_file_to_s3(self, local_path: str, s3_path: str):
        """
        Upload the given file to the S3 bucket.
        When not in the cloud (self.config.in_cloud is False), this method does nothing.
        Args:
            local_path (str): The local file path to upload
            s3_path (str): The S3 path suffix to upload the file to;
                final path in bucket will be `<task ID>/outputs/<s3_path>`
        """
        if self.config.in_cloud:
            assert self.config.task_id
            try:
                # send to s3 bucket
                self.s3.upload_file(
                    str(local_path),
                    self.config.s3_bucket,
                    self.config.task_id + "/outputs/" + s3_path,
                )
            except NoCredentialsError:
                logger.info("Credentials not available")
                raise
            except PartialCredentialsError:
                logger.info("Incomplete credentials provided")
                raise
            except Exception as e:
                logger.info(f"Error downloading file: {e}")
                raise
        else:
            pass

    def upload_dir_to_s3(self, local_path: str, s3_path: str = ""):
        """
        Upload the given directory to the S3 bucket.
        When not in the cloud (self.config.in_cloud si False), this method does nothing.
        Args:
            local_path (str): The local directory path to upload
            s3_path (str): The S3 path suffix to upload the directory to;
                final path in bucket will be `<task ID>/outputs/<s3_path>/<relative path>`
        """
        if self.config.in_cloud:
            try:
                # send to s3 bucket
                for root, _, files in os.walk(local_path):
                    for file in files:
                        full_local_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_local_path, root)
                        self.s3.upload_file(
                            full_local_path,
                            self.config.s3_bucket,
                            self.config.task_id
                            + "/outputs/"
                            + (s3_path + "/" if s3_path else "")
                            + rel_path,
                        )
            except NoCredentialsError:
                logger.info("Credentials not available")
                raise
            except PartialCredentialsError:
                logger.info("Incomplete credentials provided")
                raise
            except Exception as e:
                logger.info(f"Error downloading file: {e}")
                raise
        else:
            pass

    def download_inputs_from_s3(self, local_path: str):
        """
        Download all input files from the S3 bucket to the given local directory.
        Path in bucket is `<task ID>/inputs/`.

        When not in the cloud (self.config.in_cloud si False), this method
        just returns the list of files in the `local_path`.

        Args:
            local_path (str): The local directory path to download the files to
        Returns:
            list: The list of downloaded file paths
        """

        downloaded_files = []
        if self.config.in_cloud:
            # Create download path if it does not exist
            if not os.path.exists(local_path):
                os.makedirs(local_path)

            # List objects in the S3 bucket
            objects = self.s3.list_objects_v2(
                Bucket=self.config.s3_bucket, Prefix=self.config.task_id + "/inputs/"
            )
            # Download each object
            for obj in objects.get("Contents", []):
                key = obj["Key"]
                file_name = key.split("/")[-1]
                file_path = os.path.join(local_path, file_name)

                # Create subdirectories if needed
                if not os.path.exists(os.path.dirname(file_path)):
                    os.makedirs(os.path.dirname(file_path))

                self.s3.download_file(self.config.s3_bucket, key, file_path)
                downloaded_files.append(file_path)
        else:
            for root, dirs, files in os.walk(local_path):
                for file in files:
                    downloaded_files.append(os.path.join(local_path, file))
        return downloaded_files

    def upload_model_to_cloud_zoo(self, model_zip_path: str, zoo_url: str):
        """This function uploads the model to the model zoo.

        Args:
            model_zip_path (str): The path to the zipfile containing the files: N2X Binary, JSON Configuration File, and Labels File.
            zoo_url (str): zoo url in format of 'zoo_owner/zoo_name'

        Returns:
            None
        """
        if self.config.in_cloud:
            url = self.config.cloud_server_hostname + f"/zoo/v1/public/models/{zoo_url}"

            headers = {
                "accept": "application/json",
                "token": self.config.cloud_server_token,
            }

            with open(model_zip_path, "rb") as f:
                try:
                    response = requests.post(url, headers=headers, files={"file": f})
                    response.raise_for_status()
                except Exception as e:
                    logger.info(f"Error uploading model: {response.json()}")
                    raise e
        else:
            pass

    def run(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        """
        Run the given callable in a separate process with proper error handling,
        passing to it the task runner instance and all additional arguments.
        """

        parent_conn, child_conn = multiprocessing.Pipe()

        def process_target(conn, *args, **kwargs):
            try:
                func_output = func(self, *args, **kwargs)
                conn.send((0, None, None, func_output))  # Send success status
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                tb = traceback.format_exc()
                conn.send((1, str(e), tb, None))  # Send error status and traceback

        process = multiprocessing.Process(
            target=process_target, args=(child_conn, *args), kwargs=kwargs
        )
        process.start()
        process.join()  # Wait for the process to finish

        # Retrieve exit code and diagnostic information
        if parent_conn.poll():
            status, error_msg, tb, func_output = parent_conn.recv()
            self.runner_output = func_output
            if status == 0:
                logger.info(f"Process for {func.__name__} completed successfully.")
            else:
                self.update_status(
                    TaskStatus.FAILED,
                    0,
                    "An error occurred",
                    {"result": "FAILED", "error": error_msg, "traceback": tb},
                )
                logger.info(
                    f"Process for {func.__name__} exited with an error: {error_msg}\nTraceback:\n{tb}"
                )
        else:
            exit_code = process.exitcode
            self.update_status(
                TaskStatus.FAILED,
                0,
                "An error occurred",
                {"result": "FAILED", "error_code": exit_code},
            )
            if exit_code in EXIT_CODE_MESSAGES:
                logger.info(
                    f"Process for {func.__name__} exited with code {exit_code}: {EXIT_CODE_MESSAGES[exit_code]}"
                )
            else:
                logger.info(
                    f"Process for {func.__name__} exited with an unknown error code {exit_code}."
                )
