class GlueConnection(object):
    def __init__(self, connection_name: str,
                 connection_id: str,
                 region: str,
                 account: str,
                 project: str,
                 glue_connection: str,
                 glue_iam_role: str,
                 session_configs: dict[str, any],
                 related_redshift_properties: dict[str, any] | None = None):
        self.connection_name = connection_name
        self.connection_id = connection_id
        self.region = region
        self.account = account
        self.project = project
        self.glue_connection = glue_connection
        self.glue_iam_role = glue_iam_role
        self.session_configs = session_configs
        self.related_redshift_properties = related_redshift_properties
