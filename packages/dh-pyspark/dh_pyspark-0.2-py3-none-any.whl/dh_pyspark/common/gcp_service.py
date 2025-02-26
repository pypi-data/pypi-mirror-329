import datetime
import logging
import os
import shutil
import zipfile
from dataclasses import dataclass
from typing import List, Dict

import toml
from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage
from google.protobuf.duration_pb2 import Duration

from test.dh_pyspark.utils import delete_all_files


@dataclass
class JobParams:
    job_name: str
    spark_config: Dict = None
    prerequisite_job_names: List[str] = None
    job_args: List[str] = None


class GCPService:
    def __init__(self, config_path) -> None:
        self.config = toml.load(config_path)

        self.logger = self.setup_logger()
        self.cluster_config = self.config['cluster']
        self.cluster_name = self.cluster_config['cluster_name']
        self.spark_step_name = f'step_{self.cluster_name}_{datetime.datetime.now()}'
        self.region = self.cluster_config['region']
        self.project_id = self.cluster_config['project_id']
        self.bootstrap_script = self.cluster_config['bootstrap_script']
        self.code_location = self.cluster_config['code_location']
        self.bucket_name = self.cluster_config['bucket_name']
        self.history_server_folder = self.cluster_config['history_server_folder']
        client_options = {'api_endpoint': f'{self.region}-dataproc.googleapis.com:443'}
        self.cluster_client = dataproc.ClusterControllerClient(client_options=client_options)
        self.workflow_client = dataproc.WorkflowTemplateServiceClient(client_options=client_options)
        self.job_client = dataproc.JobControllerClient(client_options=client_options)
        self.storage_client = storage.Client()

    def setup_logger(self, write_to_file=False):

        logger = logging.getLogger("GCP Run")
        logger.setLevel(logging.DEBUG)
        # Create a stream handler to display log messages on the terminal
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(console_formatter)
        if write_to_file:
            log_folder = "Logs"
            os.makedirs(log_folder, exist_ok=True)
            # Generate a timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            # Set up the logger
            log_file = os.path.join(log_folder, f"logfile_{timestamp}_.log")
            fileHandler = logging.FileHandler(log_file)
            fileHandler.setLevel(logging.DEBUG)
            logger.addHandler(fileHandler)
        # Add the stream handler to the logger
        logger.addHandler(console_handler)

        return logger

    def get_logger(self):
        return self.logger

    def check_cluster_exists(self):

        cluster = self.cluster_client.get_cluster(
            request={'project_id': self.project_id, 'region': self.region, 'cluster_name': self.cluster_name})
        return cluster.cluster_uuid

    def deploy_cluster(self, cluster_id=None):
        if cluster_id is not None:
            self.logger.info(f"Cluster with ID: {cluster_id} already exists")
            return cluster_id

        cluster = self.define_cluster()
        self.logger.info(f"Creating cluster with name: {self.cluster_name}")
        operation = self.cluster_client.create_cluster(
            request={'project_id': self.project_id, 'region': self.region, 'cluster': cluster})
        result = operation.result()
        self.logger.info(f"Cluster created with ID: {result.cluster_uuid}")
        self.cluster_id = result.cluster_uuid
        return result.cluster_uuid

    def define_cluster(self, run_id=None):
        cluster = {
            'project_id': self.project_id,
            'cluster_name': self.cluster_name,
            'config': self.define_cluster_config(run_id=run_id)
        }
        # Create the cluster
        return cluster

    def define_cluster_config(self, run_id=None):
        history_sever_path = self.history_server_folder
        if run_id is not None:
            history_sever_path = os.path.join(self.history_server_folder, run_id)
        claster_config = {
            'gce_cluster_config': {
                'zone_uri': f'{self.region}-a',
                'service_account': self.cluster_config['service_account'],
                # 'network_uri': self.configuration['network'],
                'subnetwork_uri': self.cluster_config['subnet'],
                'internal_ip_only': False,
                'metadata': {
                    'owner': self.cluster_config['owner'],
                }
            },
            'master_config': {
                'num_instances': int(self.cluster_config['master_instance_count']),
                'machine_type_uri': self.cluster_config['master_instance_type'],
            },
            'worker_config': {
                'num_instances': int(self.cluster_config['worker_instance_count']),
                'machine_type_uri': self.cluster_config['worker_instance_type'],
                "disk_config": {
                    "boot_disk_type": self.cluster_config["worker_boot_disk_type"],
                    "boot_disk_size_gb": int(self.cluster_config["worker_boot_disk_size_gb"]),
                }
            },
            'software_config': {
                'image_version': '2.2-ubuntu22',
                'properties': {
                    'dataproc:dataproc.allow.zero.workers': 'true',
                    'spark:spark.history.fs.logDirectory': f"gs://{self.bucket_name}/{history_sever_path}"
                },
                'optional_components': ['JUPYTER']

            },
            'endpoint_config': {
                'enable_http_port_access': True
            },
            # "lifecycle_config": {
            #     "idle_delete_ttl": Duration(seconds=self.cluster_config["idleDeleteTtl_sec"])
            # },
            'initialization_actions': [{
                'executable_file': self.bootstrap_script,
                'execution_timeout': Duration(seconds=1600)
            }]
        }
        return claster_config

    def create_job(self, main_job_file, job_args=None, spark_conf=None, upload_code=True, terminate=True,
                   cluster_id=None, step_id=None, wait_for_results=True):
        # package code
        bucket_name = self.bucket_name
        # save_folder = config['experiment']['save_folder']
        logger = self.get_logger()
        logger.info(f"Packaging code")
        deploy_dir, job_files = self.package_code(main_files=[main_job_file])
        cluster_id = self.deploy_cluster(cluster_id=cluster_id)
        if upload_code:
            gcs_code_loc = self.upload_folder_to_gcs(deploy_dir, bucket_name)
            python_files = [f"{gcs_code_loc}/{file}" for file in job_files]
        else:
            python_files = job_files
        run_script = [file_name for file_name in python_files if "main.py" in file_name][0]
        archive_file = [file_name for file_name in python_files if ".zip" in file_name][0]
        spark_config = self.config["spark_config"]
        spark_config.update(spark_conf)
        job = {
            'placement': {
                'cluster_uuid': cluster_id,
                'cluster_name': self.cluster_name
            },
            'pyspark_job': {
                'main_python_file_uri': run_script,
                'python_file_uris': [archive_file],
                'properties': spark_config,
                'args': job_args
            }
        }
        if step_id is not None:
            try:
                step_id = self.get_job(step_id)
            except Exception as e:
                logger.info(f"Error getting job {step_id} \n {e} \n Submitting new job")
                step_id = self.submit_job(job, wait_for_results)
        else:
            step_id = self.submit_job(job, wait_for_results)

        # cluster.download_file_from_gcs(bucket_name, save_folder, SAVE_FILE)
        if terminate:
            self.delete_cluster()
        return step_id, cluster_id

    def upload_folder_to_gcs(self, local_folder, bucket_name, run_id=None):
        """
        Uploads a local folder to GCS with the folder name being the current datetime.
        Returns the GCS folder path.

        """

        if run_id is None:
            now = datetime.datetime.now()
            run_id = now.strftime("%Y-%m-%d-%H-%M-%S")
        save_folder = run_id

        storage_client = self.storage_client
        bucket = storage_client.bucket(bucket_name)
        gcs_folder: str = f"{self.code_location}/{save_folder}/"

        for root, _, files in os.walk(local_folder):
            for file in files:
                local_path: str = os.path.join(root, file)
                relative_path: str = os.path.relpath(local_path, local_folder)
                blob_path = os.path.join(gcs_folder, relative_path)
                blob = bucket.blob(blob_path)
                blob.upload_from_filename(local_path)
                print(f"Uploaded {local_path} to gs://{bucket_name}/{blob_path}")

        return f"gs://{bucket_name}/{gcs_folder}"

    def create_folder(self, bucket_name, folder_name):
        # Initialize a storage client
        client = self.storage_client
        # Get the bucket
        bucket = client.bucket(bucket_name)
        # Create a new blob with a trailing slash to represent a folder
        blob = bucket.blob(folder_name + "/")
        # Upload an empty string to create the folder
        blob.upload_from_string('')

        self.logger.info(f"Created folder {folder_name} in bucket {bucket_name}.")

    def upload_file_to_gcs(self, bucket_name, local_file):
        """
        Uploads a local file to GCS with the folder name being the current datetime.
        Returns the GCS folder path.

        """
        now = datetime.datetime.now()
        save_folder = now.strftime("%Y_%m_%d_%H_%M/")
        storage_client = self.storage_client
        bucket = storage_client.bucket(bucket_name)
        gcs_folder = f"{self.code_location}/{save_folder}/"

        relative_path = os.path.basename(local_file)
        blob_path = os.path.join(gcs_folder, relative_path)
        blob = bucket.blob(blob_path)
        blob.upload_from_filename(local_file)
        print(f"Uploaded {local_file} to gs://{bucket_name}/{blob_path}")

        return f"gs://{bucket_name}/{gcs_folder}"

    def download_file_from_gcs(self, bucket_name, gcs_path, filename):
        storage_client = self.storage_client
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(gcs_path)
        blob.download_to_filename(filename)
        print(f"Downloaded gs://{bucket_name}/{gcs_path} to {filename}")

    def submit_job(self, job, wait_for_results=True):

        self.logger.info(f"Submitting job to cluster with ID: {self.cluster_id}")
        operation = self.job_client.submit_job_as_operation(
            request={
                'project_id': self.project_id,
                'region': self.region,
                'job': job,
            }
        )
        self.logger.info(f"Job submitted with ID {operation.metadata.job_id}. Waiting for job to complete...")
        if wait_for_results:
            result = operation.result(timeout=None)
            return result.reference.job_id
        else:
            return operation.metadata.job_id

    def get_job(self, job_id):

        job = self.job_client.get_job(request={'project_id': self.project_id, 'region': self.region, 'job_id': job_id})
        return job

    def delete_cluster(self):

        op = self.cluster_client.delete_cluster(
            request={'project_id': self.project_id, 'region': self.region, 'cluster_name': self.cluster_name})
        result = op.result()
        self.logger.info(f"Cluster deleted succesfully: {result}")

    def zipdir(self, path, ziph):
        # Zip the entire folder and its subfolders
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.join(path, '..'))
                ziph.write(file_path, arcname)

    def create_zip(self, folder_path, zip_path):
        # Create a ZIP file from the specified folder
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            self.zipdir(folder_path, zipf)

    def package_code(self, main_files):
        project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        zip_dir = os.path.join(project_dir, "dh_pyspark")
        deploy_dir = os.path.join(project_dir, "deploy")
        delete_all_files(deploy_dir)
        # Copy files to zip_path
        if not os.path.exists(deploy_dir):
            os.makedirs(deploy_dir)
        pyspark_zip = "dh_pyspark.zip"
        self.create_zip(folder_path=zip_dir, zip_path=os.path.join(deploy_dir, pyspark_zip))

        for file in main_files:
            shutil.copy(os.path.join(project_dir, file), deploy_dir)
        main_files.append(pyspark_zip)
        return deploy_dir, main_files

    def download_folder(self, bucket_name, folder_name, local_path):
        # Initialize a storage client
        client = self.storage_client

        # Get the bucket
        bucket = client.bucket(bucket_name)

        # List all objects in the folder
        blobs = bucket.list_blobs(prefix=folder_name)

        for blob in blobs:
            # Create local directories as needed
            local_file_path = os.path.join(local_path, blob.name)
            local_dir = os.path.dirname(local_file_path)
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)

            # Download the file
            blob.download_to_filename(local_file_path)
            print(f"Downloaded {blob.name} to {local_file_path}")

    def create_workflow(self, main_job_file, jobs_params: List[JobParams], run_id=None, run_template=True,
                        delete_template=True):
        if run_id is None:
            now = datetime.datetime.now()
            run_id = now.strftime("%Y-%m-%d-%H-%M-%S")
        project_id = self.project_id
        region = self.region
        template_id = run_id
        logger = self.get_logger()
        logger.info(f"Packaging code")
        # crating a zip library if the code
        deploy_dir, job_files = self.package_code(main_files=[main_job_file])
        bucket_name = self.cluster_config["bucket_name"]
        # uploding code to cod repo in the gcp storage
        gcs_code_loc = self.upload_folder_to_gcs(deploy_dir, bucket_name, run_id)
        python_files = [f"{gcs_code_loc}/{file}" for file in job_files]

        run_script = [file_name for file_name in python_files if main_job_file in file_name][0]
        archive_file = [file_name for file_name in python_files if ".zip" in file_name][0]
        spark_config = self.config["spark_config"]
        # seting all history server logs under the work flow run id
        history_server_folder_run_id = os.path.join(self.history_server_folder, run_id)
        spark_config["spark.eventLog.dir"] = f"gs://{self.bucket_name}/{history_server_folder_run_id}"
        self.create_folder(self.bucket_name, history_server_folder_run_id)
        # Define the workflow template request
        template = {
            "id": template_id,
            # "name": "myWorkFlwe",
            "labels": {},
            "placement": {
                "managed_cluster": {
                    "cluster_name": self.cluster_config["cluster_name"],
                    "config": self.define_cluster_config(run_id=run_id),

                    "labels": {
                        "owner": self.cluster_config["owner"],
                        "run_id": run_id
                    }
                }
            },
            "jobs": [],
            "parameters": []
        }
        # define template jobs
        jobs = []
        for job_param in jobs_params:
            job_param.spark_config.update(spark_config)
            job = {
                "pyspark_job": {
                    "main_python_file_uri": run_script,
                    "python_file_uris": [archive_file],
                    # "jar_file_uris": [],
                    # "file_uris": [],
                    # "archive_uris": [],
                    "properties": job_param.spark_config,
                    "args": job_param.job_args
                },
                "step_id": job_param.job_name,
                "labels": {"run_id": run_id},
                "prerequisite_step_ids": job_param.prerequisite_job_names
            }
            jobs.append(job)

        template["jobs"] = jobs

        # Create the workflow template
        parent = f"projects/{project_id}/regions/{region}"
        response = self.workflow_client.create_workflow_template(parent=parent, template=template)
        # client.instantiate_inline_workflow_template()

        # Get the template ID for submission
        template_name = response.name
        self.logger.info(f"Workflow Template created with ID: {template_name}")
        if run_template:
            self.run_workflow(template_id=template_id)
        if delete_template:
            self.delete_workflow(template_id=template_id)

        return template_id

    def run_workflow(self, template_id):

        name = f'projects/{self.project_id}/regions/{self.region}/workflowTemplates/{template_id}'
        # Instantiate the workflow template
        operation = self.workflow_client.instantiate_workflow_template(name=name)
        self.logger.info(f'Instantiated workflow template {template_id}.')

        # Optional: Get the operation's result to ensure it completed successfully
        response = operation.result(timeout=None)
        self.logger.info(f"f run workflow operation result {response}")
        self.logger.info(f'Workflow template {template_id} completed.')
        return response

    def delete_workflow(self, template_id):

        name = f'projects/{self.project_id}/regions/{self.region}/workflowTemplates/{template_id}'
        # Instantiate the workflow template
        self.workflow_client.delete_workflow_template(name=name)
        self.logger.info(f'deleting workflow template {template_id}.')
