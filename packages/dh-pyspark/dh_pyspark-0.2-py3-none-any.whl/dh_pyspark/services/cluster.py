import json
import time
import inspect
import textwrap
from google.cloud import dataproc_v1, storage
import google.api_core.exceptions


class GoogleCloudCluster:
    def __init__(self, project_id, region, destination_path, cluster_config):
        self.project_id = project_id
        self.region = region
        self.destination_path = destination_path
        self.cluster_config = cluster_config

        self.workflow_template_id = f"wf-tmpl-id-{round(time.time())}"
        self.cluster_name = f"cluster-id-{round(time.time())}"
        self.bucket_name = destination_path.split('/')[0]
        self.folder_path = "/".join(destination_path.split('/')[1:] + [self.workflow_template_id])

        # ✅ Set the regional API endpoint for Dataproc
        client_options = {"api_endpoint": f"{region}-dataproc.googleapis.com:443"}
        self.workflow_template_client = dataproc_v1.WorkflowTemplateServiceClient(client_options=client_options)

    @staticmethod
    def get_function_body(func):
        try:
            source_code = inspect.getsource(func)
            lines = source_code.split("\n")
            body = "\n".join(lines[1:])
            return textwrap.dedent(body).strip()
        except (TypeError, OSError):
            print(f"❌ Unable to retrieve source code for '{function_name}'.")
            return None

    def get_wrapped_function(self,  func):
        function_body = self.get_function_body(func)
        if function_body:
            return f"""
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("{func.__name__}").getOrCreate()

def main():
{textwrap.indent(function_body, "    ")}

if __name__ == "__main__":
    main()
    """
        return None

    @staticmethod
    def upload_text_to_gcs(bucket_name, destination_file_name, text):
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_file_name)
        blob.upload_from_string(text, content_type="text/plain")
        gcs_path = f"gs://{bucket_name}/{destination_file_name}"
        print(f"✅ Text uploaded to: {gcs_path}")
        return gcs_path

    @staticmethod
    def upload_file_to_gcs(bucket_name, source_file_path, destination_file_name):
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_file_name)
        blob.upload_from_filename(source_file_path)
        print(f"✅ File {source_file_path} uploaded to gs://{bucket_name}/{destination_file_name}")

    def create_and_run_workflow(self, workflow_steps):
        pip_packages = "dataheroes pyarrow scikit-learn==1.4.2 dh_pyspark"
        init_text = f"""
#!/bin/bash
# echo "Initializing cluster and installing dependencies..." >> /var/log/init.log
# Upgrade pip
# python3 -m pip install --upgrade pip >> /var/log/init.log 2>&1
# Install packages
python3 -m pip install {pip_packages} >> /var/log/init.log 2>&1
echo "Dependencies installed successfully." >> /var/log/init.log
"""

        # Upload initialization script
        initial_script_path = self.upload_text_to_gcs(
            bucket_name=self.bucket_name,
            destination_file_name=f"{self.folder_path}/initialization.sh",
            text=f"python3 -m pip install {pip_packages} >> /var/log/init_script.log"
        )

        previous_step = None
        jobs = []

        for workflow_step in workflow_steps:
            step_name = workflow_step.__name__
            exec_name = self.upload_text_to_gcs(
                bucket_name=self.bucket_name,
                destination_file_name=f"{self.folder_path}/{step_name}.py",
                text=self.get_wrapped_function(workflow_step)
            )
            step_config = {
                "step_id": step_name,
                "pyspark_job": {
                    "main_python_file_uri": exec_name,
                    "args": ["arg1", "arg2"],
                    "file_uris": [initial_script_path]
                }
            }
            if previous_step:
                step_config["prerequisite_step_ids"] = [previous_step]

            jobs.append(step_config)
            previous_step = step_name

        self.cluster_config['config']['initialization_actions'] = [{
            "executable_file": initial_script_path,
            "execution_timeout": "2000s"
        }]

        self.cluster_config['config']['gce_cluster_config'] = {
            "metadata": {"PIP_PACKAGES": pip_packages},
            "internal_ip_only": False
        }
        workflow_template = {
            "id": self.workflow_template_id,
            "placement": {
                "managed_cluster": {
                    "cluster_name": self.cluster_name,
                    **self.cluster_config,
                }
            },
            "jobs": jobs,
        }

        print("============ Workflow Template ============================")
        print(json.dumps(workflow_template, indent=2))
        print("===========================================================")

        request = dataproc_v1.CreateWorkflowTemplateRequest(
            parent=f"projects/{self.project_id}/regions/{self.region}",
            template=workflow_template,
        )

        try:
            self.workflow_template_client.create_workflow_template(request=request)
            print(f"Workflow template created: {self.workflow_template_id}")
        except google.api_core.exceptions.AlreadyExists:
            print(f"Workflow template already exists: {self.workflow_template_id}")

        request = dataproc_v1.InstantiateWorkflowTemplateRequest(
            name=f"projects/{self.project_id}/regions/{self.region}/workflowTemplates/{self.workflow_template_id}"
        )

        operation = self.workflow_template_client.instantiate_workflow_template(request=request)
        operation.result()

        print(f"Workflow template instantiated: {self.workflow_template_id}")
