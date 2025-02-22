
class Config:
    def __init__(self):
        self.session_id_prefix = None
        self.max_capacity = None
        self.number_of_workers = None
        self.worker_type = None
        self.glue_version = None
        self.security_config = None
        self.idle_timeout = None
        self.tags = {}
        self.session_type = None
        self.timeout = None
        self.spark_conf = None
        self.endpoint_url = None
        self.connections = None
        self.connections_override = None
        self.auto_add_catalogs = None


default_configs = Config()
