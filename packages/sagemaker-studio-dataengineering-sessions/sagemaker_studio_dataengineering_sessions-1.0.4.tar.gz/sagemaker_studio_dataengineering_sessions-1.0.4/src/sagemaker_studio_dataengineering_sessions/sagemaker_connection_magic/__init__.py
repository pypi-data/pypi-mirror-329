__version__ = '0.0.1'
import logging

from .sagemaker_connection_magic import SageMakerConnectionMagic
from sagemaker_studio_dataengineering_sessions.sagemaker_base_session_manager.common.logger_utils import setup_logger

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
setup_logger(logger, "SageMakerConnectionMagic", "connection_magic")

def load_ipython_extension(ipython):
    ipython.register_magics(SageMakerConnectionMagic)
