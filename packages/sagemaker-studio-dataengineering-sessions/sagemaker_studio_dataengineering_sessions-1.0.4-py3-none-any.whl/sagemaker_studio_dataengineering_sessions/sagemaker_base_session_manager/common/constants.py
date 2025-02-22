import os
from enum import Enum, unique

from sagemaker_studio_dataengineering_sessions.sagemaker_base_session_manager.common.metadata_utils import retrieve_sagemaker_metadata_from_file

# Metadata key definition is in LooseLeafWorkflowsLambda
# https://code.amazon.com/packages/LooseLeafWorkflowsLambda/blobs/mainline/--/src/com/amazon/looseleafworkflowslambda/job/MaxDomeMetadataHelper.java


def _get_datazone_domain_id(metadata) -> str | None:
    if metadata and 'AdditionalMetadata' in metadata and 'DataZoneDomainId' in metadata['AdditionalMetadata']:
        return metadata['AdditionalMetadata']['DataZoneDomainId']
    domain_id = os.getenv(DATAZONE_DOMAIN_ID_ENV, None)
    return domain_id


def _get_datazone_project_id(metadata) -> str | None:
    if metadata and 'AdditionalMetadata' in metadata and 'DataZoneProjectId' in metadata['AdditionalMetadata']:
        return metadata['AdditionalMetadata']['DataZoneProjectId']
    project_id = os.getenv(DATAZONE_PROJECT_ID_ENV, None)
    return project_id

def _get_datazone_environment_id(metadata) -> str | None:
    if metadata and 'AdditionalMetadata' in metadata and 'DataZoneEnvironmentId' in metadata['AdditionalMetadata']:
        return metadata['AdditionalMetadata']['DataZoneEnvironmentId']
    return os.getenv(DATAZONE_ENVIRONMENT_ID_ENV, None)

def _get_datazone_stage(metadata) -> str | None:
    if metadata and 'AdditionalMetadata' in metadata and 'DataZoneStage' in metadata['AdditionalMetadata']:
        return metadata['AdditionalMetadata']['DataZoneStage']
    return os.getenv(DATAZONE_STAGE_ENV, None)

def _get_datazone_endpoint_url(metadata) -> str | None:
    if metadata and 'AdditionalMetadata' in metadata and 'DataZoneEndpoint' in metadata['AdditionalMetadata']:
        return metadata['AdditionalMetadata']['DataZoneEndpoint']
    datazone_endpoint = os.getenv(DATAZONE_ENDPOINT_ENV, None)
    return datazone_endpoint

def _get_project_s3_path(metadata) -> str | None:
    if metadata and 'AdditionalMetadata' in metadata and 'ProjectS3Path' in metadata['AdditionalMetadata']:
        return metadata['AdditionalMetadata']['ProjectS3Path']
    return os.getenv(PROJECT_S3_PATH_ENV, None)


def _get_datazone_region(metadata) -> str | None:
    if metadata and 'AdditionalMetadata' in metadata and 'DataZoneDomainRegion' in metadata['AdditionalMetadata']:
        return metadata['AdditionalMetadata']['DataZoneDomainRegion']
    datazone_region = os.getenv(DATAZONE_DOMAIN_REGION_ENV, None)
    return datazone_region

def _get_execution_role_arn(metadata) -> str | None:
    if metadata and metadata['ExecutionRoleArn']:
        return metadata['ExecutionRoleArn']
    return os.getenv(EXECUTION_ROLE_ARN_ENV, None)

def _get_lib_path() -> str:
     path = os.getenv(SM_PROJECT_FILES_PATH_ENV, default=os.path.expanduser("~/src"))
     return '/'.join([path, '.libs.json'])

AWS_REGION_ENV = "AWS_REGION"

CONNECTION_TYPE_ATHENA = "ATHENA"
CONNECTION_TYPE_REDSHIFT = "REDSHIFT"
CONNECTION_TYPE_SPARK_EMR_EC2 = "SPARK_EMR_EC2"
CONNECTION_TYPE_SPARK_GLUE = "SPARK_GLUE"
CONNECTION_TYPE_SPARK_EMR_SERVERLESS = "SPARK_EMR_SERVERLESS"
CONNECTION_TYPE_IAM = "IAM"
CONNECTION_TYPE_GENERAL_SPARK = "SPARK"


CONNECTION_TYPE_SPARK = [CONNECTION_TYPE_SPARK_EMR_SERVERLESS,
                         CONNECTION_TYPE_SPARK_EMR_EC2,
                         CONNECTION_TYPE_SPARK_GLUE]

CONNECTION_TYPE_NOT_SPARK = [CONNECTION_TYPE_ATHENA,
                             CONNECTION_TYPE_REDSHIFT,
                             CONNECTION_TYPE_IAM]

#
# https://code.amazon.com/packages/MaxDomePythonSDK/blobs/c99d3f86a92ba86f6f5c84e2509a2870d955e44c/--/src/maxdome/execution/remote_execution_client.py#L396-L399
DATAZONE_DOMAIN_ID_ENV = "DataZoneDomainId"
DATAZONE_DOMAIN_REGION_ENV = "DataZoneDomainRegion"
DATAZONE_PROJECT_ID_ENV = "DataZoneProjectId"
DATAZONE_ENVIRONMENT_ID_ENV = "DataZoneEnvironmentId"
DATAZONE_STAGE_ENV = "DataZoneStage"
DATAZONE_ENDPOINT_ENV = "DataZoneEndpoint"
PROJECT_S3_PATH_ENV = "ProjectS3Path"
SM_PROJECT_FILES_PATH_ENV = "SM_PROJECT_FILES_PATH"

DOMAIN_EXECUTION_ROLE_PROFILE_NAME = "DomainExecutionRoleCreds"
EXECUTION_ROLE_ARN_ENV = "ExecutionRoleArn"

SAGEMAKER_DEFAULT_CONNECTION_NAME = "project.iam"
SAGEMAKER_DEFAULT_CONNECTION_DISPLAYNAME = "project.python"
SAGEMAKER_DEFAULT_GLUE_CONNECTION_NAME = "project.spark"
SAGEMAKER_DEFAULT_ATHENA_CONNECTION_NAME = "project.athena"
SAGEMAKER_DEFAULT_REDSHIFT_CONNECTION_NAME = "project.redshift"

GET_IPYTHON_SHELL = "get_ipython()"
METADATA_CONTENT = retrieve_sagemaker_metadata_from_file()

DOMAIN_ID = _get_datazone_domain_id(METADATA_CONTENT)
PROJECT_ID = _get_datazone_project_id(METADATA_CONTENT)
DATAZONE_ENDPOINT_URL = _get_datazone_endpoint_url(METADATA_CONTENT)
DATAZONE_DOMAIN_REGION = _get_datazone_region(METADATA_CONTENT)
DATAZONE_STAGE = _get_datazone_stage(METADATA_CONTENT)
DATAZONE_ENVIRONMENT_ID = _get_datazone_environment_id(METADATA_CONTENT)
PROJECT_S3_PATH = _get_project_s3_path(METADATA_CONTENT)
EXECUTION_ROLE_ARN = _get_execution_role_arn(METADATA_CONTENT)
LIB_PATH = _get_lib_path()

@unique
class Language(Enum):
    def __new__(cls, value, supporting_connections):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._supporting_connections = supporting_connections
        return obj

    python = ("python", [CONNECTION_TYPE_SPARK_EMR_EC2,
                         CONNECTION_TYPE_SPARK_GLUE,
                         CONNECTION_TYPE_IAM,
                         CONNECTION_TYPE_SPARK_EMR_SERVERLESS])
    scala = ("scala", [CONNECTION_TYPE_SPARK_EMR_EC2,
                       CONNECTION_TYPE_SPARK_GLUE,
                       CONNECTION_TYPE_SPARK_EMR_SERVERLESS])
    sql = ("sql", [CONNECTION_TYPE_ATHENA,
                   CONNECTION_TYPE_REDSHIFT,
                   CONNECTION_TYPE_SPARK_EMR_EC2,
                   CONNECTION_TYPE_SPARK_GLUE,
                   CONNECTION_TYPE_SPARK_EMR_SERVERLESS])

    def supports_connection_type(self, connection_type: str) -> bool:
        if connection_type in self._supporting_connections:
            return True
        return False

