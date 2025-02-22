class EmrOnServerlessConnection(object):
    def __init__(self, connection_name: str, connection_id: str, url: str, runtime_role: str, application_id: str, region: str):
        self.connection_name = connection_name
        self.connection_id = connection_id
        self.url = url
        self.runtime_role = runtime_role
        self.application_id = application_id
        self.region = region
