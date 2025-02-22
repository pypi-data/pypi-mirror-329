class RedshiftConnection(object):
    def __init__(self,
                 connection_name: str,
                 connection_id: str,
                 host: str,
                 database: str,
                 port: str,
                 auth_type: str,
                 region: str):
        self.connection_name = connection_name
        self.connection_id = connection_id
        self.host = host
        self.database = database
        self.port = port
        self.auth_type = auth_type
        self.region = region