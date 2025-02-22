import abc
import logging

import pandas
from IPython import get_ipython
from sagemaker_studio_dataengineering_sessions.sagemaker_base_session_manager.base_session_manager import BaseSessionManager
from sagemaker_studio_dataengineering_sessions.sagemaker_base_session_manager.common.constants import (Language, DATAZONE_STAGE)
from sagemaker_studio_dataengineering_sessions.sagemaker_base_session_manager.common.glue_gateway import GlueGateway
from sagemaker_studio_dataengineering_sessions.sagemaker_base_session_manager.common.sagemaker_toolkit_utils import SageMakerToolkitUtils
from sagemaker_studio_dataengineering_sessions.sagemaker_spark_session_manager.spark_commands.send_to_spark_command import send_dict_to_spark_command, \
    send_str_to_spark_command, send_pandas_df_to_spark_command, send_datazone_metadata_command
from sagemaker_studio_dataengineering_sessions.sagemaker_spark_session_manager.utils.common_utils import get_glue_endpoint, get_redshift_endpoint
from sagemaker_studio_dataengineering_sessions.sagemaker_spark_session_manager.utils.lib_utils import LibProvider
from sagemaker_studio_dataengineering_sessions.sagemaker_base_session_manager.common.sagemaker_connection_display import SageMakerConnectionDisplay
from botocore.exceptions import ClientError


class SparkSession(BaseSessionManager, metaclass=abc.ABCMeta):
    lib_provider = LibProvider()
    logger = logging.getLogger(__name__)
    auto_add_catalogs = True

    def __init__(self, connection_name):
        super().__init__()
        self.connection_name = connection_name
        aws_location = self._get_connection_aws_location()
        self.region = aws_location["awsRegion"]
        self.account_id = aws_location["awsAccountId"]
        self.glue_endpoint = get_glue_endpoint(self.region, DATAZONE_STAGE)
        self.redshift_endpoint = get_redshift_endpoint(self.region, DATAZONE_STAGE)
        self.glue_client = GlueGateway()
        if DATAZONE_STAGE == "gamma":
            self.glue_client.initialize_clients(region=self.region, endpoint_url=self.glue_endpoint)
        else:
            # Use boto3 default endpoint if stage is not gamma
            self.glue_client.initialize_clients(region=self.region)
        self._gen_default_config()

    def send_to_remote(self, local_var: str, remote_var: str, language=Language.python):
        try:
            local = get_ipython().ev(f"{local_var}")
            if type(local) is dict:
                command = send_dict_to_spark_command(local, remote_var, language)
            elif type(local) is str:
                command = send_str_to_spark_command(local, remote_var, language)
            elif type(local) is pandas.DataFrame:
                command = send_pandas_df_to_spark_command(local, remote_var, language)
            else:
                raise NotImplementedError(f"Local variable {type(local)} is not supported.")
            if not self.is_session_connectable():
                self.create_session()
            self.run_statement(command, language)
        except NameError:
            self.get_logger().error(f"local variable  does not exist.")
            raise RuntimeError(f"local variable {local_var} does not exist.")

    def send_datazone_metadata_to_remote(self, language=Language.python):
        if language == Language.python:
            # Only send metadata if language is python
            command = send_datazone_metadata_command(language)
            self.run_statement(command, language)

    def _configure_core(self, cell):
        raise NotImplementedError('Must define _configure_core to use this configure function.')

    def _get_connection_aws_location(self):
        connection_details = SageMakerToolkitUtils.get_connection_detail(self.connection_name, True)
        return connection_details["physicalEndpoints"][0]["awsLocation"]

    def _gen_default_config(self):
        self.default_config = {
            "conf": {
                "spark.sql.catalog.spark_catalog": "org.apache.iceberg.spark.SparkSessionCatalog",
                "spark.sql.catalog.spark_catalog.catalog-impl": "org.apache.iceberg.aws.glue.GlueCatalog",
                "spark.sql.catalog.spark_catalog.glue.id": self.account_id,
                "spark.sql.catalog.spark_catalog.glue.account-id": self.account_id,
                "spark.sql.catalog.spark_catalog.client.region": self.region,
                "spark.sql.catalog.spark_catalog.glue.endpoint": get_glue_endpoint(self.region),

                "spark.sql.extensions": "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
                "spark.datasource.redshift.community.glue_endpoint": self.glue_endpoint,
                "spark.datasource.redshift.community.data_api_endpoint": self.redshift_endpoint,
                "spark.hadoop.fs.s3.impl": "com.amazon.ws.emr.hadoop.fs.EmrFileSystem"
            }
        }
        if self.auto_add_catalogs:
            self._gen_catalog_config()
        self.logger.info(f"update default configuration: {self.default_config}")

    def _gen_catalog_config(self):
        try:
            catalogs = self.glue_client.get_catalogs()
            conf = self.default_config['conf']
            for catalog in catalogs:
                if (catalog['CatalogType'] == "FEDERATED"
                        and catalog['FederatedCatalog']['ConnectionName'] != "aws:s3tables"):
                    pass
                else:
                    # Confirmed with glue team. If a catalog hierarchy looks like level_1 -> level_2 -> level_3 -> dev
                    # The ParentCatalogNames list of catalog dev would be
                    # index 0: level_1
                    # index 1: level_2
                    # index 2: level_3
                    catalog_name = "_".join(catalog['ParentCatalogNames'])
                    catalog_name = f"{catalog_name}_{catalog['Name']}" if catalog_name else catalog['Name']
                    conf[f"spark.sql.catalog.{catalog_name}"] = "org.apache.iceberg.spark.SparkCatalog"
                    conf[f"spark.sql.catalog.{catalog_name}.catalog-impl"]\
                        = "org.apache.iceberg.aws.glue.GlueCatalog"
                    conf[f"spark.sql.catalog.{catalog_name}.glue.id"] = f"{catalog['CatalogId']}"
                    conf[f"spark.sql.catalog.{catalog_name}.glue.catalog-arn"] = f"{catalog['ResourceArn']}"
                    conf[f"spark.sql.catalog.{catalog_name}.glue.endpoint"] = self.glue_endpoint
                    conf[f"spark.sql.catalog.{catalog_name}.client.region"] = self.region
        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDeniedException':
                SageMakerConnectionDisplay.send_error(
                    "Lakehouse catalog configurations could not be automatically added because your role does not have "
                    "the necessary permissions to call glue:getCatalogs. Please verify your permissions.")
            else:
                raise e

    def _set_auto_add_catalogs(self, val):
        self.auto_add_catalogs = False if val.casefold() == "false" else True
        # Regenerate default_config if auto_add_catalogs is defined by customer
        self._gen_default_config()
